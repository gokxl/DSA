"""
================================================================================
PROBLEM: Permutations (LeetCode 46)
Difficulty: Medium | Pattern: Backtracking
================================================================================

PROBLEM STATEMENT:
Given an array nums of distinct integers, return all the possible permutations.
You can return the answer in any order.

EXAMPLES:
    Input: nums = [1,2,3]
    Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
    
    Input: nums = [0,1]
    Output: [[0,1],[1,0]]
    
    Input: nums = [1]
    Output: [[1]]

CONSTRAINTS:
- 1 <= nums.length <= 6
- -10 <= nums[i] <= 10
- All the integers of nums are unique

================================================================================
"""
from typing import List


# ============================================================================
# SOLUTION 1: Backtracking with Used Array
# ============================================================================
def permute_used(nums: List[int]) -> List[List[int]]:
    """
    Classic backtracking with used[] array.
    
    Time: O(n! × n)
    Space: O(n) for recursion and used array
    """
    result = []
    used = [False] * len(nums)
    
    def backtrack(current: List[int]) -> None:
        if len(current) == len(nums):
            result.append(current[:])
            return
        
        for i in range(len(nums)):
            if used[i]:
                continue
            
            used[i] = True
            current.append(nums[i])
            backtrack(current)
            current.pop()
            used[i] = False
    
    backtrack([])
    return result


# ============================================================================
# SOLUTION 2: Backtracking with Swapping
# ============================================================================
def permute_swap(nums: List[int]) -> List[List[int]]:
    """
    Swap elements to generate permutations in-place.
    
    At position i, swap with each position j >= i.
    
    Time: O(n! × n)
    Space: O(n) for recursion
    """
    result = []
    
    def backtrack(first: int) -> None:
        if first == len(nums):
            result.append(nums[:])
            return
        
        for i in range(first, len(nums)):
            nums[first], nums[i] = nums[i], nums[first]  # Swap
            backtrack(first + 1)
            nums[first], nums[i] = nums[i], nums[first]  # Backtrack
    
    backtrack(0)
    return result


# ============================================================================
# SOLUTION 3: Iterative
# ============================================================================
def permute_iterative(nums: List[int]) -> List[List[int]]:
    """
    Build permutations iteratively.
    
    Insert each new number at all positions of existing permutations.
    
    Time: O(n! × n)
    Space: O(n!)
    """
    result = [[]]
    
    for num in nums:
        new_result = []
        for perm in result:
            # Insert num at each position
            for i in range(len(perm) + 1):
                new_result.append(perm[:i] + [num] + perm[i:])
        result = new_result
    
    return result


# ============================================================================
# SOLUTION 4: Using Set for tracking
# ============================================================================
def permute_set(nums: List[int]) -> List[List[int]]:
    """
    Use set to track remaining elements.
    
    Time: O(n! × n)
    Space: O(n)
    """
    result = []
    
    def backtrack(current: List[int], remaining: set) -> None:
        if not remaining:
            result.append(current[:])
            return
        
        for num in list(remaining):  # Copy since we modify
            current.append(num)
            remaining.remove(num)
            backtrack(current, remaining)
            remaining.add(num)
            current.pop()
    
    backtrack([], set(nums))
    return result


# ============================================================================
# SOLUTION 5: Using Python's itertools (for reference)
# ============================================================================
from itertools import permutations as perm

def permute_builtin(nums: List[int]) -> List[List[int]]:
    """
    Using Python's itertools.permutations.
    
    Less common, but good to know.
    """
    return [list(p) for p in perm(nums)]


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Standard case
    nums1 = [1, 2, 3]
    print(f"nums = {nums1}")
    print(f"Used array: {permute_used(nums1)}")
    print(f"Swap: {permute_swap(nums1.copy())}")
    print(f"Iterative: {permute_iterative(nums1)}")
    # Expected: 6 permutations
    print()
    
    # Test Case 2: Two elements
    nums2 = [0, 1]
    print(f"nums = {nums2}")
    print(f"Result: {permute_used(nums2)}")
    # Expected: [[0,1], [1,0]]
    print()
    
    # Test Case 3: Single element
    nums3 = [1]
    print(f"nums = {nums3}")
    print(f"Result: {permute_swap(nums3)}")
    # Expected: [[1]]
    print()
    
    # Test Case 4: Negative numbers
    nums4 = [-1, 0, 1]
    print(f"nums = {nums4}")
    print(f"Result: {permute_set(nums4)}")
    print()


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. PERMUTATIONS VS SUBSETS:
   
   Subsets: Order doesn't matter, use start index
   Permutations: Order matters, use "used" tracking
   
   [1,2] and [2,1] are:
   - Same subset ✓
   - Different permutations ✓

2. TWO MAIN APPROACHES:
   
   a) Used Array:
      - Track which elements are used
      - Try each unused element at current position
      
   b) Swapping:
      - At position i, swap with each j >= i
      - More space efficient (no used array)

3. SWAPPING VISUALIZATION:
   
   [1,2,3] at position 0:
   - Swap(0,0): [1,2,3] → recurse
   - Swap(0,1): [2,1,3] → recurse
   - Swap(0,2): [3,2,1] → recurse
   
   Each generates n-1 more permutations

4. TIME COMPLEXITY:
   
   n! permutations, O(n) to copy each
   Total: O(n! × n)
   
   For n=6: 6! = 720 permutations

5. ITERATIVE APPROACH:
   
   Start: [[]]
   Add 1: [[1]]
   Add 2: [[2,1], [1,2]]
   Add 3: [[3,2,1], [2,3,1], [2,1,3], [3,1,2], [1,3,2], [1,2,3]]
   
   Insert new element at every position

6. COMMON MISTAKES:
   
   ❌ Using start index (that's for combinations!)
   ❌ Forgetting to mark used back to False
   ❌ Not copying the result (result.append(current[:]))

7. FOLLOW-UP: WITH DUPLICATES (LC 47):
   
   Sort first, then skip duplicate branches:
   
   if i > 0 and nums[i] == nums[i-1] and not used[i-1]:
       continue

8. RELATED PROBLEMS:
   
   - Permutations II (LC 47) - with duplicates
   - Next Permutation (LC 31)
   - Permutation Sequence (LC 60)

9. N! GROWTH:
   
   n = 1: 1
   n = 3: 6
   n = 5: 120
   n = 10: 3,628,800
   
   Grows VERY fast!

10. HOW TO EXPLAIN IT:
    
    "I'll use backtracking with a used[] array.
    At each position, I try each unused element.
    
    Alternatively, I can swap: at position i, I swap with
    each position j >= i to generate all orderings.
    
    Time is O(n! × n) since there are n! permutations
    and each takes O(n) to copy."
    
    The swap approach is elegant - mention it!

================================================================================
"""
