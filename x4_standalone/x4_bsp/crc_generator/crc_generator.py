class CrcGenerator:
    """
    Class to generate CRC values for data packets using the STM32 CRC peripheral or software implementation.
    """
    def __init__(self, **kwargs): # todo figure out cuz this is better dynamically
        """
        :param poly: Polynomial used to generate crc
        :param crc_init: Initial value of crc reg
        """
        self.poly = kwargs['poly'] if 'poly' in kwargs else 0x65
        self.crc_init = kwargs['crc_init'] if 'crc_init' in kwargs else 0x00
        self.crc_reg = self.crc_init
        self.max_val = pow(2, 8) - 1
        self.crc_calc_dict = {}
        self._use_stm32_periph = False
        self.byte_ctr = 0
        self.data_reg = 0x00
        self.data_buffer = bytearray(0)
        self.name = 'crc_gen'

    def generate_crc(self, data_bytes: bytearray, verbose=False) -> int:
        """
        :param data_bytes: Data to calculate CRC on
        :return: CRC value

        Uses algorithm described in STM32 CRC unit applicaion note:
        https://www.st.com/resource/en/application_note/an4187-using-the-crc-peripheral-on-stm32-microcontrollers-stmicroelectronics.pdf
        """

        if len(data_bytes) is not None:
            if self._use_stm32_periph:
                crc = self._stm32_hw_crc(data_buffer=data_bytes, verbose=verbose)
            else:
                crc = self._sw_crc8(data_buffer=data_bytes, verbose=verbose)
            self.crc_reg = crc  # Copy result to static memory register of class instance
            return crc
        else:
            print(f'ERR NO DATA SUPPLIED')
            return -1
        
    def _clear_data_buffer(self):
        self.data_buffer.clear()
    
    def _stm32_hw_crc(self, data_buffer: bytearray, verbose=False):
        """
        Function to emulate the STM32 CRC peripheral Hardware
        :param data_buffer: Data to calculate CRC on
        :param verbose: If True, print debug information
        :return: Calculated CRC value
        """

        crc_reg = self.crc_init  # Init crc with class attribute of the initial crc register value
        for (i,byte) in enumerate(data_buffer):
            # Initialize current byte calculation with current data byte
            data_reg = byte
            crc_reg ^= data_reg
            if verbose:
                print(f'Data Byte: {hex(byte)}')
                print(f'CRC  Init: {hex(crc_reg)}')
            # Todo: track dictionary of caluclated CRCs for each processed byte
            for _ in range(8):
                mask = -(crc_reg & 0x80) >> 7  # mask = 0xFF if bit7 is set, else 0x00
                crc_reg = (crc_reg << 1) & 0xFF  # ensure crc stays 8-bit
                crc_reg ^= (self.poly & mask)
                if verbose:
                    print(f'CRC Step{_}: {hex(crc_reg)}')
        return crc_reg

    def _sw_crc8(self, data_buffer: bytearray, verbose=False):
        """
        Function that implements the CRC algorithm implemented by development team in software
        :param data_buffer: Data to calculate CRC on
        :param verbose: If True, print debug information
        :return: Calculated CRC value
        """

        crc_reg = self.crc_init  # Initialize CRC register for current byte calculation
        for (_,byte) in enumerate(data_buffer):
            data_reg = byte
            crc_reg ^= data_reg
            if verbose:
                print(f'Data Byte: {hex(byte)}')
                print(f'CRC  Init: {hex(crc_reg)}')
            # Todo: track dictionary of caluclated CRCs for each processed byte
            for _ in range(8):
                mask = -(crc_reg & 0x80) >> 7  # mask = 0xFF if bit7 is set, else 0x00
                crc_reg = (crc_reg << 1) & 0xFF  # ensure crc stays 8-bit
                crc_reg ^= (self.poly & mask)
                if verbose:
                    print(f'CRC Step{_}: {hex(crc_reg)}')
        return crc_reg

    # Possible utility function if data needs to be reversed in peripheral hardware case
    def rev_data(self, data=0x00):
        """
        Function to reverse the bits of a data word
        :param data: Data to be reversed
        :return: Integer value of reversed data
        """
        bin_str = bin(data)[2:]
        data_len = len(bin_str)
        rev_bin_arr = ['0'] * data_len
        rev_data = 0
        for (i, ch) in enumerate(bin_str):
            # rev_idx = self.data_len - i
            rev_idx = len(bin_str) - 1 - i
            rev_bin_arr[rev_idx] = bin_str[i]

        bin_idx = data_len - 1
        for b in rev_bin_arr:
            rev_data += pow(2, bin_idx) * int(b)
            bin_idx -= 1

        return rev_data