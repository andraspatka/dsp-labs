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
;       0 REPEAT intructions

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
    
    ;calc kp
    lac w0, A
    lac w1, B
    add A ; A = kp + ki
    lac w2, B
    add A ; A = kp + ki + kd

.ifdef __dsPIC33E
    pop	    DSRPAG
.endif
    
    .end
    