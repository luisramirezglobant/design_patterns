from enum import Enum

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

class Size(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3


class Specification:
    # Empty classes works as interfaces
    def is_satisfied(self, item):
        pass

    # overload of & operator
    def __and__(self, other):
        return AndSpecification(self, other)

class Product:
    def __init__(self, name, color, size):
        self.name = name
        self.color = color
        self.size = size

class Filter:
    # general porpouse filter
    # filter from an Iterable (items) and certain condition (specification)
    def filter(self, items, spec):
        pass

class ColorSpecification(Specification):
    def __init__(self, color):
        self.color = color

    def is_satisfied(self, item):
        return item.color == self.color

class SizeSpecification(Specification):
    def __init__(self, size):
        self.size = size

    def is_satisfied(self, item):
        return item.size == self.size

class AndSpecification(Specification):
    # Combinator: structure that combine other structures
    def __init__(self, *args):
        self.args = args

    def is_satisfied(self, item):
        return all(map(
            lambda spec: spec.is_satisfied(item), self.args))

class BetterFilter(Filter):
    # we are implementing the methods in Filter with out touching 
    # the existing code
    def filter(self, items, spec):
        for item in items:
            if spec.is_satisfied(item):
                yield item

apple = Product('Apple', Color.GREEN, Size.SMALL)
tree = Product('Tree', Color.GREEN, Size.LARGE)
house = Product('House', Color.BLUE, Size.LARGE)

products = [apple, tree, house]

bf = BetterFilter()

print('Green products:')
green = ColorSpecification(Color.GREEN)
for p in bf.filter(products, green):
    print(f' - {p.name} is green')

print('Large products:')
large = SizeSpecification(Size.LARGE)
for p in bf.filter(products, large):
    print(f' - {p.name} is large')

# without & overload
# large_blue = AndSpecification(large, ColorSpecification(Color.BLUE))

# with & overload
print('Large blue items:')
large_blue = large & ColorSpecification(Color.BLUE)
for p in bf.filter(products, large_blue):
    print(f' - {p.name} is large and blue')
