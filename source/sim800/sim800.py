
import time
from logging import debug, info, warning, error
from .sim800_serial import Sim800Serial

class Sim800:

    def __init__(self):
        self._port = Sim800Serial(1, baudrate=115200, tx=21, rx=20)
        self._state = "POWER_UP"
        self._last_cpas_check_ts = 0
        self.pinok = False
    

    def _state_functions(self, state:str=None, keys:bool=False):
    
        fuctions_dict = {
            "POWER_UP":     self._run_power_up,
            "OFFLINE":      self._run_offline,
            "CONNECTING":   self._run_connecting,
            "ONLINE":       self._run_online,
            "DIALING":      self._run_dialing,
            "RINGING":      self._run_ringing,
            "IN_CALL":      self._run_in_call,
        }
        if keys:
            return fuctions_dict.keys()
        try:
            retval = fuctions_dict[state]
        except KeyError as e:
            raise AttributeError(f"'{state} not a valid value for state")
        return retval

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        if new_state in self._state_functions(keys=True):
            debug(f"{self.state} -> {new_state}")
            self._state = new_state
        else:
            raise AttributeError(f"'{new_state} not a valid value for state")
    
    @state.deleter
    def state(self):
        raise AttributeError("'state' cannot be deleted")


    def _write(self, data:str):
        self._port.write(data + '\r\n')
        info(f">  {data}")
    
    def _transaction(self, data:str):
        info(f">> {data}")
        return self._port.transaction(data + '\r\n')
    
    def send_command(self, data:str):
        self._transaction(data)
        time.sleep(0.1) # allow time for answer
        start = time.monotonic_ns()

    def power_off(self):
        self._transaction("AT+CPOWD=1")

    def run(self) -> bool:
        self._port.run()
        handle_state = self._state_functions(self.state)
        handle_state()
        if "RING" in self._port._input_buffer:
            return True
        return False
    
    def ringing(self) -> bool:
        if "RING" in self._port._input_buffer():
            del self._port._input_buffer[self._port._input_buffer.index("RING")]
            return True
        return False


    ###############################
    # state specific run handlers #
    ###############################

    def _run_power_up(self) -> None:
        # -> OFFLINE
        if not self._transaction("AT"):
            return
        if not self._transaction("ATE0"): # turn off echo 
            return
        if not self._transaction("AT+CFUN=1"): # set modem to full functionality
            return
        # fallthrough, modem is ready
        self.state = "OFFLINE"

    def _run_offline(self) -> None:
        # -> CONNECTING
        self.check_pin()
        pass


    def check_pin(self):
        if not self.pinok:
            if self._transaction("AT+CPIN=2538"):
                self.pinok = True
                pass
            else:
                error("no pin")

    def _run_connecting(self) -> None:
        # -> ONLINE
        # -> OFFLINE
        pass

    def _run_online(self) -> None:
        # -> OFFLINE
        # -> DIALING
        # -> RINGING
        if time.ticks_ms() - self._last_cpas_check_ts > 10000:
            self._last_cpas_check_ts = time.ticks_ms()
            self._cpas() # TODO: go offline if CPAS fails
        pass

    def _run_dialing(self) -> None:
        # -> IN_CALL
        # -> ONLINE
        pass

    def _run_ringing(self) -> None:
        # -> IN_CALL
        # -> ONLINE
        pass

    def _run_in_call(self) -> None:
        # -> ONLINE
        pass


    def _cpas(self) -> None:
        self._write("AT+CPAS")

    def check_version(self):
        self._write("AT+CGMR")
    
    # def incoming_call(self) -> bool:
    #     if b"RING" in self._input_lines:
    #         i = self._input_lines.index(b"RING")
    #         del self._input_lines[i]
    #         return True
    #     return False