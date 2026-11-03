"""
================================================================================
PROBLEM: Binary Search (LeetCode 704)
Difficulty: Easy | Pattern: Classic Binary Search
================================================================================

PROBLEM STATEMENT:
Given an array of integers nums which is sorted in ascending order, and an 
integer target, write a function to search target in nums. If target exists, 
then return its index. Otherwise, return -1.

You must write an algorithm with O(log n) runtime complexity.

EXAMPLES:
    Input: nums = [-1,0,3,5,9,12], target = 9
    Output: 4
    Explanation: 9 exists in nums and its index is 4

    Input: nums = [-1,0,3,5,9,12], target = 2
    Output: -1
    Explanation: 2 does not exist in nums

CONSTRAINTS:
- 1 <= nums.length <= 10^4
- -10^4 < nums[i], target < 10^4
- All elements in nums are unique
- nums is sorted in ascending order

================================================================================
"""

from typing import List


# ============================================================================
# SOLUTION 1: Classic Binary Search (Closed interval [left, right])
# ============================================================================
def search(nums: List[int], target: int) -> int:
    """
    Standard binary search with closed interval [left, right].
    
    Invariant: If target exists, it's in [left, right]
    
    Time: O(log n)
    Space: O(1)
    """
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = left + (right - left) // 2  # Avoid overflow
        
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1  # Target in right half
        else:
            right = mid - 1  # Target in left half
    
    return -1


# ============================================================================
# SOLUTION 2: Binary Search with Open Interval [left, right)
# ============================================================================
def search_open(nums: List[int], target: int) -> int:
    """
    Binary search with half-open interval [left, right).
    
    Invariant: If target exists, it's in [left, right)
    
    Time: O(log n)
    Space: O(1)
    """
    left, right = 0, len(nums)  # right is exclusive
    
    while left < right:  # Note: < instead of <=
        mid = left + (right - left) // 2
        
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid  # Note: mid, not mid - 1
    
    return -1


# ============================================================================
# SOLUTION 3: Recursive Binary Search
# ============================================================================
def search_recursive(nums: List[int], target: int) -> int:
    """
    Recursive implementation.
    
    Time: O(log n)
    Space: O(log n) - call stack
    """
    def helper(left: int, right: int) -> int:
        if left > right:
            return -1
        
        mid = left + (right - left) // 2
        
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            return helper(mid + 1, right)
        else:
            return helper(left, mid - 1)
    
    return helper(0, len(nums) - 1)


# ============================================================================
# TEMPLATE: Find Leftmost (First occurrence)
# ============================================================================
def search_leftmost(nums: List[int], target: int) -> int:
    """
    Find the leftmost (first) occurrence of target.
    Returns index or -1 if not found.
    
    Time: O(log n)
    Space: O(1)
    """
    left, right = 0, len(nums)
    
    while left < right:
        mid = left + (right - left) // 2
        
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid  # Move right even when equal
    
    if left < len(nums) and nums[left] == target:
        return left
    return -1


# ============================================================================
# TEMPLATE: Find Rightmost (Last occurrence)
# ============================================================================
def search_rightmost(nums: List[int], target: int) -> int:
    """
    Find the rightmost (last) occurrence of target.
    Returns index or -1 if not found.
    
    Time: O(log n)
    Space: O(1)
    """
    left, right = 0, len(nums)
    
    while left < right:
        mid = left + (right - left) // 2
        
        if nums[mid] <= target:
            left = mid + 1  # Move left even when equal
        else:
            right = mid
    
    # left is now past the last target
    if left > 0 and nums[left - 1] == target:
        return left - 1
    return -1


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Target exists
    nums1, target1 = [-1, 0, 3, 5, 9, 12], 9
    print(f"Input: nums = {nums1}, target = {target1}")
    print(f"Output (Closed): {search(nums1, target1)}")
    print(f"Output (Open): {search_open(nums1, target1)}")
    print(f"Output (Recursive): {search_recursive(nums1, target1)}")
    # Expected: 4
    print()
    
    # Test Case 2: Target doesn't exist
    nums2, target2 = [-1, 0, 3, 5, 9, 12], 2
    print(f"Input: nums = {nums2}, target = {target2}")
    print(f"Output: {search(nums2, target2)}")
    # Expected: -1
    print()
    
    # Test Case 3: Single element (found)
    nums3, target3 = [5], 5
    print(f"Input: nums = {nums3}, target = {target3}")
    print(f"Output: {search(nums3, target3)}")
    # Expected: 0
    print()
    
    # Test Case 4: Single element (not found)
    nums4, target4 = [5], 3
    print(f"Input: nums = {nums4}, target = {target4}")
    print(f"Output: {search(nums4, target4)}")
    # Expected: -1
    print()
    
    # Test Case 5: First element
    nums5, target5 = [1, 2, 3, 4, 5], 1
    print(f"Input: nums = {nums5}, target = {target5}")
    print(f"Output: {search(nums5, target5)}")
    # Expected: 0
    print()
    
    # Test Case 6: Last element
    nums6, target6 = [1, 2, 3, 4, 5], 5
    print(f"Input: nums = {nums6}, target = {target6}")
    print(f"Output: {search(nums6, target6)}")
    # Expected: 4
    print()
    
    # Test Case 7: Leftmost and rightmost (with duplicates)
    nums7 = [1, 2, 2, 2, 3, 4]
    print(f"Array with duplicates: {nums7}, target = 2")
    print(f"Leftmost: {search_leftmost(nums7, 2)}")  # Expected: 1
    print(f"Rightmost: {search_rightmost(nums7, 2)}")  # Expected: 3


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. TWO MAIN STYLES (Know both!):
   
   a) Closed interval [left, right]:
      - while left <= right
      - right = mid - 1 (exclude mid)
      - More intuitive for exact search
   
   b) Half-open interval [left, right):
      - while left < right
      - right = mid (exclude right boundary)
      - Better for boundary problems

2. AVOIDING OVERFLOW:
   
   BAD:  mid = (left + right) / 2     # Can overflow!
   GOOD: mid = left + (right - left) / 2

3. THREE TYPES OF BINARY SEARCH:
   
   a) Exact match: Find target
   b) Lower bound: First element >= target
   c) Upper bound: First element > target
   
   Lower/upper bound are crucial for many problems!

4. BINARY SEARCH DECISION TEMPLATE:
   
   def binary_search(arr, target):
       left, right = 0, len(arr)  # or len(arr) - 1
       
       while left < right:  # or left <= right
           mid = left + (right - left) // 2
           
           if CONDITION(arr[mid]):
               right = mid  # or mid - 1
           else:
               left = mid + 1
       
       return left  # or check if found

5. WHEN TO USE WHICH:
   
   - Exact search: Either style works
   - Find first occurrence: Use [left, right), move right when >=
   - Find last occurrence: Use [left, right), move left when <=
   - Find insertion point: bisect_left or bisect_right

6. PYTHON BUILT-IN:
   
   import bisect
   - bisect.bisect_left(arr, x)   # First position >= x
   - bisect.bisect_right(arr, x)  # First position > x
   - bisect.insort_left(arr, x)   # Insert maintaining sorted order

7. COMMON MISTAKES:
   - Off-by-one errors (most common!)
   - Wrong loop condition (< vs <=)
   - Wrong update (mid vs mid-1 vs mid+1)
   - Infinite loop (left = mid when range is [left, mid])

8. VISUALIZING THE SEARCH:
   
   nums = [1, 3, 5, 7, 9], target = 5
   
   Step 1: left=0, right=4, mid=2
           nums[2]=5 == target ✓ Return 2
   
   nums = [1, 3, 5, 7, 9], target = 6
   
   Step 1: left=0, right=4, mid=2
           nums[2]=5 < 6, left=3
   Step 2: left=3, right=4, mid=3
           nums[3]=7 > 6, right=2
   Step 3: left=3 > right=2, exit
           Return -1

9. BINARY SEARCH ON ANSWER:
   
   Many problems use binary search on the answer space:
   - "Find minimum X such that CONDITION is true"
   - Binary search on possible values of X
   - Check CONDITION in O(n) or O(n log n)
   
   Examples: Koko Eating Bananas, Capacity To Ship

10. RELATED PROBLEMS:
    - Search Insert Position (LC 35)
    - Find First and Last Position (LC 34)
    - Search in Rotated Array (LC 33)
    - Find Peak Element (LC 162)
    - Koko Eating Bananas (LC 875)

================================================================================
"""
