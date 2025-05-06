from crc_generator import CrcGenerator
"""
              ********** Byte alignment of CRC-7 polynomial: (0x65 << 1) + 1 = 0xCB ********** 
    We left shift 7 bit polynomial by 1 and add 1 to create an 8 bit odd parity polynomial from the standard CRC-7
"""

# Example from Application Note
print(f'--------------------------------------------------------------------------------------------------------------')
print(f'EX From STM32 CRC Peripheral Application Note (DATA = 0xC1, POLY = 0x3B):')
data_buffer = bytearray()
data_buffer.append(0xC1)
stm32_hw_crc = CrcGenerator(data_buffer=data_buffer, poly=0xCB, crc_init=0xFF)
stm32_hw_crc._use_stm32_periph = True
stm32_hw_crc.generate_crc(data_bytes=data_buffer, verbose=True)
print(f'CRC OUT  : {hex(stm32_hw_crc.crc_reg)}\n'
      f'EXPECTED : 0x4c')
data_buffer.clear()
print(f'--------------------------------------------------------------------------------------------------------------')
print(f'RD STATUS CMD = 0xA201 w/STM32 CRC Peripheral HW:')
cmd_bytes = [0xA2, 0x01]
for byte in cmd_bytes:
      data_buffer.append(byte)
stm32_hw_crc = CrcGenerator(data_buffer=data_buffer, poly=0xCB, crc_init=0xFF)
stm32_hw_crc._use_stm32_periph = True
crc_cmd = stm32_hw_crc.generate_crc(data_bytes=data_buffer, verbose=True)
print(f'CRC CMD = {hex(cmd_bytes[0])[2:]}{hex(cmd_bytes[1])[2:]} = {hex(crc_cmd)}\n')
data_buffer.clear()
print(f'--------------------------------------------------------------------------------------------------------------')
print(f'RD STATUS CMD = 0xA201 CRC Calculation from firmware team:')
cmd_bytes = [0xA2, 0x01]
for byte in cmd_bytes:
      data_buffer.append(byte)
sw_crc8 = CrcGenerator(data_buffer=data_buffer, poly=0x65, crc_init=0x00)
sw_crc8._use_stm32_periph = False
crc_cmd = sw_crc8.generate_crc(data_bytes=data_buffer, verbose=True)
print(f'CRC (CMD = {hex(cmd_bytes[0])[2:]}{hex(cmd_bytes[1])[2:]}) = {hex(crc_cmd)}\n')
print(f'EXPECTED: 0xa5')
print(f'--------------------------------------------------------------------------------------------------------------')

