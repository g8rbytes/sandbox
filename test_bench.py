import os
from x4_test_bench.x4_standalone.x4_bsp.x4_bsp import *
from x4_test_bench.utils.object_builders import *


class x4TestBench:
    def __init__(self, **kwargs):
        """
        :param: x4_bsp: Lists configuration path for x4Bsp class which is dynamically configured from YAML file
        :param x4_bsp_master: Instance of x4Bsp class used for driving serial communication with the x4 board
        :param x4_bsp_slave: Instance of x4Bsp class used for receiving serial communication from master
        """
        pass

    def __repr__(self):
        out_str = f"----------------------------------------------------------------------------------------------\n"
        out_str += "X4 Test Bench Configurations: \n"
        for key, value in self.__dict__.items():
            out_str += value.__repr__()
        out_str += f"----------------------------------------------------------------------------------------------\n"
        return out_str


def build_x4_test_bench():
    """
    Initialize the test bench by parsing the YAML file in test_bench.yml and creating instances of each component
    :return:
    """
    # Todo: environment files for overarching path either here or in builder class
    # Get the attributes of the test bench components from the YAML file
    config_path = '/test_bench.yml'
    # Parse the YAML file and create instances of each x4 component
    base_path = os.path.dirname(os.path.abspath(__file__))
    test_bench_builder = TestBenchBuilder()
    x4_test_bench_component_dict = test_bench_builder.build(base_path=base_path, config_path=config_path)
    component_dict = {}
    for constructor, attributes_dict in x4_test_bench_component_dict.items():
        x4_test_bench_component = globals()[constructor](**attributes_dict)
        component_key = x4_test_bench_component.name
        component_dict[component_key] = x4_test_bench_component
    x4_bsp_obj = x4Bsp(**component_dict)
    return x4_bsp_obj
    # Todo: Add shorter aliasing to make object component/attribute access more readable


if __name__ == "__main__":
    x4_bsp_master = build_x4_test_bench()
    print(f'{x4_bsp_master.__repr__()}')
    print(f'RD STATUS COMMAND DEMO:')
    x4_bsp_master.send_rd_status_cmd(verbose=True)
