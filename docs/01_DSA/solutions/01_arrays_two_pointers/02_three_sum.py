"""
================================================================================
PROBLEM: 3Sum (LeetCode 15)
Difficulty: Medium | Pattern: Arrays & Two Pointers
================================================================================

PROBLEM STATEMENT:
Given an integer array `nums`, return all triplets [nums[i], nums[j], nums[k]] 
such that i != j, i != k, j != k, and nums[i] + nums[j] + nums[k] == 0.

REQUIREMENTS:
- Solution set must NOT contain duplicate triplets
- Return triplets in any order

EXAMPLES:
    Input: nums = [-1,0,1,2,-1,-4]
    Output: [[-1,-1,2],[-1,0,1]]
    Explanation: 
        nums[0] + nums[1] + nums[2] = -1 + 0 + 1 = 0
        nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0
        nums[0] + nums[3] + nums[4] = -1 + 2 + (-1) = 0
        The distinct triplets are [-1,0,1] and [-1,-1,2]

    Input: nums = [0,1,1]
    Output: []
    Explanation: No triplets sum to 0

    Input: nums = [0,0,0]
    Output: [[0,0,0]]

CONSTRAINTS:
- 3 <= nums.length <= 3000
- -10^5 <= nums[i] <= 10^5

================================================================================
"""

from typing import List


# ============================================================================
# SOLUTION: Sort + Two Pointers (Optimal)
# ============================================================================
def threeSum(nums: List[int]) -> List[List[int]]:
    """
    1. Sort the array to enable two pointers and handle duplicates
    2. Fix first element, use two pointers for remaining two
    3. Skip duplicates at each level
    
    Time: O(n^2) - O(n log n) sort + O(n^2) two pointers
    Space: O(1) or O(n) depending on sort implementation
    """
    nums.sort()  # Sort to use two pointers and handle duplicates
    result = []
    n = len(nums)
    
    for i in range(n - 2):
        # Skip duplicates for first element
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        
        # Early termination: if smallest number is positive, no solution possible
        if nums[i] > 0:
            break
        
        # Two pointers for remaining two elements
        left, right = i + 1, n - 1
        target = -nums[i]  # We need nums[left] + nums[right] = -nums[i]
        
        while left < right:
            curr_sum = nums[left] + nums[right]
            
            if curr_sum == target:
                result.append([nums[i], nums[left], nums[right]])
                
                # Skip duplicates for second element
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                # Skip duplicates for third element
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                
                # Move both pointers
                left += 1
                right -= 1
                
            elif curr_sum < target:
                left += 1
            else:
                right -= 1
    
    return result


# ============================================================================
# SOLUTION 2: Using HashSet (Alternative, but Two Pointers is preferred)
# ============================================================================
def threeSum_hashset(nums: List[int]) -> List[List[int]]:
    """
    For each pair (i, j), check if -(nums[i] + nums[j]) exists.
    Use set to avoid duplicates.
    
    Time: O(n^2)
    Space: O(n) for the set
    """
    nums.sort()
    result = []
    n = len(nums)
    
    for i in range(n - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
            
        seen = set()
        j = i + 1
        
        while j < n:
            complement = -nums[i] - nums[j]
            
            if complement in seen:
                result.append([nums[i], complement, nums[j]])
                # Skip duplicates
                while j + 1 < n and nums[j] == nums[j + 1]:
                    j += 1
            
            seen.add(nums[j])
            j += 1
    
    return result


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Standard case
    nums1 = [-1, 0, 1, 2, -1, -4]
    print(f"Input: {nums1}")
    print(f"Output: {threeSum(nums1)}")
    # Expected: [[-1,-1,2],[-1,0,1]]
    print()
    
    # Test Case 2: No solution
    nums2 = [0, 1, 1]
    print(f"Input: {nums2}")
    print(f"Output: {threeSum(nums2)}")
    # Expected: []
    print()
    
    # Test Case 3: All zeros
    nums3 = [0, 0, 0]
    print(f"Input: {nums3}")
    print(f"Output: {threeSum(nums3)}")
    # Expected: [[0,0,0]]
    print()
    
    # Test Case 4: Multiple triplets
    nums4 = [-2, 0, 1, 1, 2]
    print(f"Input: {nums4}")
    print(f"Output: {threeSum(nums4)}")
    # Expected: [[-2,0,2],[-2,1,1]]
    print()
    
    # Test Case 5: All positive (no solution)
    nums5 = [1, 2, 3, 4, 5]
    print(f"Input: {nums5}")
    print(f"Output: {threeSum(nums5)}")
    # Expected: []


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. WHY SORT FIRST?
   - Enables two pointers approach
   - Makes duplicate handling easier (consecutive)
   - Early termination when nums[i] > 0

2. DUPLICATE HANDLING IS CRITICAL:
   - Skip duplicates for first element: if i > 0 and nums[i] == nums[i-1]
   - Skip duplicates for second element: while nums[left] == nums[left+1]
   - Skip duplicates for third element: while nums[right] == nums[right-1]

3. REDUCING TO TWO SUM:
   - Fix first element nums[i]
   - Find two numbers that sum to -nums[i]
   - This is the 2Sum II problem (sorted array)

4. OPTIMIZATIONS TO MENTION:
   - Early termination when nums[i] > 0
   - Could also terminate when nums[i] + nums[i+1] + nums[i+2] > 0
   - Could skip when nums[i] + nums[n-2] + nums[n-1] < 0

5. EDGE CASES:
   - All same elements [0,0,0]
   - All positive or all negative
   - Array with length exactly 3
   - Many duplicates

6. FOLLOW-UP: 4Sum
   - Fix two elements, reduce to 2Sum
   - Time: O(n^3)
   - Same duplicate handling pattern

7. TIME/SPACE ANALYSIS:
   - Sorting: O(n log n)
   - Two pointers for each i: O(n)
   - Total: O(n^2)
   - Space: O(1) extra (output doesn't count)

================================================================================
COMMON MISTAKES TO AVOID:
================================================================================
- Forgetting to skip duplicates (results in duplicate triplets)
- Wrong order of operations when skipping duplicates
- Not moving BOTH pointers after finding a valid triplet
- Off-by-one errors in duplicate skipping (left+1 vs left)

================================================================================
"""
