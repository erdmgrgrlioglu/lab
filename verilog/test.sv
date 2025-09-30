`timescale 1ns / 10 ps

module clock (
    output logic CLK;
);
    
    always begin
        CLK = 1;
        #1;
        CLK = 0;
        #1;
    end

endmodule