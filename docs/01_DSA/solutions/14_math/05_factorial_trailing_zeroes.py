"""
================================================================================
PROBLEM: Factorial Trailing Zeroes (LeetCode 172)
Difficulty: Medium | Pattern: Math / Number Theory
================================================================================

PROBLEM STATEMENT:
Given an integer n, return the number of trailing zeroes in n! (n factorial).

EXAMPLES:
    Input: n = 3
    Output: 0
    Explanation: 3! = 6, no trailing zero.

    Input: n = 5
    Output: 1
    Explanation: 5! = 120, one trailing zero.

    Input: n = 0
    Output: 0

CONSTRAINTS:
- 0 <= n <= 10^4

FOLLOW-UP: Can you solve it in logarithmic time?

================================================================================
"""


# ============================================================================
# SOLUTION 1: Count Factors of 5 (Optimal, O(log n))
# ============================================================================
def trailingZeroes(n: int) -> int:
    """
    A trailing zero is produced by a factor of 10 = 2 * 5. In n!, factors of 2
    are far more common than factors of 5, so the number of 5s is the limiter.

    Count multiples of 5, plus 25, plus 125, ... (numbers like 25 contribute
    two 5s, etc.).

        count = n/5 + n/25 + n/125 + ...

    Time:  O(log_5 n)
    Space: O(1)
    """
    count = 0
    power_of_5 = 5
    while power_of_5 <= n:
        count += n // power_of_5
        power_of_5 *= 5
    return count


# ============================================================================
# SOLUTION 2: Divide-Down Variant (same idea, no overflow on power_of_5)
# ============================================================================
def trailingZeroes_divide(n: int) -> int:
    """
    Repeatedly divide n by 5 and accumulate. Equivalent to Solution 1 but never
    builds a large power_of_5 value.

    Time:  O(log_5 n)
    Space: O(1)
    """
    count = 0
    while n:
        n //= 5
        count += n
    return count


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    print(f"n = 3   -> {trailingZeroes(3)}")    # 0
    print(f"n = 5   -> {trailingZeroes(5)}")    # 1
    print(f"n = 10  -> {trailingZeroes(10)}")   # 2
    print(f"n = 25  -> {trailingZeroes(25)}")   # 6
    print(f"n = 100 -> {trailingZeroes(100)}")  # 24
    print(f"n = 0   -> {trailingZeroes(0)}")    # 0
    assert trailingZeroes(100) == trailingZeroes_divide(100)


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. THE KEY OBSERVATION:
   Trailing zeros come from factors of 10 = 2 * 5. In any factorial there are
   always more 2s than 5s, so just COUNT THE 5s. This turns an impossible
   "compute n!" problem into simple division.

2. WHY n/5 + n/25 + n/125 + ...:
   Every 5th number contributes one 5. Every 25th contributes an EXTRA 5
   (25 = 5*5), every 125th an extra one again, and so on. Summing these layers
   counts total factors of 5.

3. COMMON MISTAKE:
   Stopping after just n/5 forgets that 25, 50, 75, 100 each supply two 5s.
   Always loop over increasing powers of 5.

4. practice TIP:
   Do NOT try to compute n! directly -- it overflows instantly and misses the
   point. Jumping straight to "count factors of 5" signals real math maturity.
"""
