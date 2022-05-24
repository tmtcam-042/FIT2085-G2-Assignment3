def largest_prime(k: int) -> int:
    """
    for i = 2, 3, 4, ..., not exceeding √n do
    if A[i] is true
        for j = i2, i2+i, i2+2i, i2+3i, ..., not exceeding n do
            set A[j] := false

    return all i such that A[i] is true.
    """
    # A = [True for _ in range(k-1)]
    # A[0] = False
    # A[1] = False
    # for i in range(2, int(k**0.5) + 1):
    # if A[i]:
    # for j in range(i**2, k-1, i):
    # A[j] = False

    # return max([i for i, b in enumerate(A) if b])

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
