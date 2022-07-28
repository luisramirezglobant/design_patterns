from abc import ABC, abstractmethod

class Movable(ABC):
    @abstractmethod
    def go(self):
        pass

# The flyable vehicle can also go, we are adding this functionality
# to the design of this class
class Flyable(Movable):
    @abstractmethod
    def fly(self):
        pass

class Aircraft(Flyable):
    def go(self):
        print("Taxiing")

    def fly(self):
        print("Flying")

class Car(Movable):
    def go(self):
        print("Going")