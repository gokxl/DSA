"""
================================================================================
PROBLEM: Subsets (LeetCode 78)
Difficulty: Medium | Pattern: Backtracking
================================================================================

PROBLEM STATEMENT:
Given an integer array nums of unique elements, return all possible subsets 
(the power set).

The solution set must not contain duplicate subsets. Return the solution in 
any order.

EXAMPLES:
    Input: nums = [1,2,3]
    Output: [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]
    
    Input: nums = [0]
    Output: [[],[0]]

CONSTRAINTS:
- 1 <= nums.length <= 10
- -10 <= nums[i] <= 10
- All the numbers of nums are unique

================================================================================
"""
from typing import List


# ============================================================================
# SOLUTION 1: Backtracking (Classic)
# ============================================================================
def subsets_backtrack(nums: List[int]) -> List[List[int]]:
    """
    Backtracking approach - for each element, decide include/exclude.
    
    Time: O(n × 2^n) - 2^n subsets, O(n) to copy each
    Space: O(n) for recursion depth
    """
    result = []
    
    def backtrack(start: int, current: List[int]) -> None:
        # Add current subset (every path is valid)
        result.append(current[:])  # Copy!
        
        # Try adding each remaining element
        for i in range(start, len(nums)):
            current.append(nums[i])
            backtrack(i + 1, current)  # Move to next index
            current.pop()  # Backtrack
    
    backtrack(0, [])
    return result


# ============================================================================
# SOLUTION 2: Iterative (Cascading)
# ============================================================================
def subsets_iterative(nums: List[int]) -> List[List[int]]:
    """
    Build subsets iteratively by adding each number to existing subsets.
    
    Start: [[]]
    Add 1: [[], [1]]
    Add 2: [[], [1], [2], [1,2]]
    Add 3: [[], [1], [2], [1,2], [3], [1,3], [2,3], [1,2,3]]
    
    Time: O(n × 2^n)
    Space: O(n × 2^n) for result
    """
    result = [[]]
    
    for num in nums:
        # Add num to each existing subset
        result += [subset + [num] for subset in result]
    
    return result


# ============================================================================
# SOLUTION 3: Bit Manipulation
# ============================================================================
def subsets_bitmask(nums: List[int]) -> List[List[int]]:
    """
    Use bitmask to represent subset.
    
    For n elements, there are 2^n subsets.
    Each number from 0 to 2^n-1 represents a subset:
    - Bit i = 1 means include nums[i]
    
    Example for [1,2,3]:
    000 -> []
    001 -> [1]
    010 -> [2]
    011 -> [1,2]
    100 -> [3]
    ...
    
    Time: O(n × 2^n)
    Space: O(n) per subset
    """
    n = len(nums)
    result = []
    
    for mask in range(1 << n):  # 0 to 2^n - 1
        subset = []
        for i in range(n):
            if mask & (1 << i):  # Check if bit i is set
                subset.append(nums[i])
        result.append(subset)
    
    return result


# ============================================================================
# SOLUTION 4: Backtracking with explicit include/exclude
# ============================================================================
def subsets_include_exclude(nums: List[int]) -> List[List[int]]:
    """
    Binary tree approach - at each position, branch include/exclude.
    
    Time: O(n × 2^n)
    Space: O(n) recursion
    """
    result = []
    
    def dfs(index: int, current: List[int]) -> None:
        if index == len(nums):
            result.append(current[:])
            return
        
        # Exclude nums[index]
        dfs(index + 1, current)
        
        # Include nums[index]
        current.append(nums[index])
        dfs(index + 1, current)
        current.pop()
    
    dfs(0, [])
    return result


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Standard case
    nums1 = [1, 2, 3]
    print(f"nums = {nums1}")
    print(f"Backtrack: {subsets_backtrack(nums1)}")
    print(f"Iterative: {subsets_iterative(nums1)}")
    print(f"Bitmask: {subsets_bitmask(nums1)}")
    # Expected: 8 subsets total
    print()
    
    # Test Case 2: Single element
    nums2 = [0]
    print(f"nums = {nums2}")
    print(f"Result: {subsets_backtrack(nums2)}")
    # Expected: [[], [0]]
    print()
    
    # Test Case 3: Two elements
    nums3 = [1, 2]
    print(f"nums = {nums3}")
    print(f"Result: {subsets_include_exclude(nums3)}")
    # Expected: [[], [1], [2], [1,2]]
    print()
    
    # Test Case 4: Negative numbers
    nums4 = [-1, 0, 1]
    print(f"nums = {nums4}")
    print(f"Result: {subsets_backtrack(nums4)}")
    print()


r"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. BACKTRACKING TEMPLATE FOR SUBSETS:
   
   def backtrack(start, current):
       result.append(current[:])  # Add every subset
       
       for i in range(start, len(nums)):
           current.append(nums[i])
           backtrack(i + 1, current)
           current.pop()
   
   Key: start index prevents duplicates like [2,1]

2. WHY EVERY PATH IS VALID:
   
   Unlike combinations (fixed k) or permutations (use all),
   subsets can be ANY length from 0 to n.
   
   Add to result at START of function, not just at leaves.

3. CASCADING PATTERN:
   
   Start with [[]]
   For each num, add it to ALL existing subsets
   
   This doubles the count each time → 2^n total

4. BITMASK INTUITION:
   
   n elements → 2^n subsets
   Each subset = binary number from 0 to 2^n-1
   
   Bit i set = include element i
   
   Very clean and O(1) per element check!

5. TIME/SPACE COMPLEXITY:
   
   Time: O(n × 2^n)
   - 2^n subsets
   - O(n) to copy each subset
   
   Space: O(n) for recursion (not counting result)

6. INCLUDE/EXCLUDE TREE:
   
          []
        /    \
      []      [1]
     / \      / \
   []  [2] [1] [1,2]
   ...
   
   Binary tree with 2^n leaves

7. COMMON MISTAKES:
   
   ❌ Forgetting to copy (result.append(current[:]))
   ❌ Not incrementing start index → duplicates
   ❌ Only adding at leaves → missing partial subsets

8. FOLLOW-UP: SUBSETS WITH DUPLICATES (LC 90):
   
   Sort input first, then skip duplicates:
   
   if i > start and nums[i] == nums[i-1]:
       continue

9. RELATED PROBLEMS:
   
   - Subsets II (LC 90) - with duplicates
   - Combinations (LC 77)
   - Permutations (LC 46)
   - Combination Sum (LC 39)

10. HOW TO EXPLAIN IT:
    
    "I'll use backtracking. At each position, I add the current
    subset to result (every subset is valid), then try adding
    each remaining element.
    
    The key is using a 'start' index to avoid duplicates like
    [2,1] when we already have [1,2].
    
    Time is O(n × 2^n) for 2^n subsets, each taking O(n) to copy."
    
    Know bitmask approach too - some interviewers love it!

================================================================================
"""
