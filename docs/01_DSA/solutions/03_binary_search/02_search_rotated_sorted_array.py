"""
================================================================================
PROBLEM: Search in Rotated Sorted Array (LeetCode 33)
Difficulty: Medium | Pattern: Binary Search + Rotation
================================================================================

PROBLEM STATEMENT:
There is an integer array nums sorted in ascending order (with distinct values).

Prior to being passed to your function, nums is possibly rotated at an unknown 
pivot index k (1 <= k < nums.length) such that the resulting array is:
[nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]] (0-indexed).

For example, [0,1,2,4,5,6,7] might be rotated at pivot index 3 → [4,5,6,7,0,1,2].

Given the array nums after the possible rotation and an integer target, return 
the index of target if it is in nums, or -1 if it is not in nums.

You must write an algorithm with O(log n) runtime complexity.

EXAMPLES:
    Input: nums = [4,5,6,7,0,1,2], target = 0
    Output: 4

    Input: nums = [4,5,6,7,0,1,2], target = 3
    Output: -1

    Input: nums = [1], target = 0
    Output: -1

CONSTRAINTS:
- 1 <= nums.length <= 5000
- -10^4 <= nums[i] <= 10^4
- All values of nums are unique
- nums is an ascending array that is possibly rotated
- -10^4 <= target <= 10^4

================================================================================
"""

from typing import List


# ============================================================================
# SOLUTION 1: One-Pass Binary Search (Optimal)
# ============================================================================
def search(nums: List[int], target: int) -> int:
    """
    Key insight: At least one half is always sorted!
    
    If nums[left] <= nums[mid]: Left half is sorted
    Else: Right half is sorted
    
    Check if target is in the sorted half, then decide which way to go.
    
    Time: O(log n)
    Space: O(1)
    """
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if nums[mid] == target:
            return mid
        
        # Check which half is sorted
        if nums[left] <= nums[mid]:
            # Left half [left, mid] is sorted
            if nums[left] <= target < nums[mid]:
                # Target is in sorted left half
                right = mid - 1
            else:
                # Target is in right half
                left = mid + 1
        else:
            # Right half [mid, right] is sorted
            if nums[mid] < target <= nums[right]:
                # Target is in sorted right half
                left = mid + 1
            else:
                # Target is in left half
                right = mid - 1
    
    return -1


# ============================================================================
# SOLUTION 2: Two-Pass (Find pivot, then binary search)
# ============================================================================
def search_two_pass(nums: List[int], target: int) -> int:
    """
    Step 1: Find the pivot (minimum element index)
    Step 2: Binary search in the appropriate half
    
    Time: O(log n) - two binary searches
    Space: O(1)
    """
    n = len(nums)
    
    # Step 1: Find pivot (index of minimum element)
    left, right = 0, n - 1
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid
    
    pivot = left  # Index of minimum element
    
    # Step 2: Determine which half to search
    if target >= nums[pivot] and target <= nums[n - 1]:
        # Target is in right sorted half
        left, right = pivot, n - 1
    else:
        # Target is in left sorted half
        left, right = 0, pivot - 1
    
    # Standard binary search
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1


# ============================================================================
# SOLUTION 3: Find Rotation + Virtual Index Mapping
# ============================================================================
def search_virtual(nums: List[int], target: int) -> int:
    """
    Find rotation amount, then do binary search with virtual indices.
    
    Real index = (virtual index + rotation) % n
    
    Time: O(log n)
    Space: O(1)
    """
    n = len(nums)
    
    # Find rotation (index of minimum)
    left, right = 0, n - 1
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid
    
    rotation = left
    
    # Binary search with virtual indices
    left, right = 0, n - 1
    while left <= right:
        mid = left + (right - left) // 2
        real_mid = (mid + rotation) % n
        
        if nums[real_mid] == target:
            return real_mid
        elif nums[real_mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Target in right half
    nums1, target1 = [4, 5, 6, 7, 0, 1, 2], 0
    print(f"Input: nums = {nums1}, target = {target1}")
    print(f"Output (One-pass): {search(nums1, target1)}")
    print(f"Output (Two-pass): {search_two_pass(nums1, target1)}")
    print(f"Output (Virtual): {search_virtual(nums1, target1)}")
    # Expected: 4
    print()
    
    # Test Case 2: Target not found
    nums2, target2 = [4, 5, 6, 7, 0, 1, 2], 3
    print(f"Input: nums = {nums2}, target = {target2}")
    print(f"Output: {search(nums2, target2)}")
    # Expected: -1
    print()
    
    # Test Case 3: Single element (not found)
    nums3, target3 = [1], 0
    print(f"Input: nums = {nums3}, target = {target3}")
    print(f"Output: {search(nums3, target3)}")
    # Expected: -1
    print()
    
    # Test Case 4: Not rotated
    nums4, target4 = [1, 2, 3, 4, 5], 3
    print(f"Input: nums = {nums4}, target = {target4}")
    print(f"Output: {search(nums4, target4)}")
    # Expected: 2
    print()
    
    # Test Case 5: Target in left half
    nums5, target5 = [4, 5, 6, 7, 0, 1, 2], 5
    print(f"Input: nums = {nums5}, target = {target5}")
    print(f"Output: {search(nums5, target5)}")
    # Expected: 1
    print()
    
    # Test Case 6: Rotation at middle
    nums6, target6 = [3, 1], 1
    print(f"Input: nums = {nums6}, target = {target6}")
    print(f"Output: {search(nums6, target6)}")
    # Expected: 1


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. THE KEY OBSERVATION:
   
   After rotation, at least ONE HALF is always sorted!
   
   Original: [0, 1, 2, 4, 5, 6, 7]
   Rotated:  [4, 5, 6, 7 | 0, 1, 2]
                sorted    sorted
   
   The pivot divides array into two sorted halves.

2. HOW TO IDENTIFY WHICH HALF IS SORTED:
   
   Compare nums[left] with nums[mid]:
   
   - If nums[left] <= nums[mid]: Left half is sorted
   - Else: Right half is sorted
   
   Note: Use <= to handle edge case when left == mid

3. DECISION LOGIC (One-pass approach):
   
   Case 1: Left half sorted (nums[left] <= nums[mid])
       - If target in [nums[left], nums[mid]) → go left
       - Else → go right
   
   Case 2: Right half sorted
       - If target in (nums[mid], nums[right]] → go right
       - Else → go left

4. VISUAL WALKTHROUGH for [4,5,6,7,0,1,2], target=0:
   
   Step 1: left=0, right=6, mid=3
           nums[0]=4 <= nums[3]=7 → left half sorted
           Is 4 <= 0 < 7? No → go right
           left = 4
   
   Step 2: left=4, right=6, mid=5
           nums[4]=0 <= nums[5]=1 → left half sorted
           Is 0 <= 0 < 1? Yes → go left
           right = 4
   
   Step 3: left=4, right=4, mid=4
           nums[4]=0 == target ✓ Return 4

5. EDGE CASES TO CONSIDER:
   
   - Not rotated at all: [1, 2, 3, 4, 5]
   - Rotated by 1: [5, 1, 2, 3, 4]
   - Single element: [1]
   - Two elements: [2, 1]
   - Target at boundaries

6. COMMON MISTAKES:
   
   - Using < instead of <= when checking sorted half
     (fails when left == mid)
   - Wrong boundary checks for target range
   - Off-by-one in range comparisons

7. RELATED PROBLEM: WITH DUPLICATES (LC 81)
   
   If nums can have duplicates:
   - When nums[left] == nums[mid] == nums[right]
   - Can't determine which half is sorted
   - Shrink both: left++, right--
   - Worst case becomes O(n)

8. TWO-PASS vs ONE-PASS:
   
   Two-pass:
   - More intuitive: find pivot, then search
   - Easier to explain
   
   One-pass:
   - More elegant
   - Same complexity O(log n)
   - Preferred if you can explain it

9. FINDING THE PIVOT (Minimum Element):
   
   while left < right:
       mid = (left + right) // 2
       if nums[mid] > nums[right]:
           left = mid + 1
       else:
           right = mid
   # left is the index of minimum

10. RELATED PROBLEMS:
    - Search in Rotated Array II (LC 81) - with duplicates
    - Find Minimum in Rotated Array (LC 153)
    - Find Minimum in Rotated Array II (LC 154)

================================================================================
"""
