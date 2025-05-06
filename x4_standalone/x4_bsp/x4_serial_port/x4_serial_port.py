import serial


class x4SerialPort:
    def __init__(self, **kwargs):
        """
        :param com_port: COM port to use for serial communication
        :param baudrate: Baudrate to use for serial communication
        """
        self.serial = serial.Serial(
            port=kwargs['com_port'] if 'com_port' in kwargs else 'COM3',
            baudrate=kwargs['baudrate'] if 'baudrate' in kwargs else 9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        self.name = 'x4_serial_port'

