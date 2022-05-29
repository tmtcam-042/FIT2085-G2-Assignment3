from typing import Generator


def lcg(modulus: int, a: int, c: int, seed: int) -> Generator[int, None, None]:
    """Linear congruential generator."""
    while True:
        seed = (a * seed + c) % modulus
        yield seed


class RandomGen:
    """
    Class that returns a randomly generated number
    """
    def __init__(self, seed: int = 0) -> None:
        self.seed = seed
        self.randgen = lcg(pow(2, 32), 134775813, 1, seed)

    def randint(self, k: int) -> int:
        """
        returns a random integer
        :param k: positive non-zero integer
        :return: random number in range (1,k) inclusive
        :complexity: O(N) where N is the length of the randlist
        """
        if k == 0:
            return 0
        randlist = []
        for i in range(0, 5):
            binary_num = bin(next(self.randgen))  # Convert to binary
            processed_num = binary_num[2:].zfill(32)  # Remove 0b from the start
            shifted_num = processed_num[0:16]  # Grab the 16 MSB of processed_num
            randlist.append(shifted_num)

        new_num = [0 for _ in range(16)]
        for i in range(16):
            count = 0
            for j in range(len(randlist)):
                if randlist[j][i] == "1":
                    count += 1

                if count >= 3:
                    new_num[i] = "1"
                else:
                    new_num[i] = "0"

        new_num = int("".join(new_num), 2)
        output = (new_num % k) + 1
        return output
