class Car:
    def __init__(self, name):
        self.name = name
        self.gears = ["N", "1", "2", "3", "4", "5", "6", "R"]
        self.speed = 0
        self.gear = "N"
    
    def changeGear(self, gear):
        if (gear in self.gears):
            self.gear = gear
            print(f"Car {self.name} is in gear {self.gear}")
    
    def accelerate(self):
        if (self.gear == "N"):
            print(f"Error: Car {self.name} is in gear N")
        else:
            self.speed += 1
            print(f"Car {self.name} is accelerating")


# We are making a subclass over a car

class SportsCar(Car):
    def __init__(self, name):
        super().__init__(name)
        self.turbos = [2, 3]
    """
    The problem is that we are re implementing the method
    and changing the original parameters.
    """  
    def accelerate(self, turbo):
        if (self.gear == "N"):
            print("Error: Car %s is in gear N" % self.name)
        else:
            if (turbo in self.turbos):
                self.speed += turbo
                print("Car %s is accelerating with turbo %d" % (self.name, turbo))

if __name__ == '__main__':
    
    # The original car
    car = Car('BMW')
    car.changeGear("1")
    car.accelerate()

    # We can't replace Car with SportsCar without breaking changes
    # If we let accelerate with the original parameters, the program crashes:
    autoCar = SportsCar('Audi')
    autoCar.changeGear("1")
    autoCar.accelerate()