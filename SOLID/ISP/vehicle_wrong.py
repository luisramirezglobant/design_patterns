from abc import ABC, abstractmethod

class Vehicle(ABC):
    @abstractmethod
    def go(self):
        pass

    @abstractmethod
    def fly(self):
        pass

class Aircraft(Vehicle):
    def go(self):
        print("Taxiing")

    def fly(self):
        print("Flying")

"""
In the design of the Car class, fly() should be implemented from Vehicle,
but Car doesn't fly. Therefor violates ISP since we don't need to implement
interfaces that we don't need. In this case implementing an unsued method
"""
class Car(Vehicle):
    def go(self):
        print("Going")

    def fly(self):
        raise Exception('The car cannot fly')