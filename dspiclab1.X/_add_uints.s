    .nolist
    ; includes
    .list
    .include "xc.inc"
    ; w0 first operand used, not restored  
    ; w1 second operand used, not restored 
    ; w8 result register used, restored  
    .text
    .global _add_uints
_add_uints:
    ; save CORCON, PSVPAG and w8
    push  w8
    push  CORCON
    
    add    w0,w1,w8
    mov    w8,w0
    
    pop    CORCON
    pop   w8
    
    return
    .end
    