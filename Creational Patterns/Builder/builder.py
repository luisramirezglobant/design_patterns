class Car:
    def __init__(self):
        self.__wheels = None
        self.__engine = None
        self.__body = None

    def set_wheels(self, wheels):
        self.__wheels = wheels

    def set_engine(self, engine):
        self.__engine = engine

    def set_body(self, body):
        self.__body = body

    def __str__(self):
        return f"{self.__wheels} wheels, {self.__engine} engine, {self.__body} body"


class Builder:
    def get_wheels(self):
        pass

    def get_engine(self):
        pass

    def get_body(self):
        pass


class Director:
    def __init__(self, builder: Builder):
        self.__builder = builder

    def construct_car(self):
        self.__builder.get_wheels()
        self.__builder.get_engine()
        self.__builder.get_body()


class CarBuilder(Builder):
    def __init__(self):
        self.car = Car()

    def get_wheels(self):
        self.car.set_wheels("4")

    def get_engine(self):
        self.car.set_engine("V8")

    def get_body(self):
        self.car.set_body("Sedan")


class SUVBuilder(Builder):
    def __init__(self):
        self.car = Car()

    def get_wheels(self):
        self.car.set_wheels("6")

    def get_engine(self):
        self.car.set_engine("V6")

    def get_body(self):
        self.car.set_body("SUV")


if __name__ == "__main__":
    car_builder = CarBuilder()
    suv_builder = SUVBuilder()

    director = Director(car_builder)
    director.construct_car()
    car = car_builder.car
    print("Car: ", car)

    director = Director(suv_builder)
    director.construct_car()
    suv = suv_builder.car
    print("SUV: ", suv)
