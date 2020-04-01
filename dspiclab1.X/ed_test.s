    .nolist
    ; includes
    .list
    .include "xc.inc"
    ; w0 first operand used, not restored  
    ; w1 second operand used, not restored 
    ; w8 result register used, restored  
    .text
    .global _ed_test
_ed_test:
     push        CORCON
     push       w4
     push       w8
     push       w10
     
     clr A
     mov                #0x0, w4
     mov                w0, w8
     mov                w1, w10
     edac       w4*w4, A, [w8]+=2, [w10]+=2, w4
     edac       w4*w4, A, [w8], [w10], w4
     edac       w4*w4, A, [w8], [w10], w4

    sftac A, #-16
     sac                A, w0

     pop                w10
     pop                w8
     pop                w4
     pop                CORCON
     return
    .end
