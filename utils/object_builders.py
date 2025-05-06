from abc import ABC, abstractmethod
import yaml


class ObjectBuilder(ABC):
    @abstractmethod
    def build(self, base_path: str, config_path: str):
        pass


class TestBenchBuilder(ObjectBuilder):
    def __init__(self):
        pass

    def build(self, base_path: str, config_path: str):
        # Get the attributes of the test bench components from the YAML file
        absolute_path = base_path + config_path
        with open(absolute_path, 'r') as file:
            component_data = yaml.safe_load(file)
            component_definitions = component_data['components']
            component_builder = ComponentBuilder()
            # Parse the YAML file and create instances of each x4 component
            component_obj_dict = {}
            for component_str in component_definitions.keys():
                constructor_name = component_definitions[component_str]['class_name']
                component_config_path = component_definitions[component_str]['config_path']
                component_obj = component_builder.build(base_path=base_path, config_path=component_config_path)
                component_obj_dict[constructor_name] = component_obj
            return component_obj_dict


class ComponentBuilder(ObjectBuilder):
    def __init__(self):
        pass
    
    def build(self, base_path: str, config_path: str):
        """
        :param attribute_config_path: 
        :return: 
        """
        # Get the byte attributes of the x4 commands from the YAML file
        absolute_path = base_path + config_path
        with open(absolute_path, 'r') as file:
            attribute_data = yaml.safe_load(file)
            attribute_dict = attribute_data['attributes']
        return attribute_dict
    