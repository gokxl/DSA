"""
================================================================================
PROBLEM: House Robber (LeetCode 198)
Difficulty: Medium | Pattern: DP (1D)
================================================================================

PROBLEM STATEMENT:
You are a professional robber planning to rob houses along a street. Each house 
has a certain amount of money stashed, the only constraint stopping you from 
robbing each of them is that adjacent houses have security systems connected 
and it will automatically contact the police if two adjacent houses were broken 
into on the same night.

Given an integer array nums representing the amount of money of each house, 
return the maximum amount of money you can rob tonight without alerting the 
police.

EXAMPLES:
    Input: nums = [1,2,3,1]
    Output: 4
    Explanation: Rob house 1 (money = 1) and then rob house 3 (money = 3).
    Total = 1 + 3 = 4.

    Input: nums = [2,7,9,3,1]
    Output: 12
    Explanation: Rob house 1 (money = 2), house 3 (money = 9) and house 5 (money = 1).
    Total = 2 + 9 + 1 = 12.

CONSTRAINTS:
- 1 <= nums.length <= 100
- 0 <= nums[i] <= 400

================================================================================
"""
from typing import List


# ============================================================================
# SOLUTION 1: Bottom-Up DP
# ============================================================================
def rob_dp(nums: List[int]) -> int:
    """
    dp[i] = maximum money from houses 0 to i
    
    At house i, either:
    - Skip it: dp[i-1]
    - Rob it: nums[i] + dp[i-2]
    
    Time: O(n)
    Space: O(n)
    """
    n = len(nums)
    if n == 1:
        return nums[0]
    
    dp = [0] * n
    dp[0] = nums[0]
    dp[1] = max(nums[0], nums[1])
    
    for i in range(2, n):
        dp[i] = max(dp[i - 1], nums[i] + dp[i - 2])
    
    return dp[n - 1]


# ============================================================================
# SOLUTION 2: Space Optimized
# ============================================================================
def rob(nums: List[int]) -> int:
    """
    Only need last two values, so use two variables.
    
    Time: O(n)
    Space: O(1)
    """
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
    
    prev2 = nums[0]          # dp[i-2]
    prev1 = max(nums[0], nums[1])  # dp[i-1]
    
    for i in range(2, len(nums)):
        current = max(prev1, nums[i] + prev2)
        prev2 = prev1
        prev1 = current
    
    return prev1


# ============================================================================
# SOLUTION 3: Alternative DP formulation
# ============================================================================
def rob_alt(nums: List[int]) -> int:
    """
    Track rob vs not-rob at each position.
    
    rob[i] = max money if we rob house i
    not_rob[i] = max money if we don't rob house i
    
    Time: O(n)
    Space: O(1)
    """
    if not nums:
        return 0
    
    rob = nums[0]
    not_rob = 0
    
    for i in range(1, len(nums)):
        new_rob = not_rob + nums[i]  # Must not have robbed previous
        new_not_rob = max(rob, not_rob)  # Max of either case
        rob, not_rob = new_rob, new_not_rob
    
    return max(rob, not_rob)


# ============================================================================
# SOLUTION 4: Recursive with Memoization
# ============================================================================
def rob_memo(nums: List[int]) -> int:
    """
    Top-down approach.
    
    Time: O(n)
    Space: O(n)
    """
    from functools import lru_cache
    
    @lru_cache(maxsize=None)
    def dp(i: int) -> int:
        if i < 0:
            return 0
        return max(dp(i - 1), nums[i] + dp(i - 2))
    
    return dp(len(nums) - 1)


# ============================================================================
# HOUSE ROBBER II (LC 213) - Circular houses
# ============================================================================
def rob_circular(nums: List[int]) -> int:
    """
    Houses are in a circle - first and last are adjacent.
    
    Solution: Max of (rob 0 to n-2) and (rob 1 to n-1)
    
    Time: O(n)
    Space: O(1)
    """
    n = len(nums)
    if n == 1:
        return nums[0]
    
    def rob_range(start: int, end: int) -> int:
        prev2, prev1 = 0, 0
        for i in range(start, end + 1):
            current = max(prev1, nums[i] + prev2)
            prev2, prev1 = prev1, current
        return prev1
    
    # Either skip first house or skip last house
    return max(rob_range(0, n - 2), rob_range(1, n - 1))


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Standard case
    nums1 = [1, 2, 3, 1]
    print(f"nums = {nums1}")
    print(f"DP: {rob_dp(nums1)}")
    print(f"Optimized: {rob(nums1)}")
    # Expected: 4 (1 + 3)
    print()
    
    # Test Case 2: Another case
    nums2 = [2, 7, 9, 3, 1]
    print(f"nums = {nums2}")
    print(f"Result: {rob(nums2)}")
    # Expected: 12 (2 + 9 + 1)
    print()
    
    # Test Case 3: Single house
    nums3 = [5]
    print(f"nums = {nums3}")
    print(f"Result: {rob(nums3)}")
    # Expected: 5
    print()
    
    # Test Case 4: Two houses
    nums4 = [1, 2]
    print(f"nums = {nums4}")
    print(f"Result: {rob(nums4)}")
    # Expected: 2
    print()
    
    # Test Case 5: Circular houses (House Robber II)
    nums5 = [2, 3, 2]
    print(f"Circular: nums = {nums5}")
    print(f"Result: {rob_circular(nums5)}")
    # Expected: 3 (can't rob both 2s since they're adjacent in circle)


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. CORE RECURRENCE:
   
   At house i, two choices:
   - Skip: Take dp[i-1]
   - Rob: Take nums[i] + dp[i-2]
   
   dp[i] = max(dp[i-1], nums[i] + dp[i-2])

2. INTUITION:
   
   "If I rob this house, I can't rob the previous one,
   so I get nums[i] plus the best from two houses ago.
   
   If I skip this house, I get the best from the previous house."

3. SPACE OPTIMIZATION:
   
   Only need dp[i-1] and dp[i-2], so use two variables:
   
   prev2, prev1 = prev1, max(prev1, nums[i] + prev2)

4. ALTERNATIVE: ROB VS NOT-ROB:
   
   Track separately:
   - rob[i] = best if we rob i → not_rob[i-1] + nums[i]
   - not_rob[i] = best if we skip i → max(rob[i-1], not_rob[i-1])

5. BASE CASES:
   
   dp[0] = nums[0] (must rob first if only one)
   dp[1] = max(nums[0], nums[1]) (pick better of first two)

6. HOUSE ROBBER II (CIRCULAR):
   
   First and last are adjacent!
   
   Solution: Can't rob both, so take max of:
   - Rob houses 0 to n-2 (skip last)
   - Rob houses 1 to n-1 (skip first)

7. HOUSE ROBBER III (TREE):
   
   Houses form a tree. Similar concept but need tree DP:
   
   At each node: max(skip, rob)
   rob = node.val + skip(left) + skip(right)
   skip = max(rob, skip for left) + max(rob, skip for right)

8. COMMON MISTAKES:
   
   ❌ Wrong base cases
   ❌ Off-by-one in circular version
   ❌ Not handling single element case

9. RELATED PROBLEMS:
   
   - House Robber II (LC 213) - circular
   - House Robber III (LC 337) - tree
   - Delete and Earn (LC 740)
   - Paint House (LC 256)

10. HOW TO EXPLAIN IT:
    
    "This is a classic DP problem. At each house, I either
    skip it (take dp[i-1]) or rob it (take nums[i] + dp[i-2]).
    
    dp[i] = max(dp[i-1], nums[i] + dp[i-2])
    
    Since I only need the last two values, I can optimize
    to O(1) space.
    
    For the circular variant, I solve twice: once excluding
    the first house, once excluding the last, and take max."

================================================================================
"""
