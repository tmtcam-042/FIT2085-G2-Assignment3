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
        """ Creates a potion with corresponding potion type,name and buy price and
        initialises the quantity of it to 0
        :complexity: O(1) where returning a tuple is constant
        """
        return Potion(potion_type, name, buy_price, 0)

    @classmethod
    def good_hash(cls, potion_name: str, tablesize: int) -> int:
        """
        Method that hashes a position for a given string and tablesize. This uses
        a universal hash method to prevent collisions and conflicts
        :complexity: O(1) where char is the first letter of the string
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
        Method that hashes a position for a given string and tablesize. This uses
        a bad hash method to hash a key where lots of collisions and conflicts can occur.
        :complexity: O(1) where the first letter of the string is constant
        """
        return ord(potion_name[0]) % tablesize


