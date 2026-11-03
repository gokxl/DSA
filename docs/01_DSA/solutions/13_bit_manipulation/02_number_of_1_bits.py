"""
================================================================================
PROBLEM: Number of 1 Bits / Hamming Weight (LeetCode 191)
Difficulty: Easy | Pattern: Bit Manipulation
================================================================================

PROBLEM STATEMENT:
Write a function that takes the binary representation of a positive integer and
returns the number of set bits it has (also known as the Hamming weight).

EXAMPLES:
    Input: n = 11   (binary 1011)
    Output: 3

    Input: n = 128  (binary 10000000)
    Output: 1

    Input: n = 2147483645
    Output: 30

CONSTRAINTS:
- 1 <= n <= 2^31 - 1

================================================================================
"""


# ============================================================================
# SOLUTION 1: Brian Kernighan's Trick (Optimal)
# ============================================================================
def hammingWeight(n: int) -> int:
    """
    n & (n - 1) clears the LOWEST set bit of n.
    So we loop exactly once per set bit instead of once per bit.

    Example: n = 1100
        n - 1    = 1011
        n & (n-1)= 1000   (lowest set bit cleared)

    Time:  O(k) where k = number of set bits (<= 32)
    Space: O(1)
    """
    count = 0
    while n:
        n &= n - 1
        count += 1
    return count


# ============================================================================
# SOLUTION 2: Check Each Bit
# ============================================================================
def hammingWeight_shift(n: int) -> int:
    """
    Inspect the lowest bit, then shift right. Always 32 iterations.

    Time:  O(32)
    Space: O(1)
    """
    count = 0
    while n:
        count += n & 1
        n >>= 1
    return count


# ============================================================================
# SOLUTION 3: Built-in (know this exists, but be able to explain the trick)
# ============================================================================
def hammingWeight_builtin(n: int) -> int:
    """Python makes this trivial. Time: O(1) conceptually. Space: O(1)."""
    return bin(n).count("1")


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    print(f"11         -> {hammingWeight(11)}")          # 3
    print(f"128        -> {hammingWeight(128)}")         # 1
    print(f"2147483645 -> {hammingWeight(2147483645)}")  # 30
    print(f"0          -> {hammingWeight(0)}")           # 0


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. BRIAN KERNIGHAN'S TRICK (the one to show off):
   n & (n - 1) removes the rightmost 1 bit. Looping on this runs only as many
   times as there are set bits -> faster than scanning all 32 positions.

2. WHY n & (n - 1) CLEARS THE LOWEST SET BIT:
   Subtracting 1 flips the lowest set bit to 0 and all bits below it to 1.
   ANDing with the original keeps everything above untouched and zeroes that
   block, erasing exactly the lowest set bit.

3. RELATED: Counting Bits (LC 338) asks for this for every number 0..n and is
   best solved with DP: dp[i] = dp[i >> 1] + (i & 1).

4. HOW TO EXPLAIN IT:
   Start with the simple shift-and-mask version, then mention Kernighan's
   optimization. Interviewers love the "I can do better" moment.
"""
