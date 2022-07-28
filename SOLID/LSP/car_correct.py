from abc import ABC, abstractmethod

class Car(ABC):
    @abstractmethod
    def __init__(self, name):
        self.name = name
        self.gears = ["N", "1", "2", "3", "4", "5", "6", "R"]
        self.speed = 0
        self.gear = "N"

    def changeGear(self, gear):
        if (gear in self.gears):
            self.gear = gear
            print("Car %s is in gear %s" % (self.name, self.gear))

    def accelerate(self):
        if (self.gear == "N"):
            print("Error: Car %s is in gear N" % self.name)
        else:
            self.speed += 1
            print("Car %s is accelerating" % self.name)

class RegularCar(Car):
    def __init__(self, name):
        super().__init__(name)

"""
Using an abstract class (can't be instantiated).
We are able to create differnt types of cars. One of them 
is making modifications to the original Car, by adding a turbo
attribute and a method for turbo acceleration
"""
class SportsCar(Car):
    def __init__(self, name):
        super().__init__(name)
        self.turbos = [2, 3]

    def turboAccelerate(self, turbo):
        if (self.gear == "N"):
            print("Error: Car %s is in gear N" % self.name)
        else:
            if (turbo in self.turbos):
                self.speed += turbo
                print("Car %s is accelerating with turbo %d" % (self.name, turbo))

if __name__ == '__main__':
    
    car = RegularCar('BMW')
    car.changeGear("1")
    car.accelerate()

    autoCar = SportsCar('Audi')
    autoCar.changeGear("1")
    autoCar.turboAccelerate(2)

"""We are not breaking the LSP since we are not changing the function signature
by adding other elements since Car can't be instantiated, therefor can't be replaced"""