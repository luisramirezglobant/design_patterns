
class Class:
    def __init__(self, name: str) -> None:
        self.name = name
        self.attributes = []

    def __str__(self):
        response = f"Class {self.name}:\n"
        if self.attributes:
            for attribute in self.attributes:
                response += f"\t{attribute.name} = {attribute.value}\n"
        else:
            response += f"\tpass"
        return response

class Attribute:
    def __init__(self, name: str, value: str) -> None:
        self.name = name
        self.value = value

class ClassBuilder:
    def __init__(self, class_name: str) -> None:
        self.class_obj = Class(class_name)
    
    def add_attribute(self, name: str, value: str):
        self.class_obj.attributes.append(Attribute(name, value))

    def build(self):
        return self.class_obj

class EmptyClassBuilder(ClassBuilder):
    def __init__(self, class_name: str):
        super().__init__(class_name=class_name)

class PatermetersClassBuilder(ClassBuilder):
    def __init__(self, class_name: str):
        super().__init__(class_name=class_name)

    def build(self):
        self.add_attribute("nombre", "Jeremias")
        self.add_attribute("edad", "2000")
        return super().build()

class Director:
    def __init__(self, builder: ClassBuilder):
        self.builder = builder
    
    def build_class(self):
        self.builder.build()
        return self.builder.class_obj
    
empty_builder = EmptyClassBuilder("EmptyClass")
empty_director = Director(empty_builder)
empty_class = empty_director.build_class()
print(empty_class)

parameter_class_builder = PatermetersClassBuilder("ParameterClass")
parameter_class_director = Director(parameter_class_builder)
parameter_class = parameter_class_director.build_class()
print(parameter_class)