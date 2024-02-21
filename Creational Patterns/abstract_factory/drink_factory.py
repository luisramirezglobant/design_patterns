from abc import ABC, abstractmethod

class AbstractDrinkFactory(ABC):
    """
    This class handles the creation of the group of products 
    that will be created together
    """
    @abstractmethod
    def make_ingredient():
        pass
    
    @abstractmethod
    def make_complement():
        pass

class AbstractIngredient(ABC):
    # @abstractmethod
    def __init__(self, kind: str, amount: int) -> None:
        self.kind = kind
        self.amount = amount

    @abstractmethod
    def prepare(self):
        pass

    def __str__(self):
        return f"kind: {self.kind} {self.amount} grs"

class AbstractComplement(ABC):
    def __init__(self, kind: str, amount: int) -> None:
        self.kind = kind
        self.amount = amount

# class IngredientFactory:

class Coffee(AbstractIngredient):
    # def __init__(self, kind: str, amount: int) -> None:
    #     super().__init__(kind=kind, amount=amount)

    def prepare(self):
        print(f"boil water, pour the coffe")
    
    def __str__(self):
        return f"Coffe {super().__str__()}"

class Whisky(AbstractIngredient):
    def __init__(self, kind: str, amount: int) -> None:
        super().__init__(kind=kind, amount=amount)

    def prepare(self):
        print(f"straight to a glass")
    
    def __str__(self):
        return f"Whisky {super().__str__()}"

class IngredientFactory:
    @staticmethod
    def get_ingredient(ingredient: str):
        ingredients = {
            "coffee": Coffee,
            "whisky": Whisky
        }
        try:
            return ingredients[ingredient]
        except KeyError:
            raise KeyError(f"{ingredient} is not in the list of valid ingredients")

# Calling the factory method for coffee
coffee: Coffee = IngredientFactory.get_ingredient("coffee")("Arabiga", 15)
print(coffee)

# Calling the factory method to throw an error
# ingredient = IngredientFactory.get_ingredient("random")("Random", 0)

