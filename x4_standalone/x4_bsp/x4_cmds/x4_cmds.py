class x4Cmd:
    """
    Class to hold command attributes for each command
    """
    def __init__(self, **kwargs):
        """
        :param name: Name of command
        :param len: Length of command in bytes
        :param len_byte: Byte representation of length of command
        :param cmd_code: Byte representation of command code
        """
        self.name = kwargs['name'] if 'name' in kwargs else ''
        self.len = kwargs['len'] if 'len' in kwargs else 0x00
        self.len_byte = kwargs['len_byte'] if 'len_byte' in kwargs else 0x00
        self.cmd_code = kwargs['cmd_code'] if 'cmd_code' in kwargs else 0x00

    def __repr__(self):
        out_str = f'Length: {hex(self.len_byte)}, Code: {hex(self.cmd_code)}'
        return out_str


class x4Cmds:
    """
    Class to hold all command objects so we can access and format commands dynamically within X4 BSP class
    """
    def __init__(self, **kwargs):
        """
        :param kwargs: Dict in form of {cmd_str: x4Cmd_obj}
        """
        for cmd_str, cmd_attributes in kwargs.items():
            cmd_obj = x4Cmd(**cmd_attributes)
            self.__setattr__(cmd_str, cmd_obj)
        self.name = 'x4_cmds'

    def __repr__(self):
        cmd_str = ''
        for k,v in self.__dict__.items():
            cmd_description = v.__repr__()
            cmd_str += f'{k}: {cmd_description}\n'
        return cmd_str

