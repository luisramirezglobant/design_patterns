from abc import ABC, abstractmethod
from random import choices


class IPrize(ABC):
    @abstractmethod
    def get_info():
        pass


class CommonPrize(IPrize):
    def get_info(self):
        return "common prize :)"


class SpecialPrize(IPrize):
    def get_info(self):
        return "special prize :D"


class RarePrize(IPrize):
    def get_info(self):
        return "rare prize :O"


class SuperRarePrize(IPrize):
    def get_info(self):
        return "super rare prize >:O"


class PrizeFactory:
    @staticmethod
    def get_prize(prize_category):
        factory_methods = {
            "common": CommonPrize,
            "special": SpecialPrize,
            "rare": RarePrize,
            "super rare": SuperRarePrize,
        }
        return factory_methods[prize_category]()


if __name__ == "__main__":
    selection = choices(
        ["common", "special", "rare", "super rare"], weights=(50, 25, 10, 5)
    )[0]
    prize = PrizeFactory().get_prize(selection)
    print(prize.get_info())
