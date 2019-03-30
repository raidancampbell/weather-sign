import time
import serial


# an interface for writing data to Rice Lake's EL233 Flip-Digit display
class EL233:
    def __init__(self, serial_port, baud_rate=4800, byte_size=serial.SEVENBITS, stop_bits=serial.STOPBITS_TWO,
                 parity=serial.PARITY_ODD):
        # these values are read from the internal switch 1 positions
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.byte_size = byte_size
        self.stop_bits = stop_bits
        self.parity = parity
        self.ser = serial.Serial(port=self.serial_port, baudrate=self.baud_rate, bytesize=self.byte_size,
                                 parity=self.parity, stopbits=self.stop_bits, write_timeout=0, timeout=0)

    def _write_value(self, value):
        stx = chr(2)  # start symbol
        polarity = ' '  # polarity, left section will be temperature
        weight = value  # 7 digits, right justified, dummy zeroes,
        # decimal point with no leading zeroes except for zero preceding decimal point
        # leading zeroes transmitted as spaces
        unit = 'L'  # must not be space, even though that's legal in the documentation
        weight_type = 'G'  # Gross/Net, doesn't matter
        status = 'M'  # must not be space, even though that's legal in the documentation
        termination = '\r\n'

        combined_command = f'{stx}{polarity}{weight}{unit}{weight_type}{status}{termination}'
        print(f'writing string:"{str.encode(combined_command)}"')
        if len(str.encode(combined_command)) != 14:
            print('invalid output!')
            print(str.encode(combined_command))
        else:
            resp = self.ser.write(str.encode(combined_command))
            print(resp)

    def display_temp_and_humidity(self, temp, humidity):
        is_temp_negative = temp < 0
        temp_str = str(abs(temp)).zfill(3 if not is_temp_negative else 2)
        humidity_str = str(humidity).zfill(2)
        prefix = '_' if is_temp_negative else ''
        self._write_value(f'0{prefix}{temp_str}F{humidity_str}')

    def check_and_recover(self):
        if not self.ser or self.ser.closed:
            self.ser = serial.Serial(port=self.serial_port, baudrate=self.baud_rate, bytesize=self.byte_size,
                                     parity=self.parity, stopbits=self.stop_bits, write_timeout=0, timeout=0)

    def __del__(self):
        time.sleep(0.2)
        if self.ser:
            self.ser.close()

# sign.ser.write(b'\x02 00HELLOLGM\r\n')
