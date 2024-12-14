from machine import Pin, SLEEP, DEEPSLEEP
from time import sleep, ticks_ms
from logging import debug, info, warning, error

#from machine.Pin import PULL_UP, IRQ_FALLING, IRQ_RISING, IN
#from copy import deepcopy

class Dial:

    _MIN_NSI_DN_ms = 60
    _MIN_NSI_UP_ms = 60
    _MIN_NSA_DN_ms = 100
    _MIN_NSA_UP_ms = 100

    def __init__(self, nsa:int, nsi:int):
        self._buf=[]
        self._new_number_available = False
        self._new_num = None
        self._nsi_count:int = 0
        # NSA pin: when the dial starts to turn, this pin stays low until dial returns to idle position
        self._nsa = Pin(nsa, mode=Pin.IN, pull=Pin.PULL_UP)
        self._nsa_irq = self._nsa.irq(self._pin_irq, Pin.IRQ_FALLING | Pin.IRQ_RISING, wake=SLEEP|DEEPSLEEP)
        # NSI pin: pulses for the dialed number. pulled to low while idle, so 
        self._nsi = Pin(nsi, mode=Pin.IN, pull=Pin.PULL_UP)
        self._nsi_irq = self._nsi.irq(self._pin_irq, Pin.IRQ_RISING, wake=SLEEP|DEEPSLEEP)
        self.printbuf = ""
        self._last_nsi_dn = 0
        self._last_nsi_up = 0
        self._last_nsa_dn = 0
        self._last_nsa_up = 0
        info("Dial inited")

    def _pin_irq(self, pin:Pin):
        if pin == self._nsa:
            value = pin.value()
            self.printbuf += "A"
            if not value: # dial turn end
                t = ticks_ms()
                if (t - self._last_nsa_up < self._MIN_NSA_UP_ms):
                    return
                self._last_nsa_up = t
                self.printbuf += "a1 "
                if 1 <= self._nsi_count <= 9:
                    self._new_num = self._nsi_count
                    self._new_number_available = True
                elif self._nsi_count == 10:
                    self._new_num = 0
                    self._new_number_available = True
                elif self._nsi_count == 0:
                    pass
                else:
                    error(f"ERR: {self._nsi_count}")
            else:           # dial turn start
                t = ticks_ms()
                if (t - self._last_nsa_dn < self._MIN_NSA_DN_ms):
                    return
                self._last_nsa_dn = t
                self.printbuf += "a0 "
                self._nsi_count = 0
        if pin == self._nsi:
            value = pin.value()
            self.printbuf += "I"
            if value:
                t = ticks_ms()
                if (t - self._last_nsi_up < self._MIN_NSI_UP_ms):
                    return
                self._last_nsi_up = t
                self.printbuf += "i1 "
                self._nsi_count += 1
            else:
                t = ticks_ms()
                if (t - self._last_nsi_dn < self._MIN_NSI_DN_ms):
                    return
                self._last_nsi_dn = t
                self.printbuf += "i0 "

    def getNum(self) -> list:
        num = self._buf.pop(0) if len(self._buf) > 0 else None
        return num


    def run(self) -> None:
        if len(self.printbuf) > 0:
            #print(self.printbuf, end="")
            self.printbuf = ""
        if self._new_number_available:
            self._buf.append(self._new_num)
            self._new_number_available = False
            return True

