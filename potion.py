class Potion:
    
    def __init__(self, potion_type: str, name: str, buy_price: float, quantity: float) -> None:
        self.potion_type = potion_type
        self.name = name
        self.buy_price = buy_price
        self.quantity = quantity

    @classmethod
    def create_empty(cls, potion_type: str, name: str, buy_price: float) -> 'Potion':
        """"""
        raise NotImplementedError()

    @classmethod
    def good_hash(cls, potion_name: str, tablesize: int) -> int:
        """"""
        raise NotImplementedError()

    @classmethod
    def bad_hash(cls, potion_name: str, tablesize: int) -> int:
        """"""
        raise NotImplementedError()
