/* 
 * File:   main_header.h
 * Author: andraspatka
 *
 * Created on March 12, 2020, 3:46 PM
 */

#ifndef MAIN_HEADER_H
#define	MAIN_HEADER_H

#ifdef	__cplusplus
extern "C" {
#endif

// FPOR
#pragma config ALTI2C1 = OFF            // Alternate I2C1 pins (I2C1 mapped to SDA1/SCL1 pins)
#pragma config ALTI2C2 = OFF            // Alternate I2C2 pins (I2C2 mapped to SDA2/SCL2 pins)
#pragma config WDTWIN = WIN25           // Watchdog Window Select bits (WDT Window is 25% of WDT period)

// FWDT
#pragma config WDTPOST = PS32768        // Watchdog Timer Postscaler bits (1:32,768)
#pragma config WDTPRE = PR128           // Watchdog Timer Prescaler bit (1:128)
#pragma config PLLKEN = ON              // PLL Lock Enable bit (Clock switch to PLL source will wait until the PLL lock signal is valid.)
#pragma config WINDIS = OFF             // Watchdog Timer Window Enable bit (Watchdog Timer in Non-Window mode)
#pragma config FWDTEN = OFF             // Watchdog Timer Enable bit (Watchdog timer enabled/disabled by user software)

// FOSC
#pragma config POSCMD = XT              // Primary Oscillator Mode Select bits (XT Crystal Oscillator Mode)
#pragma config OSCIOFNC = OFF           // OSC2 Pin Function bit (OSC2 is clock output)
#pragma config IOL1WAY = ON             // Peripheral pin select configuration (Allow only one reconfiguration)
#pragma config FCKSM = CSDCMD           // Clock Switching Mode bits (Both Clock switching and Fail-safe Clock Monitor are disabled)

// FOSCSEL
#pragma config FNOSC = PRIPLL           // Oscillator Source Selection (Primary Oscillator with PLL module (XT + PLL, HS + PLL, EC + PLL))
#pragma config IESO = ON                // Two-speed Oscillator Start-up Enable bit (Start up device with FRC, then switch to user-selected oscillator source)

// FGS
#pragma config GWRP = OFF               // General Segment Write-Protect bit (General Segment may be written)
#pragma config GCP = OFF                // General Segment Code-Protect bit (General Segment Code protect is Disabled)

// #pragma config statements should precede project file includes.
// Use project enums instead of #define for ON and OFF.

#include <xc.h>
#include <stdio.h>
#include <stdlib.h>
    
#define FOSC 140000000
#define FCY (FOSC/2)
#define BAUDRATE 115200
#define BRGVAL ((FCY/BAUDRATE)/4) - 1
    
extern char add_uints(char,char);

uint16_t memXdata[10] __attribute__ ((space(xmemory), address(0x1000))) = {10, 16, 3, 4, 5, 6, 7, 8, 9, 10};
int16_t memYdata[10] __attribute__ ((space(ymemory), address(0x5000))) = {10, 5, -8, 7, 6, 5, 4, 3, 2, 1};

extern void dsp_instr_test(uint16_t* Xmem, int16_t* Ymem);

int16_t kp = 1;
int16_t ki = 2;
int16_t kd = 3;

int16_t coeff[3] __attribute__ ((space(ymemory), address(0x5020)));
int16_t cout[2] __attribute__ ((space(ymemory), address(0x5026))) = {5, 6};
int16_t error[3] __attribute__ ((space(xmemory), address(0x1020))) = {1, 2, 3};

uint16_t A[2] __attribute__ ((space(xmemory), address(0x1040))) = {3,2};
uint16_t B[2] __attribute__ ((space(ymemory), address(0x5040))) = {1,1};

extern uint16_t ed_test(uint16_t*, uint16_t*);

extern int16_t PID(int16_t * coeff, int16_t * error, int16_t * cout);

extern void CoeffCalc(int16_t kp, int16_t ki, int16_t kd, int16_t * coeff);

#ifdef	__cplusplus
}
#endif

#endif	/* MAIN_HEADER_H */

