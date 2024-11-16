import sys
#from sim800 import Sim800
from dial import Dial
from time import sleep, ticks_ms
from machine import Pin

# pinout revision: 0.0.1
pinout = {
    "SIM_TX":   20, # SIM800 TX pin
    "SIM_RX":   21, # SIM800 RX pin
    "USB_D-":   18, # for debug/dev
    "USB_D+":   19, # for debug/dev
    "ES1":      2,  # ErdSchalter
    "ES2":      8,  # ErdSchalter
    "NSA":      10,  # NummernSchalter Aktiv
    "NSI":      7,  # NummernSchalter Impulse
    "GS":       6,  # GabelSchalter
    "HV_EN":    3,  # power supply for bell
    "BELL_A":   5,  # H-bridge bell
    "BELL_B":   4, # H-bridge bell
    "ADC_EN":   1,
    "ADC_BATT": 0,  # battery voltage
}

DIAL_TIMEOUT = 3000

def main():
    print("MAIN")

    dial_num_buf = []
    last_number_dialed_ts = 0

    dial = Dial(nsa=pinout["NSA"], nsi=pinout["NSI"])
    #gsm = Sim800()
    #gsm.init()
    #gsm.check_version() # debug
    fork = Pin(pinout["GS"], pull=Pin.PULL_UP)
    fork_state = 1
    while 1:
        if fork_state != fork.value():
            fork_state = 1 - fork_state
            if not fork_state:
                print("Abgehoben")
            else:
                print("Aufgelegt")
        if dial.run():
            #something to do
            a = dial.getNum()
            if a is not None:
                print(a, end="")
                dial_num_buf.append(a)
                last_number_dialed_ts = ticks_ms()
                pass
        if len(dial_num_buf) > 0 and (ticks_ms() - last_number_dialed_ts) > DIAL_TIMEOUT:
            number = "".join(str(n) for n in dial_num_buf)
            print(f" Wählt: {number}")
            dial_num_buf = []
        #if gsm.run():
        #    # something to do
        #    if gsm.incoming_call():
        #        print("RING")
        #        pass
        #    pass
        
        


        sleep(0.01)

    pass



if __name__ == "__main__":
    main()

