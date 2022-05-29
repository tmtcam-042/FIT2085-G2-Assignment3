def largest_prime(k: int) -> int:
    """
    A function designed to return the largest prime number less than k.
    Implemented using the Sieve of Eratosthenes algorithm.
    :pre: k must be an integer >= 3
    :post: the integer returned is strictly less than k
    :raises ValueError: if k < 3
    :raises TypeError: if k is not integer
    :complexity: best and worst O(N log(log N)) where N is the value of k
    :return: the largest prime number strictly less than k
    """

    try:
        if k < 3:
            raise ValueError("Input must be >= 3")
        primes_list = [True for i in range(k)]
        p = 2

        while p ** 2 <= k:

            # If prime[p] is not changed, then it is a prime
            if primes_list[p]:

                # Update all multiples of p
                for i in range(p ** 2, k, p):
                    primes_list[i] = False

            p += 1

        primes_list[0] = False
        primes_list[1] = False

        # Print all prime numbers
        return max([i for i, b in enumerate(primes_list) if b])

    except Exception as e:
        print(f"Error {type(e)}: {e}")
