from typing import Generator
import time


def lcg(modulus: int, a: int, c: int, seed: int) -> Generator[int, None, None]:
    """Linear congruential generator."""
    while True:
        seed = (a * seed + c) % modulus
        yield seed


class RandomGen:

    def __init__(self, seed: int = 0) -> None:
        self.seed = seed
        self.randgen = lcg(pow(2, 32), 134775813, 1, seed)
        next(self.randgen)  # To clear initial value of 1 from generator

    def randint(self, k: int) -> int:
        """

        :param k: positive non-zero integer
        :return: random number in range (1,k) inclusive
        """
        if k == 0:
            return 0
        randlist = []
        for i in range(0, 5):
            # TODO: make this O(1)
            binary_num = bin(next(self.randgen))  # Convert to binary and remove '0b' prefix
            shifted_num = binary_num[2:18]  # Grab the 16 MSB of binary_num
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


if __name__ == "__main__":
    # Random_gen = lcg(pow(2,32), 134775813, 1, 0)
    # for num in Random_gen:
    #     print(num)
    r = RandomGen(int(time.strftime('%S')))
    print(r.randint(100))
    print(r.randint(100))
    print(r.randint(100))
    print(r.randint(100))
    print(r.randint(100))
    print(r.randint(100))
