import sys
from sim800 import Sim800
from dial import Dial
from time import sleep, ticks_ms
from machine import Pin, ADC

from logging import DEBUG, INFO, WARNING, ERROR, basicConfig as logConfig
from logging import debug, info, warning, error

LOG_LEVEL = DEBUG


logConfig(format="%(asctime)10s %(levelname)-8s %(message)s", level=LOG_LEVEL)

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
    info("MAIN")

    dial_num_buf = []
    last_number_dialed_ts = 0

    dial = Dial(nsa=pinout["NSA"], nsi=pinout["NSI"])
    adc_en = Pin(pinout["ADC_EN"], Pin.OUT)
    adc_en.off()
    adc = ADC(Pin(pinout["ADC_BATT"]), atten=ADC.ATTN_11DB)
    info(f"ADC: {read_battery(adc_en, adc)}")
    es = Pin(pinout["ES1"], Pin.IN, pull=Pin.PULL_UP)
    gsm = Sim800()
    #gsm.init()
    #gsm.check_version() # debug
    fork = Pin(pinout["GS"], pull=Pin.PULL_UP)
    fork_state = 1
    while 1:
        if fork_state != fork.value():
            fork_state = 1 - fork_state
            if not fork_state:
                info("Abgehoben")
            else:
                info("Aufgelegt")
        if dial.run():
            #something to do
            a = dial.getNum()
            if a is not None:
                debug(str(a))
                dial_num_buf.append(a)
                last_number_dialed_ts = ticks_ms()
                pass
        if len(dial_num_buf) > 0 and (ticks_ms() - last_number_dialed_ts) > DIAL_TIMEOUT:
            number = "".join(str(n) for n in dial_num_buf)
            info(f" Wählt: {number}")
            dial_num_buf = []
        if gsm.run():
            if gsm.ringing():
                # TODO: let the bells sing
                
                pass
            # something to do
            #if gsm.incoming_call():
            #    print("RING")
            #    pass
            pass
        if not es.value():
            start = ticks_ms()
            info("Shutdown?")
            while not es.value():
                if ticks_ms() - start > 2000:
                    gsm.power_off()


        sleep(0.01)

    pass


def read_battery(adc_en:Pin, adc:ADC) -> float:
    adc_en.on()
    sleep(0.01)
    voltage = adc.read_uv()
    adc_en.off()
    return voltage*2.2/1e6

if __name__ == "__main__":
    main()

