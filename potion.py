from primes import largest_prime


class Potion:

    def __init__(self, potion_type: str, name: str, buy_price: float, quantity: float) -> None:
        """
        Init method to initialise Potion Objects
        """
        self.potion_type = potion_type
        self.name = name
        self.buy_price = buy_price
        self.quantity = quantity

    @classmethod
    def create_empty(cls, potion_type: str, name: str, buy_price: float) -> 'Potion':
        """ Creates a potion with corresponding potion type,name and buy price and initialises the quantity of it to
        0
        """
        return Potion(potion_type, name, buy_price, 0)

    @classmethod
    def good_hash(cls, potion_name: str, tablesize: int) -> int:
        """
        Method that hashes a position for a given string and tablesize. This uses a universal hash method to prevent
        collisions and conflicts
        """
        value = 0
        a = largest_prime(52459)
        b = largest_prime(27183)
        for char in potion_name:
            value = (ord(char) + a * value) % tablesize
        a = a * b % (tablesize - 1)
        return value

    @classmethod
    def bad_hash(cls, potion_name: str, tablesize: int) -> int:
        """
        Method that hashes a position for a given string and tablesize. This uses a bad hash method to hash a key where
        lots of collisions and conflicts can occur.
        """
        return ord(potion_name[0]) % tablesize

    def get_name(self) -> str:
        return self.name


if __name__ == '__main__':
    health = Potion("health", "blue barrel", 60, 4)
    hashnum = health.bad_hash("blue barrel", 3)
    hashnum1 = health.good_hash("blue barrel", 162)
    print(hashnum1)
