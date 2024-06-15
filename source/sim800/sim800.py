
import time
from machine import UART


class Sim800:
    class _STATE:
        _STATES = {
            "PWR_UP",
            "IDLE",
            "IDLE_CONN"
            "DIALING",
            "IN_CALL",
        }
        def __init__(self, state = None):
            if state is not None:
                if state in self._STATES:
                    self._state = state
            else:
                self._state = "PWR_UP"
        def update(self, state):
            if state in self._STATES:
                self._state = state
            else:
                raise ValueError("Unknown state: ", state)
            print("State updated: ", self._state)
        def get(self) -> str:
            return self._state

    def __init__(self):
        self._port = UART(1, baudrate=115200, tx=21, rx=20)
        self._state = self._STATE()
        self._input_buffer = b""
        self._input_lines = []
        self._last_cpas_check_ts = 0


    def _write(self, data:str):
        self._port.write(data + '\r\n')
        print(">  ", data)

    def init(self):
        inbuf = ""
        send_at_ts = 0 
        while 1:
            if (time.ticks_ms() - send_at_ts > 1000):
                send_at_ts = time.ticks_ms()
                self._write("AT")
            if self.run():
                if len(self._input_lines) > 1:
                    i = self._input_lines.index(b'AT')
                    if self._input_lines[i+1] == b'OK':
                        self._input_lines = self._input_lines[2:]
                        break
                    elif self._input_lines[i+1] == b'AT':
                        self._input_lines = self._input_lines[1:]
                    print(self._input_lines)

        self._state.update("IDLE")
            
    def run(self) -> bool:
        if self._state.get() == "IDLE" and time.ticks_ms() - self._last_cpas_check_ts > 10000:
            self._last_cpas_check_ts = time.ticks_ms()
            self._cpas()
        while self._port.any():
            c = self._port.read(1)
            self._input_buffer += c
        if b"\n" in self._input_buffer:
            retval = self._parse_input_buffer()
            self._handle_input_lines()
            return retval
        return False
    
    def _parse_input_buffer(self) -> bool:
        retval = False
        self._input_buffer = self._input_buffer.replace(b"\r", b"")
        while b"\n" in self._input_buffer:
            i0 = self._input_buffer.find(b'\n')
            #print(i0)
            line = self._input_buffer[:i0]
            #print(self._input_buffer)
            self._input_buffer = self._input_buffer[i0+1:]
            #print(self._input_buffer)
            if len(line) > 0:
                self._input_lines.append(line)
                print("<< ", line, len(self._input_lines))
                retval = True
        return True

    def _handle_input_lines(self):
        new_input_lines = []
        for i,  line in enumerate(self._input_lines):
            if line[:2] == b"AT":
                # echo, ignore
                pass
            elif line[:5] == b"+CPAS":
                print("CPAS", line[7])
            elif line == b"OK"
            else:
                new_input_lines.append(line)
        self._input_lines = new_input_lines
            
        if b"+CPAS" in self._input_lines:
            pass

    def _cpas(self) -> None:
        self._write("AT+CPAS")

    def check_version(self):
        self._write("AT+CGMR")
    
    def incoming_call(self) -> bool:
        if b"RING" in self._input_lines:
            i = self._input_lines.index(b"RING")
            del self._input_lines[i]
            return True
        return False