    .nolist
    ; includes
    .list
    .include "xc.inc"
    ; w0 first operand used, not restored  
    ; w1 second operand used, not restored 
    ; w8 result register used, restored  
    .text
    .global _dsp_instr_test
_dsp_instr_test:
    push CORCON
    push w4
    push w5
    
    ;BSET CORCON, #SATB
    
    sl w0,#3,w0
;    repeat #10
    lac [w0],A
    lac [w1],B
    
    pop w5
    pop w4
    pop CORCON
    return
    .end

