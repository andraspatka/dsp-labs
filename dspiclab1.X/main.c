/*
 * File:   main.c
 * Author: andraspatka
 *
 * Created on March 12, 2020, 3:46 PM
 */


#include "xc.h"
#include "main_header.h"

int counter = 0;

/**
 * leosztas ki volt dolgozva amivel kijon a 140 MHZ, datasheetben megvan a keplet
 * ami szerint
 */
void SetupOscillator(){
    // bizonyos regek vedve vannak, azert kell ez
    // ez ha at akarunk iranyitani dolgokat
    __builtin_write_OSCCONL((uint8_t) (0x300 & 0x00FF)); 
    CLKDIV = 0x3100; // PLL leosztasat allitja be
    OSCTUN = 0x0;
    REFOCON = 0x0;
    PLLFBD = 0x44;
    // CORCON a DSP utasitasokra vannak
    CORCONbits.RND = 0; // RNG leallitasa
    CORCONbits.SATB = 0; // akkumulator telitese
    CORCONbits.SATA = 0; // akku
    CORCONbits.ACCSAT = 0; // globalis akkumulator telites
    //while(OSCCONbits.LOCK!=1); // csak valos hardver eseten
}

/**
 * Idozito diagram szerint tortenik ennek beallitasa
 * DATASHEET
 * 
 */
void initTMR1(){
    TMR1 = 0;
    PR1 = 0x222E; // LEOSZTO
    T1CON = 0x8010;
    IFS0bits.T1IF = 0; // interuupt flag 0
    IEC0bits.T1IE = 1; // interrupt enable
}

void initTMR3(){
    TMR3 = 0; // Timer3 value
    PR3 = 0x1117; // PERIOD register half of PR1
    T3CON = 0x8010; 
    IFS0bits.T3IF = 0;
    IEC0bits.T3IE = 1;
}

/**
 * DATASHEET uartx simplified block diagram
 */
void initUART(){
    U1MODEbits.STSEL = 0;
    U1MODEbits.PDSEL = 0;
    U1MODEbits.ABAUD = 0;
    U1MODEbits.BRGH = 1; 
    
    U1BRG = BRGVAL;
    U1STAbits.URXISEL = 3;
    IEC0bits.U1RXIE = 1;
    U1MODEbits.UARTEN = 1; 
    U1STAbits.UTXEN = 1; 
}

/**
 * ha ez meg van irva akkor a printf ezt hasznalja
 * @param c
 */
void putCharUART(char c){
    while (U1STAbits.UTXBF);
    U1TXREG = c;
}
/**
 * datasheet 23.0 chapter
 * 10/12 bitben hasznlahato
 * 
 */
void InitADC(){
    ANSELAbits.ANSA0 = 1; // referebcua feszultsegek
    ANSELAbits.ANSA1 = 1; // ref feszultsegek
    AD1CON1bits.FORM = 3;
    AD1CON1bits.SSRC = 2;
    AD1CON1bits.ASAM = 1;
    AD1CON1bits.AD12B = 1; // 12 bites uzemod
    AD1CON2bits.CHPS = 0;
    
    AD1CON3bits.ADRC = 0;
    AD1CON3bits.ADCS = 6;
  
    AD1CON2bits.SMPI    = 0; 
    AD1CON4bits.ADDMAEN = 1;  
    
    AD1CHS0bits.CH0SA=0;  // channel 0 kivalasztas
    AD1CHS0bits.CH0NA=0;  
 
    // megszakitast lenullazzuk es lezarjuk
    IFS0bits.AD1IF = 0;  
    IEC0bits.AD1IE = 0; 

    AD1CON1bits.ADON = 1; // engedelyezi a beolvasast
}  

/**
 * psv - priority set vector automatikas legyen veallitva, nem erdekel minket
 * T1IF ha nem nullazzuk, akkor nem fog tobbet meghivodni
 * 
 */
void __attribute__((interrupt, no_auto_psv)) _T1Interrupt(void){
    counter++;
    if(counter == 500){
        counter = 0;
        LATAbits.LATA8 ^= 1;
    }
    
    IFS0bits.T1IF = 0;
}

/**
 * 
 * Clear ADC SAMP register to start a conversion
 * Wait while the conversion is done (AD1CON1 DONE bit is set)
 * Read the converted value from ADC1BUF0
 * Convert the Q15 value to voltage (0V to 3.3V)
 * Send the data to the PC on USART (Attention: 12b data must be sent as 2 bytes)
 */
void __attribute__((interrupt, no_auto_psv)) _T3Interrupt(void){
    
    unsigned int temp_data;
    AD1CON1bits.SAMP = 0;  
    while ( !AD1CON1bits.DONE );
    temp_data = ADC1BUF0;
    
    IFS0bits.T3IF = 0;
}

int main(void) {
    
//    char c = add_uints(3, 4);
//    
//    c = c + 1;
//    
    dsp_instr_test(memXdata, memYdata);
    
    uint16_t res = ed_test(A, B);
    
    res = res + 0;
    
    CoeffCalc(kp, ki, kd, coeff);
    int16_t result = PID(coeff, error, cout);
    result++;
//    SetupOscillator();
//    initUART();
//    InitADC();
//    initTMR3();
//    initTMR1();
//    while (1);
    return 0;
}
