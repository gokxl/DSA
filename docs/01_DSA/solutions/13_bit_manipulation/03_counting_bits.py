"""
================================================================================
PROBLEM: Counting Bits (LeetCode 338)
Difficulty: Easy | Pattern: Bit Manipulation + DP
================================================================================

PROBLEM STATEMENT:
Given an integer n, return an array ans of length n + 1 such that for each i
(0 <= i <= n), ans[i] is the number of 1's in the binary representation of i.

EXAMPLES:
    Input: n = 2
    Output: [0, 1, 1]
    Explanation: 0 -> 0, 1 -> 1, 2 -> 10

    Input: n = 5
    Output: [0, 1, 1, 2, 1, 2]
    Explanation:
        0 -> 000
        1 -> 001
        2 -> 010
        3 -> 011
        4 -> 100
        5 -> 101

CONSTRAINTS:
- 0 <= n <= 10^5

FOLLOW-UP: Solve it in O(n) time using a single pass without __builtin_popcount.

================================================================================
"""


# ============================================================================
# SOLUTION 1: DP using Right Shift (Optimal)
# ============================================================================
def countBits(n: int) -> list[int]:
    """
    i >> 1 removes the lowest bit of i, so it has the same set-bit count as i
    minus that lowest bit. Add back (i & 1) for the bit we dropped.

        dp[i] = dp[i >> 1] + (i & 1)

    Time:  O(n)
    Space: O(1) extra (output array not counted)
    """
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i >> 1] + (i & 1)
    return dp


# ============================================================================
# SOLUTION 2: DP using Kernighan Relation (Lowest Set Bit)
# ============================================================================
def countBits_lowbit(n: int) -> list[int]:
    """
    i & (i - 1) clears the lowest set bit, giving a smaller already-solved
    subproblem.

        dp[i] = dp[i & (i - 1)] + 1

    Time:  O(n)
    Space: O(1) extra
    """
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i & (i - 1)] + 1
    return dp


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    print(f"n = 2 -> {countBits(2)}")  # [0, 1, 1]
    print(f"n = 5 -> {countBits(5)}")  # [0, 1, 1, 2, 1, 2]
    print(f"n = 0 -> {countBits(0)}")  # [0]
    assert countBits(5) == countBits_lowbit(5)


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. THE KEY REALIZATION:
   This is DP where each answer reuses a smaller, already-computed answer.
   Two valid recurrences:
     - Right shift:  dp[i] = dp[i >> 1] + (i & 1)
     - Lowest bit:   dp[i] = dp[i & (i - 1)] + 1

2. WHY O(n) BEATS THE NAIVE O(n log n):
   Calling popcount on each number is O(n * 32). Reusing prior results makes
   each new value O(1), giving a clean O(n).

3. CONNECTION TO OTHER PROBLEMS:
   - Number of 1 Bits (LC 191) is the single-value version.
   - The i & (i - 1) trick is the same Brian Kernighan idea reused as DP.

4. HOW TO EXPLAIN IT:
   Draw the binary table for 0..5 and point out that i and i>>1 differ by only
   the trailing bit. That observation is the whole solution.
"""
