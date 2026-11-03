"""
================================================================================
PROBLEM: Pow(x, n) (LeetCode 50)
Difficulty: Medium | Pattern: Math / Fast Exponentiation
================================================================================

PROBLEM STATEMENT:
Implement pow(x, n), which calculates x raised to the power n (x^n).

EXAMPLES:
    Input: x = 2.00000, n = 10
    Output: 1024.00000

    Input: x = 2.10000, n = 3
    Output: 9.26100

    Input: x = 2.00000, n = -2
    Output: 0.25000
    Explanation: 2^-2 = 1/4 = 0.25

CONSTRAINTS:
- -100.0 < x < 100.0
- -2^31 <= n <= 2^31 - 1
- Either x is not zero or n > 0.
- -10^4 <= x^n <= 10^4

================================================================================
"""


# ============================================================================
# SOLUTION 1: Iterative Fast Exponentiation (Optimal)
# ============================================================================
def myPow(x: float, n: int) -> float:
    """
    Binary (fast) exponentiation: square the base and halve the exponent.
    Multiply the base into the result whenever the current exponent bit is 1.

        x^13 = x^8 * x^4 * x^1   (13 = 1101 in binary)

    Time:  O(log n)
    Space: O(1)
    """
    if n < 0:
        x = 1 / x
        n = -n

    result = 1.0
    while n:
        if n & 1:          # current lowest bit is set
            result *= x
        x *= x             # square the base for the next bit
        n >>= 1
    return result


# ============================================================================
# SOLUTION 2: Recursive Divide and Conquer
# ============================================================================
def myPow_recursive(x: float, n: int) -> float:
    """
    x^n = (x^(n/2))^2, with an extra x if n is odd.

    Time:  O(log n)
    Space: O(log n) recursion stack
    """
    def helper(base: float, exp: int) -> float:
        if exp == 0:
            return 1.0
        half = helper(base, exp // 2)
        if exp % 2 == 0:
            return half * half
        return half * half * base

    if n < 0:
        return helper(1 / x, -n)
    return helper(x, n)


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    print(f"myPow(2, 10)  -> {myPow(2, 10)}")    # 1024.0
    print(f"myPow(2.1, 3) -> {myPow(2.1, 3):.5f}")  # 9.26100
    print(f"myPow(2, -2)  -> {myPow(2, -2)}")    # 0.25
    print(f"myPow(2, 0)   -> {myPow(2, 0)}")     # 1.0
    print(f"myPow(1, 2^31)-> {myPow(1, 2**31 - 1)}")  # 1.0


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. WHY NOT A SIMPLE LOOP:
   Multiplying x by itself n times is O(n) and times out for n up to 2^31.
   Fast exponentiation turns that into O(log n) by squaring.

2. THE BINARY INSIGHT:
   Any exponent can be written in binary. Each set bit corresponds to a power
   of x you must include. Squaring the base each step produces x, x^2, x^4, ...
   ready to multiply in whenever the matching bit is 1.

3. NEGATIVE EXPONENT EDGE CASE:
   x^-n = 1 / x^n. Flip x to 1/x and negate n. Careful: negating INT_MIN
   overflows in fixed-width languages (not in Python) -- mention this.

4. practice TIP:
   The iterative version avoids recursion depth concerns for large n. Lead with
   it, then offer the elegant recursive form if asked.
"""
