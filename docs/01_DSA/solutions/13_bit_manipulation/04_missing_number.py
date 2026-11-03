"""
================================================================================
PROBLEM: Missing Number (LeetCode 268)
Difficulty: Easy | Pattern: Bit Manipulation / Math
================================================================================

PROBLEM STATEMENT:
Given an array nums containing n distinct numbers in the range [0, n], return
the only number in the range that is missing from the array.

EXAMPLES:
    Input: nums = [3, 0, 1]
    Output: 2
    Explanation: n = 3, range is [0, 3]. 2 is missing.

    Input: nums = [0, 1]
    Output: 2

    Input: nums = [9, 6, 4, 2, 3, 5, 7, 0, 1]
    Output: 8

CONSTRAINTS:
- n == nums.length
- 1 <= n <= 10^4
- 0 <= nums[i] <= n
- All numbers are distinct.

FOLLOW-UP: O(1) extra space and O(n) runtime.

================================================================================
"""


# ============================================================================
# SOLUTION 1: XOR (Optimal, no overflow risk)
# ============================================================================
def missingNumber(nums: list[int]) -> int:
    """
    XOR every index 0..n together with every value. Each present number cancels
    with its index; the leftover is the missing number.

    Time:  O(n)
    Space: O(1)
    """
    result = len(nums)  # start with n (the index that has no value)
    for i, num in enumerate(nums):
        result ^= i ^ num
    return result


# ============================================================================
# SOLUTION 2: Gauss Sum Formula
# ============================================================================
def missingNumber_sum(nums: list[int]) -> int:
    """
    Expected sum of 0..n is n*(n+1)//2. Missing = expected - actual.

    Time:  O(n)
    Space: O(1)
    (Watch for integer overflow in languages with fixed-width ints; safe in Python.)
    """
    n = len(nums)
    expected = n * (n + 1) // 2
    return expected - sum(nums)


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    print(f"[3, 0, 1]                  -> {missingNumber([3, 0, 1])}")   # 2
    print(f"[0, 1]                     -> {missingNumber([0, 1])}")      # 2
    print(f"[9,6,4,2,3,5,7,0,1]        -> "
          f"{missingNumber([9, 6, 4, 2, 3, 5, 7, 0, 1])}")              # 8
    print(f"[0]                        -> {missingNumber([0])}")        # 1


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. TWO CLEAN O(1)-SPACE APPROACHES:
   - XOR:  index ^ value pairs cancel, missing survives. No overflow.
   - Sum:  n(n+1)/2 - actual_sum. Simpler to explain, but can overflow in
           fixed-width-int languages.

2. WHY XOR IS SAFER:
   In Java/C++, the Gauss sum can overflow for large n. XOR never overflows,
   so it is the preferred answer when the interviewer cares about robustness.

3. RELATED PROBLEMS (same toolkit):
   - Single Number (LC 136): XOR to cancel duplicates.
   - Find the Duplicate Number (LC 287): cycle detection variant.
   - First Missing Positive (LC 41): harder, uses index-as-hash.

4. HOW TO EXPLAIN IT:
   Offer the sum formula first (easiest to reason about), then say "to avoid
   overflow I'd prefer XOR" -- it signals maturity about edge cases.
"""
