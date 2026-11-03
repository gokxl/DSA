"""
================================================================================
PROBLEM: Count Primes (LeetCode 204)
Difficulty: Medium | Pattern: Math / Sieve of Eratosthenes
================================================================================

PROBLEM STATEMENT:
Given an integer n, return the number of prime numbers that are strictly less
than n.

EXAMPLES:
    Input: n = 10
    Output: 4
    Explanation: Primes below 10 are 2, 3, 5, 7.

    Input: n = 0
    Output: 0

    Input: n = 1
    Output: 0

CONSTRAINTS:
- 0 <= n <= 5 * 10^6

================================================================================
"""


# ============================================================================
# SOLUTION 1: Sieve of Eratosthenes (Optimal)
# ============================================================================
def countPrimes(n: int) -> int:
    """
    Mark multiples of each prime as composite. Any number left marked prime
    truly is prime.

    Two key optimizations:
      - Start crossing out from p*p (smaller multiples already handled).
      - Only sieve p up to sqrt(n).

    Time:  O(n log log n)
    Space: O(n)
    """
    if n < 3:
        return 0

    is_prime = [True] * n
    is_prime[0] = is_prime[1] = False

    p = 2
    while p * p < n:
        if is_prime[p]:
            # Cross out multiples starting at p*p.
            for multiple in range(p * p, n, p):
                is_prime[multiple] = False
        p += 1

    return sum(is_prime)


# ============================================================================
# SOLUTION 2: Sieve with Slice Assignment (Pythonic, faster in practice)
# ============================================================================
def countPrimes_fast(n: int) -> int:
    """
    Same sieve, but zero out multiples with a slice assignment, which runs in
    optimized C under the hood.

    Time:  O(n log log n)
    Space: O(n)
    """
    if n < 3:
        return 0

    is_prime = [True] * n
    is_prime[0] = is_prime[1] = False

    for p in range(2, int(n**0.5) + 1):
        if is_prime[p]:
            is_prime[p * p : n : p] = [False] * len(range(p * p, n, p))

    return sum(is_prime)


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    print(f"n = 10  -> {countPrimes(10)}")   # 4
    print(f"n = 0   -> {countPrimes(0)}")    # 0
    print(f"n = 1   -> {countPrimes(1)}")    # 0
    print(f"n = 2   -> {countPrimes(2)}")    # 0
    print(f"n = 100 -> {countPrimes(100)}")  # 25
    assert countPrimes(100) == countPrimes_fast(100)


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. WHY SIEVE BEATS TRIAL DIVISION:
   Checking each number for primality is O(n * sqrt(n)). The sieve shares work
   across numbers and runs in near-linear O(n log log n).

2. THE TWO OPTIMIZATIONS TO MENTION:
   - Start at p*p: every smaller multiple of p already had a smaller prime
     factor, so it was crossed out earlier.
   - Sieve only to sqrt(n): any composite below n has a factor <= sqrt(n).

3. STRICTLY LESS THAN n:
   The array has indices 0..n-1, so we naturally count primes below n. Watch
   this off-by-one -- a classic interviewer trap.

4. HOW TO EXPLAIN IT:
   Define primality clearly (> 1, divisible only by 1 and itself), handle n<3
   up front, then build the sieve. Narrate the p*p optimization -- it is the
   detail that distinguishes a prepared candidate.
"""
