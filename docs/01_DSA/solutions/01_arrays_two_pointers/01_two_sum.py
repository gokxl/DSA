"""
================================================================================
PROBLEM: Two Sum (LeetCode 1)
Difficulty: Easy | Pattern: Arrays & Two Pointers
================================================================================

PROBLEM STATEMENT:
Given an array of integers `nums` and an integer `target`, return indices of 
the two numbers such that they add up to `target`.

REQUIREMENTS:
- Each input has exactly one solution
- You may not use the same element twice
- Return answer in any order

EXAMPLES:
    Input: nums = [2,7,11,15], target = 9
    Output: [0,1]
    Explanation: nums[0] + nums[1] = 2 + 7 = 9

    Input: nums = [3,2,4], target = 6
    Output: [1,2]

    Input: nums = [3,3], target = 6
    Output: [0,1]

CONSTRAINTS:
- 2 <= nums.length <= 10^4
- -10^9 <= nums[i] <= 10^9
- -10^9 <= target <= 10^9
- Only one valid answer exists

================================================================================
"""

from typing import List


# ============================================================================
# SOLUTION 1: Brute Force (Don't use in practice, but mention it)
# ============================================================================
def twoSum_bruteforce(nums: List[int], target: int) -> List[int]:
    """
    Check every pair of elements.
    
    Time: O(n^2) - nested loops
    Space: O(1)
    """
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []


# ============================================================================
# SOLUTION 2: HashMap (Optimal - Use this in practice)
# ============================================================================
def twoSum(nums: List[int], target: int) -> List[int]:
    """
    Use HashMap to store seen values and their indices.
    For each number, check if its complement (target - num) exists.
    
    Time: O(n) - single pass through array
    Space: O(n) - HashMap stores up to n elements
    """
    seen = {}  # value -> index
    
    for i, num in enumerate(nums):
        complement = target - num
        
        if complement in seen:
            return [seen[complement], i]
        
        seen[num] = i
    
    return []  # No solution found


# ============================================================================
# SOLUTION 3: Two Pointers (Only if array is sorted)
# ============================================================================
def twoSum_sorted(nums: List[int], target: int) -> List[int]:
    """
    If array is SORTED, use two pointers.
    Note: This returns values, not original indices (indices change after sort)
    
    Time: O(n) if already sorted, O(n log n) if need to sort
    Space: O(1)
    """
    left, right = 0, len(nums) - 1
    
    while left < right:
        curr_sum = nums[left] + nums[right]
        
        if curr_sum == target:
            return [left, right]
        elif curr_sum < target:
            left += 1
        else:
            right -= 1
    
    return []


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1
    nums1 = [2, 7, 11, 15]
    target1 = 9
    print(f"Input: nums={nums1}, target={target1}")
    print(f"Output: {twoSum(nums1, target1)}")  # Expected: [0, 1]
    print()
    
    # Test Case 2
    nums2 = [3, 2, 4]
    target2 = 6
    print(f"Input: nums={nums2}, target={target2}")
    print(f"Output: {twoSum(nums2, target2)}")  # Expected: [1, 2]
    print()
    
    # Test Case 3: Duplicates
    nums3 = [3, 3]
    target3 = 6
    print(f"Input: nums={nums3}, target={target3}")
    print(f"Output: {twoSum(nums3, target3)}")  # Expected: [0, 1]
    print()
    
    # Test Case 4: Negative numbers
    nums4 = [-1, -2, -3, -4, -5]
    target4 = -8
    print(f"Input: nums={nums4}, target={target4}")
    print(f"Output: {twoSum(nums4, target4)}")  # Expected: [2, 4]


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. ALWAYS MENTION BRUTE FORCE FIRST
   - Shows you understand the problem
   - Then optimize to HashMap approach

2. HASHMAP TRADEOFF
   - Trade space for time: O(n) space gives O(n) time
   - This is a common pattern in practice sessions

3. EDGE CASES TO DISCUSS:
   - Duplicates: [3, 3] with target 6
   - Negative numbers
   - What if no solution? (problem says exactly one exists)
   - Can I use the same element twice? (No)

4. FOLLOW-UP QUESTIONS:
   Q: What if array is sorted?
   A: Use two pointers, O(1) space
   
   Q: What if we need all pairs?
   A: Don't return early, collect all pairs
   
   Q: What about 3Sum?
   A: Fix one element, reduce to 2Sum (next problem)

5. COMMUNICATION TIPS:
   - "Let me first clarify - can we use the same element twice?"
   - "I'll start with brute force, then optimize"
   - "The key insight is that if we've seen a number, we can check if its 
      complement exists in O(1) using a HashMap"

================================================================================
"""
