# Component Interface
class Coffee:
    def cost(self):
        pass

# Concrete Component
class SimpleCoffee(Coffee):
    def cost(self):
        return 2

# Decorator
class CoffeeDecorator(Coffee):
    def __init__(self, decorated_coffee):
        self.decorated_coffee = decorated_coffee

    def cost(self):
        return self.decorated_coffee.cost()

# Concrete Decorator
class MilkDecorator(CoffeeDecorator):
    def cost(self):
        return self.decorated_coffee.cost() + 1

# Concrete Decorator
class SugarDecorator(CoffeeDecorator):
    def cost(self):
        return self.decorated_coffee.cost() + 0.5

# Usage
coffee = SimpleCoffee()
print(coffee.cost())  # Output: 2

coffee_with_milk = MilkDecorator(coffee)
print(coffee_with_milk.cost())  # Output: 3

coffee_with_sugar_and_milk = SugarDecorator(coffee_with_milk)
print(coffee_with_sugar_and_milk.cost())