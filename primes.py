def largest_prime(k: int) -> int:
    """
    for i = 2, 3, 4, ..., not exceeding √n do
    if A[i] is true
        for j = i2, i2+i, i2+2i, i2+3i, ..., not exceeding n do
            set A[j] := false

    return all i such that A[i] is true.
    """

    primes_list = [True for i in range(k + 1)]
    p = 2

    while p * p <= k:

        # If prime[p] is not changed, then it is a prime
        if primes_list[p]:

            # Update all multiples of p
            for i in range(p ** 2, k + 1, p):
                primes_list[i] = False

        p += 1

    primes_list[0] = False
    primes_list[1] = False
    # Print all prime numbers
    return max([i for i, b in enumerate(primes_list) if b])


if __name__ == "__main__":
    print(largest_prime(20))
