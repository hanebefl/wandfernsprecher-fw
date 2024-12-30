from machine import Pin, PWM, Timer
from time import sleep
pins = {
    0: "ADC",
    1: "ADC_EN",
    2: "ES1",
    3: "HV_EN",
    4: "BELL_B",
    5: "BELL_A",
    6: "GS",
    7: "NSI",
    8: "ES2",
    9: "BOOT",
    10: "NSA"
}

a = Pin(5, Pin.OUT)
a.off()
b = Pin(4, Pin.OUT)
b.off()

def toggle(foo):
    if a.value():
        a.off()
        b.on()
    else:
        b.off()
        a.on()

#def type_timer():
#    tim0 = Timer(0)
#    tim0.init(freq=20, mode=Timer.PERIODIC, callback=toggle)
#    sleep(2)
#    tim0.deinit()


try:
    print("try")
    hv_en = Pin(3, Pin.OUT)
    hv_en.off()


    while 1:
        print("while1")
        hv_en.on()
        sleep(0.2)
        print("tim0")
        tim0 = Timer(0)
        print("init")
        # double the frequency, because toggling halves it again.
        tim0.init(freq=20*2, mode=Timer.PERIODIC, callback=toggle)
        print("init_done")
        sleep(2.0)
        print("deinit")
        tim0.deinit()
        print("off")
        hv_en.off()
        sleep(5)


            
            
except KeyboardInterrupt:
    pass