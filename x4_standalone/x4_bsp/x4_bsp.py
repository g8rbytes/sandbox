from typing import List
from time import sleep
from serial.tools import list_ports
from x4_test_bench.x4_standalone.x4_bsp.crc_generator.crc_generator import *
from x4_test_bench.x4_standalone.x4_bsp.x4_serial_port.x4_serial_port import *
from x4_test_bench.x4_standalone.x4_bsp.x4_cmds.x4_cmds import *

class x4Bsp:
    def __init__(self, **kwargs):
        """
        :param x4_serial_port: Serial port object to be used for communication with the x4 board
        :param x4_cmds: Command objects to be used for communication with the x4 board
        :param crc_generator: CRC generator object to be used for generating CRC values for commands
        """
        # Configure the serial port using settings from yml file and open it
        self.x4_serial = kwargs['x4_serial_port'] if 'x4_serial_port' in kwargs else x4SerialPort()
        # self.open_port()

        # Initialize command objects from yml file
        self.x4_cmds = kwargs['x4_cmds'] if 'x4_cmds' in kwargs else {}

        # Init CRC generator object to class attribute from yml file
        self.crc_gen = kwargs['crc_generator'] if 'crc_generator' in kwargs else CrcGenerator(poly=0x65, crc_init=0x00, data_len=8, data_reg=0x00)
        self.crc_reg = 0x00

        # Initialize data buffers building and sending packets in form of byte arrays
        self.data_buffer = bytearray(0)
        self.cmd_byte_arr = bytearray(0)
        self.len_byte_msb = 0xA0

    def __repr__(self):
        serial_str = f"----------------------------------------------------------------------------------------------\n"
        serial_str += f"Serial Port Settings\n"
        serial_str += f"{self.x4_serial.serial.__repr__()}, data_buffer={self.data_buffer}\n"
        crc_str = f"----------------------------------------------------------------------------------------------\n"
        crc_str += f"CRC Generator Settings\n"
        crc_str += f"CRC(Poly={self.crc_gen.poly}, Init={self.crc_gen.crc_init}, Reg={self.crc_reg})\n"
        cmd_str = f"----------------------------------------------------------------------------------------------\n"
        cmd_str += f"X4 Commands: \n{self.x4_cmds.__repr__()}\n"
        cmd_str += f"----------------------------------------------------------------------------------------------\n"
        out_str = serial_str + crc_str + cmd_str
        return out_str

    def open_port(self, verbose=False):
        if not self.x4_serial.serial.is_open:
            try:
                self.x4_serial.serial.open()
            except:
                print(f'X4 SERIAL PORT Configured in x4_serial_port.yml NOT FOUND...')
                print(f'AVAILABLE PORTS: \n')
                ports = list(list_ports.comports())
                for p in ports:
                    print(p.device)
        if verbose:
            print(f'X4 SERIAL PORT {self.x4_serial.serial.port} OPEN')

    def close_port(self, verbose=False):
        if self.x4_serial.serial.is_open:
            self.x4_serial.serial.close()
        if verbose:
            print(f'X4 SERIAL PORT {self.x4_serial.serial.port} CLOSED')

    def build_cmd_bytearr(self, cmd: x4Cmd, data: List[int]):
        """
        :param cmd: Command object used to build byte array from attributes provided in yml
        :param data: Data to be sent in format of list of integers corresponding to bytes i.e. [BYTE1, BYTE2, ...]
                     length of data must be equal to cmd.len_byte - 2                          [MSB,      ....LSB]
        :return: packed bytearray of command to be sent over serial
        """
        # Check if data length matches the expected length
        if len(data) != cmd.len - 2:
            print(f'ERR: Data length {len(data)} does not match command length {cmd.len - 2}')
            return None
        cmd_byte_arr = bytearray()
        cmd_byte_arr.append(cmd.len_byte)
        cmd_byte_arr.append(cmd.cmd_code)
        for byte in data:
            cmd_byte_arr.append(byte)
        crc_reg = self.crc_gen.generate_crc(data_bytes=cmd_byte_arr, verbose=False)
        self.crc_reg = crc_reg
        cmd_byte_arr.append(crc_reg)
        return cmd_byte_arr

    def read_x4(self, rd_cmd_byte_arr: bytearray, verbose=False):
        """
        :param rd_cmd_byte_arr: byte array of a read command to be sent over serial to x4
        :param verbose: If True, print the byte array being sent to console
        :return: response from x4 read over serial
        """
        # Check if the serial port is open before attempting to write
        if self.x4_serial.serial.is_open:
            self.x4_serial.serial.reset_input_buffer()    # Clear old junk BEFORE writing
            self.x4_serial.serial.write(rd_cmd_byte_arr)  # Write rd command to x4
            sleep(0.1)                                    # Let the device respond
            x4_response = self.x4_serial.serial.read(2)
            sleep(0.1)
            if verbose:
                print(f'Command sent: {(rd_cmd_byte_arr[:2])}')
                print(f'CRC: {rd_cmd_byte_arr[2:]}')
            return x4_response
        else:
            print(f'ERR: Serial port is not open')
            return None

    def send_rd_status_cmd(self, verbose=False):
        """
        :return: status read from x4 (format tbd)
        """
        self.data_buffer.clear()  # Clear old junk BEFORE writing
        rd_status_cmd = self.x4_cmds.rd_status_cmd
        rd_status_data_buffer = self.build_cmd_bytearr(cmd=rd_status_cmd, data=[])
        x4_response_status = self.read_x4(rd_cmd_byte_arr=rd_status_data_buffer, verbose=verbose)
        # Todo add decoding for raw data
        print(f"Received {len(x4_response_status)} bytes: {[f'{b:02X}' for b in x4_response_status]}")

    def send_rd_data_cmd(self):
        """
        :return: data read (format tbd)
        """
        pass

    def send_rd_version_cmd(self):
        """
        :return: version number read
        """
        pass

    def send_wr_move_rel_cmd(self, eev_sel=0x00, rel_position_change=0x0000):
        """
        :param eev_sel: EEV selection (1-4 inclusive)
        :param position_change: Signed 16 bit data for relative eev position
        :return: tbd
        """
        pass

    def send_wr_move_abs_cmd(self, eev_sel=0x00, abs_position_change=0x0000):
        """
        :param eev_sel: EEV selection (1-4 inclusive)
        :param abs_position_change: Unsigned 16 bit data for absolute eev position
        :return: tbd
        """
        pass

    def send_wr_move_home_cmd(self, eev_sel=0x00):
        """
        :param eev_sel: EEV selection (1-4 inclusive)
        :return: tbd
        """
        pass

    def send_wr_self_test_cmd(self, eev_sel=0x00):
        """
        :param eev_sel: EEV selection (1-4 inclusive)
        :return: tbd
        """
        pass

    def send_wr_solenoid_enable_cmd(self, sol_rly_sel=0x00):
        """
        :param sol_rly_sel: Which solenoid relay to enable (inclusive 1-4)
        :return: tbd
        """
        pass

    def send_wr_solenoid_disable_cmd(self, sol_rly_sel=0x00):
        """
        :param sol_rly_sel: Which solenoid relay to disable (inclusive 1-4)
        :return: tbd
        """
        pass

    def send_wr_eev_set_position_cmd(self, eev_sel=0x00, eev_position=0x0000):
        """
        :param eev_sel: EEV selection (1-4 inclusive)
        :param eev_position: Sets eev position without moving
        :return: tbd
        """
        pass

    def send_wr_fan_pwm_cmd(self, pin_sel=0x00, duty_cycle=0x0000):
        """

        :param pin_sel: PWM output_monitors pin selection (either 1 or 2)
        :param duty_cycle: 2 bytes indicating duty cycle between 1 and 1000
        :return: tbd
        """
        pass

    def send_wr_heater_relay_enable_cmd(self, htr_rly_sel=0x00):
        """

        :param htr_rly_sel: Which heater relay to enable (1 or 2)
        :return: tbd
        """
        pass

    def send_wr_heater_relay_disable_cmd(self, htr_rly_sel=0x00):
        """
        :param htr_rly_sel: Which heater relay to enable (1 or 2)
        :return: tbd
        """
        pass

    def send_wr_all_stop_cmd(self):
        """
        Resets selected outputs to defualt state. EEV drives not touched
        :return: n/a
        """
        pass

    def send_reset_cmd(self):
        """
        Resets the x4
        :return: n/a
        """
        pass


if __name__ == "__main__":
    pass
