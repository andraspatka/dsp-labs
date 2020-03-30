.nolist
    ;.include "common.inc"
.list
;...............................................................................
; PID controller ASM implementation:
; y[n] = y[n-1] + c0*e[n] + c1*e[n-1] + c2*e[n-2]
; where y - is the control signal, e = ref - output is the error term
; ci are the coefficients with i = 0, 1, 2 defined as:
; c0 = kp + ki + kd, c1 = -(kp + 2*kd), c2 = kd with
; kp - the proportional gain, ki - the integral gain, kd - the derrivative gain
; and Ts as the sampling period.
;
; Operation:
;
;                                             ----   Proportional
;                                            |    |  Output
;                             ---------------| Kp |-----------------
;                            |               |    |                 |
;                            |                ----                  |
;Reference                   |                                     ---
;Input         ---           |           --------------  Integral | + | Control   -------
;     --------| + |  Control |          |   Ki*Ts*Z    | Output   |   | Output   |       |
;             |   |----------|----------| ------------ |----------|+  |----------| Plant |--
;        -----| - |Difference|          |     Z - 1    |          |   |          |       |  |
;       |      ---  (error)  |           --------------           | + |           -------   |
;       |                    |                                     ---                      |
;       | Measured           |         -------------------  Deriv   |                       |
;       | Outut              |        |    Kd( Z - 1 )    | Output  |                       |
;       |                     --------|   -------------   |---------                        |
;       |                             |        Ts*Z       |                                 |
;       |                              -------------------                                  |
;       |                                                                                   |
;       |                                                                                   |
;        -----------------------------------------------------------------------------------
;Inputs: 
;	w0 - address of coefficient vector
;	w1 - address of errorHistory vector
;	w2 - address of controlOutput vector
;Returns:
;	w0 - control output
; System resources usage:
;       {w0..w2}        used, not restored
;       {w8,w10}        saved, used, restored
;        AccA, AccB     used, not restored
;        CORCON         saved, used, restored
;
; DO and REPEAT instruction usage.
;       0 level DO instruction
;       1 REPEAT intructions

    .global _PID
_PID:

.ifdef __dsPIC33E
		push	DSRPAG
		movpag #0x0001, DSRPAG
.endif
; Save working registers.

 ; past control output
    
; Calculate PID control signal
    
; Update the output terms
   
; Update the error terms

; Reset CORCON and working registers  
 
    push CORCON   
    push w7 ; helper register
    push w8 ; x memory address register for coeff
    push w10 ; y memory address register for error
    push w11 ; y memory address register for control out
    
    mov w0, w10
    mov w1, w8
    mov w2, w11
    
    ; Put old u[n] to new u[n-1]
    mov [w11], w7
    inc2 w11, w11
    mov w7, [w11]

    ; initialize
    clr A, [w8], w4, [w10], w5
    
    repeat #3
    mac w4*w5, A, [w8]+=2, w4, [w10]+=2, w5
    
    lac [w11], B ; u[n-1]
    add A
    
    ; restore original address, this is were the new u[n] is going to be
    mov w2, w11
    
    sac A, w0
    mov w0, [w11]
    
    
    pop w11
    pop w10
    pop w8
    pop w7
    pop CORCON
    
.ifdef __dsPIC33E
    pop	    DSRPAG
.endif
    
    return 
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; _CoeffCalc:
;
;
; Operation: This routine computes the PID coefficients to use based on values
;            of Kp, Ki and Kd provided. The calculated coefficients are:
;             A = Kp + Ki + Kd
;             B = -(Kp + 2*Kd)
;             C = Kd
; Input:
;       w0 = kp
;	w1 = ki
;	w2 = kd
;       w3 = Address of computed coefficients
;
; Return:
;       (void)
;
; System resources usage:
;       {w0..w4}        used, not restored
;        AccA, AccB     used, not restored
;        CORCON         saved, used, restored
;
; DO and REPEAT instruction usage.
;       0 level DO instruction
;       0 REPEAT intructions
;
;............................................................................
    
    .global  _CoeffCalc
_CoeffCalc:
.ifdef __dsPIC33E
    push    DSRPAG
    movpag  #0x0001, DSRPAG
.endif
    push w7
    mov w3, w7 ;w7 is an address register
    
    ; Calc coeff A = Kp + Ki + Kd
    lac w0, A
    lac w1, B
    add A ; A = kp + ki
    lac w2, B
    add A ; A = kp + ki + kd
    sac A, [w7]
    inc2 w7, w7
    ; Calc coeff B = -(Kp + 2*Kd)
    lac w2, A
    add A ; 2 * Kd (B already contains w2 a.k.a Kp)
    lac w0, B
    add A ; Kp + 2 * Kd
    neg A ; - (Kp + 2 * Kd)
    sac A, [w7]
    inc2 w7, w7
    ; Calc coeff C = Kd
    mov w2, [w7]
    
    pop w7
.ifdef __dsPIC33E
    pop	    DSRPAG
.endif
    return
    .end
    