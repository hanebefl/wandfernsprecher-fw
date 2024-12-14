
from time import ticks_ms
from machine import UART
from logging import debug, info, warning, error


class Sim800Serial:
    def __init__(self, id, baudrate=115200, bits=8,  parity=None, stop=1, *args, **kwargs) -> None:
        self._uart = UART(id)
        self._uart.init(baudrate, bits, parity, stop, *args, **kwargs)
        self._lines = []
        self._input_buffer = b""

    def run(self):
        if self._receive():
            if self._parse_input_buffer():
                self._handle_lines()
        pass

    def write(self, *args, **kwargs) -> None:
        self._uart.write(*args, **kwargs)
        pass

    def transaction(self, command:str, timeout:int = 500) -> bool:
        lines = []
        self._uart.write(command.encode('UTF-8'))
        transaction_start = ticks_ms()
        while True:
            if ticks_ms() - transaction_start > timeout:
                #TODO: maybe clear some buffer?
                return False
            if self._receive():
                if self._parse_input_buffer(into=lines):
                    debug(f"lines {lines}")
                    if lines[-1] == b'OK':
                        return True
                    elif lines[-1] == b'RING':
                        self._lines.append(b'RING')
                        
    def clear(self) -> None:
        self._lines = []


    def _receive(self) -> bool:
        # TODO: add timeout if a lot of input data
        retval = False
        while self._uart.any():
            retval = True
            c = self._uart.read(1)
            self._input_buffer += c
            debug(f"received <<{c}")
        return retval



    def _parse_input_buffer(self, into:list=None) -> bool:
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
                if into is None:
                    self._lines.append(line)
                else:
                    into.append(line)
                info(f"parsed << {line} {len(self._lines)}")
                retval = True
        return retval

    def _handle_lines(self):
        new_lines = []
        for i,  line in enumerate(self._lines):
            if line[:2] == b"AT":
                # echo, ignore
                pass
            elif line[:5] == b"+CPAS":
                print("CPAS", line[7])
            else:
                new_lines.append(line)
        self._lines = new_lines
        #TODO: make sense of this. Delete b"OK" after +CPAS