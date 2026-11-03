"""
================================================================================
PROBLEM: Find First and Last Position of Element (LeetCode 34)
Difficulty: Medium | Pattern: Binary Search Bounds
================================================================================

PROBLEM STATEMENT:
Given an array of integers nums sorted in non-decreasing order, find the 
starting and ending position of a given target value.

If target is not found in the array, return [-1, -1].

You must write an algorithm with O(log n) runtime complexity.

EXAMPLES:
    Input: nums = [5,7,7,8,8,10], target = 8
    Output: [3,4]

    Input: nums = [5,7,7,8,8,10], target = 6
    Output: [-1,-1]

    Input: nums = [], target = 0
    Output: [-1,-1]

CONSTRAINTS:
- 0 <= nums.length <= 10^5
- -10^9 <= nums[i] <= 10^9
- nums is a non-decreasing array
- -10^9 <= target <= 10^9

================================================================================
"""

from typing import List
import bisect


# ============================================================================
# SOLUTION 1: Two Binary Searches (Find Left, Find Right)
# ============================================================================
def searchRange(nums: List[int], target: int) -> List[int]:
    """
    Perform two binary searches:
    1. Find leftmost (first) occurrence
    2. Find rightmost (last) occurrence
    
    Time: O(log n)
    Space: O(1)
    """
    def find_left(nums, target):
        """Find the leftmost index where target appears."""
        left, right = 0, len(nums)
        
        while left < right:
            mid = left + (right - left) // 2
            
            if nums[mid] < target:
                left = mid + 1
            else:
                right = mid  # Move right even when equal
        
        return left
    
    def find_right(nums, target):
        """Find the rightmost index where target appears."""
        left, right = 0, len(nums)
        
        while left < right:
            mid = left + (right - left) // 2
            
            if nums[mid] <= target:
                left = mid + 1  # Move left even when equal
            else:
                right = mid
        
        return left - 1  # Subtract 1 because we went one past
    
    if not nums:
        return [-1, -1]
    
    left_idx = find_left(nums, target)
    
    # Check if target exists
    if left_idx == len(nums) or nums[left_idx] != target:
        return [-1, -1]
    
    right_idx = find_right(nums, target)
    
    return [left_idx, right_idx]


# ============================================================================
# SOLUTION 2: Using bisect library
# ============================================================================
def searchRange_bisect(nums: List[int], target: int) -> List[int]:
    """
    Use Python's bisect module for cleaner code.
    
    bisect_left: First position where target can be inserted
    bisect_right: Position after last occurrence
    
    Time: O(log n)
    Space: O(1)
    """
    left = bisect.bisect_left(nums, target)
    
    # Check if target exists
    if left == len(nums) or nums[left] != target:
        return [-1, -1]
    
    right = bisect.bisect_right(nums, target) - 1
    
    return [left, right]


# ============================================================================
# SOLUTION 3: Single Function with Direction Flag
# ============================================================================
def searchRange_unified(nums: List[int], target: int) -> List[int]:
    """
    Single binary search function with a flag for direction.
    
    Time: O(log n)
    Space: O(1)
    """
    def binary_search(nums, target, find_first):
        left, right = 0, len(nums) - 1
        result = -1
        
        while left <= right:
            mid = left + (right - left) // 2
            
            if nums[mid] == target:
                result = mid
                if find_first:
                    right = mid - 1  # Continue searching left
                else:
                    left = mid + 1  # Continue searching right
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        return result
    
    if not nums:
        return [-1, -1]
    
    first = binary_search(nums, target, True)
    
    if first == -1:
        return [-1, -1]
    
    last = binary_search(nums, target, False)
    
    return [first, last]


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Target exists multiple times
    nums1, target1 = [5, 7, 7, 8, 8, 10], 8
    print(f"Input: nums = {nums1}, target = {target1}")
    print(f"Output (Two searches): {searchRange(nums1, target1)}")
    print(f"Output (Bisect): {searchRange_bisect(nums1, target1)}")
    print(f"Output (Unified): {searchRange_unified(nums1, target1)}")
    # Expected: [3, 4]
    print()
    
    # Test Case 2: Target doesn't exist
    nums2, target2 = [5, 7, 7, 8, 8, 10], 6
    print(f"Input: nums = {nums2}, target = {target2}")
    print(f"Output: {searchRange(nums2, target2)}")
    # Expected: [-1, -1]
    print()
    
    # Test Case 3: Empty array
    nums3, target3 = [], 0
    print(f"Input: nums = {nums3}, target = {target3}")
    print(f"Output: {searchRange(nums3, target3)}")
    # Expected: [-1, -1]
    print()
    
    # Test Case 4: Single element (found)
    nums4, target4 = [1], 1
    print(f"Input: nums = {nums4}, target = {target4}")
    print(f"Output: {searchRange(nums4, target4)}")
    # Expected: [0, 0]
    print()
    
    # Test Case 5: All same elements
    nums5, target5 = [2, 2, 2, 2, 2], 2
    print(f"Input: nums = {nums5}, target = {target5}")
    print(f"Output: {searchRange(nums5, target5)}")
    # Expected: [0, 4]
    print()
    
    # Test Case 6: Target at boundaries
    nums6a = [1, 2, 3, 4, 5]
    print(f"Input: {nums6a}, target=1: {searchRange(nums6a, 1)}")  # [0, 0]
    print(f"Input: {nums6a}, target=5: {searchRange(nums6a, 5)}")  # [4, 4]


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. TWO TYPES OF BOUNDS:
   
   Lower bound (bisect_left):
   - First position where element >= target
   - Or: First position where target can be inserted
   
   Upper bound (bisect_right):
   - First position where element > target
   - Or: Position after last occurrence

2. FIND FIRST vs FIND LAST:
   
   Find First (leftmost):
   - When nums[mid] == target, go LEFT (right = mid)
   - Want to find the boundary between < and >=
   
   Find Last (rightmost):
   - When nums[mid] == target, go RIGHT (left = mid + 1)
   - Want to find the boundary between <= and >
   - Result is left - 1

3. VISUAL EXPLANATION:
   
   nums = [5, 7, 7, 8, 8, 10], target = 8
                   ↑  ↑
                 first last
   
   Find First 8:
   - Binary search converges to first position where value >= 8
   - Check if that value is actually 8
   
   Find Last 8:
   - Binary search converges to first position where value > 8
   - Subtract 1 to get last 8

4. BISECT MODULE:
   
   bisect_left(arr, x):  First position i where arr[i] >= x
   bisect_right(arr, x): First position i where arr[i] > x
   
   For target = 8 in [5,7,7,8,8,10]:
   bisect_left  → 3 (first 8)
   bisect_right → 5 (after last 8, so last 8 is at index 4)

5. EDGE CASES TO HANDLE:
   
   - Target not in array
   - Empty array
   - Single element
   - All elements are target
   - Target at first/last position

6. COMMON MISTAKES:
   
   - Forgetting to check if target actually exists
   - Off-by-one for rightmost (forgetting to subtract 1)
   - Wrong comparison operators (< vs <= in conditions)

7. TEMPLATE FOR LOWER BOUND:

   def lower_bound(arr, target):
       left, right = 0, len(arr)
       while left < right:
           mid = (left + right) // 2
           if arr[mid] < target:
               left = mid + 1
           else:
               right = mid
       return left

8. TEMPLATE FOR UPPER BOUND:

   def upper_bound(arr, target):
       left, right = 0, len(arr)
       while left < right:
           mid = (left + right) // 2
           if arr[mid] <= target:
               left = mid + 1
           else:
               right = mid
       return left

9. RELATIONSHIP:
   
   First occurrence = lower_bound(target)
   Last occurrence = upper_bound(target) - 1
   Count of target = upper_bound - lower_bound

10. RELATED PROBLEMS:
    - Count of Element (first position + last position + 1)
    - Search Insert Position (LC 35)
    - Find Smallest Letter Greater Than Target (LC 744)
    - Time Based Key-Value Store (LC 981)

================================================================================
"""
