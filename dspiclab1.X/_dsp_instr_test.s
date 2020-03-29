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
    push w6
    push w7
    push w8
    push w10
    push w13
    
    BSET CORCON, #SATA
    BSET CORCON, #SATB
    
    lac [w0],#-4,A    
    lac [w1],#-4,B
    
    repeat #2
    add B
    
    repeat #2
    add A
    
    mov w0, w8
    mov w1, w10
    mov #5014, w13
    
    clr B,[w8]+=2,w4,[w10]+=2,w5,[w13]+=2
    
    ed w4*w4, B, [w8]+=2, [w10]+=2, w4
    
    ;BSET CORCON, #IF
    
    mov #0x2000, w4
    mov #0x4000, w5
    mpy w4*w5, A
    mpy.n w4*w5, A
    
    BSET CORCON, #IF ; integer mode
    ;bset CORCON, #ACCSAT ;super saturation enabled
    
    clr A
    mov #0xA022, w4
    mov #0xB900, w5
    mac w4*w5, A;, [w8] += 2, w4, [w10] += 2, w5, w3
    
    pop w13
    pop w10
    pop w8
    pop w7
    pop w6
    pop w5
    pop w4
    pop CORCON
    return
    .end


    