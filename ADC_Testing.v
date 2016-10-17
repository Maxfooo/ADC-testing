`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: Alphacore Inc.
// Engineer: Max Ruiz
// 
// Create Date:    12:24:52 09/19/2016 
// Design Name: 
// Module Name:    ADC_Testing_Top 
// Project Name: 
// Target Devices: 
// Tool versions: 
// Description: 
//
// Dependencies: 
//
// Revision: 
// Revision 0.01 - File Created
// Additional Comments: 
//
//////////////////////////////////////////////////////////////////////////////////
module ADC_Testing_Top(
	input clk, 
	input adc_clk,
	input [PRECISION-1:0] adc_code_in,
	input ext_reset,
	
	// Opal Kelly
	input  wire [7:0]  hi_in,
	output wire [1:0]  hi_out,
	inout  wire [15:0] hi_inout,
	inout wire hi_aa,    
	
	output wire i2c_sda,
	output wire i2c_scl,
	output wire hi_muxsel 
);

parameter PRECISION = 10;
parameter FIFO_COUNT_WIDTH = 12;


/*************************************************/
//------------ Handle reset signals -------------//
/*************************************************/
wire reset; // internal reset, FrontPanel
wire ext_rst;
wire rst;
// DEBUG
//assign rst = reset | ext_rst;
assign rst = reset;
// DEBUG

Debounce debounce_0(
	.clk(clk),
	.signalIn(ext_reset),
	.signalOut(ext_rst)
);


/*************************************************/
//------------------- FIFO ----------------------//
/*************************************************/
reg rd_en = 1'b0;
wire [PRECISION-1:0] adc_code_out;
wire fifo_full;
wire fifo_empty;
wire [FIFO_COUNT_WIDTH-1:0] rd_data_count;
wire [FIFO_COUNT_WIDTH-1:0] wr_data_count;
wire fifo_clk;
fifo_adc fifo_adc_0(
  .rst(rst),
  .wr_clk(adc_clk), // data will be avaible for reading from ADC on negedge of adc_clock
  .rd_clk(fifo_clk),
  .din(adc_code_in), // 10 bit;
  .wr_en(1'b1),
  .rd_en(rd_en),
  .dout(adc_code_out), // 10 bit;
  .full(fifo_full),
  .empty(fifo_empty),
  .rd_data_count(rd_data_count), // 12 bit;
  .wr_data_count(wr_data_count) // 12 bit; provides how many words are in the fifo, how full is the fifo
);

// Data should be available as the host requests it via epA0read.
always @(posedge ti_clk) begin
	rd_en <= epA0read;
end


/*************************************************/
//------------- Opal Kelly Comm. ----------------//
/*************************************************/
/*
file:///C:/Users/Alphacore%20Engineer%201/Desktop/FrontPanel-UM.pdf
page 41

Endpoint Type | Address Range | Sync/Async   | Data Type
-------------------------------------------------------------------
Wire In 	     | 0x00 - 0x1F 	| Asynchronous | Signal state
Wire Out 	  | 0x20 - 0x3F 	| Asynchronous | Signal state
Pipe In       | 0x80 - 0x9F   | Synchronous  | Multi-byte transfer
Pipe Out      | 0xA0 - 0xBF   | Synchronous  | Multi-byte transfer

ENDPOINT DATAWIDTH
Endpoint Type | USB 2.0
-----------------------
Wire			  | 16bit
Pipe          | 16bit
*/

// Target interface bus
wire ti_clk;
wire [30:0] ok1;
wire [16:0] ok2;

// OK uC comm.
assign i2c_sda = 1'bz;
assign i2c_scl = 1'bz;
assign hi_muxsel = 1'b0;

// HDL bus
parameter EP_OUTPUTS = 7; // define number of connections to OK OR block
wire [17*EP_OUTPUTS-1:0] ok2x;

// Host to HDL connection module
okHost hostIF (
	.hi_in(hi_in),
	.hi_out(hi_out),
	.hi_inout(hi_inout),
	.hi_aa(hi_aa),
	.ti_clk(ti_clk),
	.ok1(ok1),
	.ok2(ok2)
);

//--------------------------------------------------
//-------------------- WIRE IN ---------------------
//--------------------------------------------------
wire [15:0] ep00wire; // reset
assign reset = ep00wire[0];
okWireIn wire00 (
	.ok1(ok1),
	.ep_addr(8'h00),
	.ep_dataout(ep00wire)
);


wire [15:0] ep01wire; // R_sel
wire [3:0] R_sel;
assign R_sel = ep01wire[3:0];
okWireIn wire01 (
	.ok1(ok1),
	.ep_addr(8'h01),
	.ep_dataout(ep01wire)
);

wire [15:0] ep02wire; // shift_clk_ctrl[0], pix_out_ctrl[1]
wire shift_clk_ctrl;
assign shift_clk_ctrl = ep02wire[0];
wire pix_out_ctrl;
assign pix_out_ctrl = ep02wire[1];
okWireIn wire02 (
	.ok1(ok1),
	.ep_addr(8'h02),
	.ep_dataout(ep02wire)
);

//--------------------------------------------------
//-------------------- WIRE OUT --------------------
//--------------------------------------------------
//==== Testing/Debugging ====
wire [15:0] ep20wire; // wire out, fifo_empty
assign ep20wire[0] = fifo_empty;
okWireOut wire20 (
	.ok1(ok1),
	.ok2(ok2x[0*17 +: 17]),
	.ep_addr(8'h20),
	.ep_datain(ep20wire)
);

//--------------------------------------------------
//-------------------- PIPE OUT --------------------
//--------------------------------------------------

//==== Testing/Debugging ====
wire [15:0] epA0pipe; // pipe out; adc data from fifo
wire epA0read; // pipe out read signal from host
okPipeOut pipeA0 (
	.ok1(ok1),
	.ok2(ok2x[1*17 +: 17]),
	.ep_addr(8'hA0),
	.ep_datain(epA0pipe), // data from FIFO
	.ep_read(epA0read) // enable rd_en at FIFO
);

wire [15:0] epA1pipe; // pipe out; wr_data_count
assign epA1pipe = wr_data_count;
wire epA1read;
okPipeOut pipeA1 (
	.ok1(ok1),
	.ok2(ok2x[2*17 +: 17]),
	.ep_addr(8'hA1),
	.ep_datain(epA1pipe), // data from FIFO
	.ep_read(epA1read) // enable rd_en at FIFO
);

//==== Chip #1 ====
wire [15:0] epA4pipe; // pipe out; Chip#1 ADC_0
wire epA4read;
okPipeOut pipeA4 (
	.ok1(ok1),
	.ok2(ok2x[3*17 +: 17]),
	.ep_addr(8'hA4),
	.ep_datain(epA4pipe), // data from FIFO
	.ep_read(epA4read) // enable rd_en at FIFO
);

wire [15:0] epA5pipe; // pipe out; Chip#1 ADC_1
wire epA5read;
okPipeOut pipeA5 (
	.ok1(ok1),
	.ok2(ok2x[4*17 +: 17]),
	.ep_addr(8'hA5),
	.ep_datain(epA5pipe), // data from FIFO
	.ep_read(epA5read) // enable rd_en at FIFO
);

wire [15:0] epA6pipe; // pipe out; Chip#1 ADC_2
wire epA6read;
okPipeOut pipeA6 (
	.ok1(ok1),
	.ok2(ok2x[5*17 +: 17]),
	.ep_addr(8'hA6),
	.ep_datain(epA6pipe), // data from FIFO
	.ep_read(epA6read) // enable rd_en at FIFO
);

wire [15:0] epA7pipe; // pipe out; Chip#1 ADC_3
wire epA7read;
okPipeOut pipeA7 (
	.ok1(ok1),
	.ok2(ok2x[6*17 +: 17]),
	.ep_addr(8'hA7),
	.ep_datain(epA7pipe), // data from FIFO
	.ep_read(epA7read) // enable rd_en at FIFO
);


//--------------------------------------------------
//------------------ Trigger In --------------------
//--------------------------------------------------

wire [15:0] ep40trigger;
wire next_row;
assign next_row = ep40trigger[0];
wire shift_clk; // may need to change
okTriggerIn ep40trigger (
	.ok1(ok),
	.ep_addr(8'h40),
	.ep_clk(shift_clk), // may need to change
	.ep_trigger(ep40trigger),
);


okWireOR #(.N(EP_OUTPUTS)) wireOR(
	.ok2(ok2),
	.ok2s(ok2x)
);

/*************************************************/
//------------- Readback ADC data ---------------//
/*************************************************/

assign epA0pipe = {{6 {1'b0}}, adc_code_out}; // 6-0's appended to 10bits of adc data

assign fifo_clk = ~ti_clk; // page 50 of FrontPanel-UM.pdf


/*************************************************/
//------------- Write in ADC data ---------------//
/*************************************************/

// Writing data is all taken care of via the ADC signals


/*************************************************/
//------------------- DEBUG ---------------------//
/*************************************************/




endmodule
