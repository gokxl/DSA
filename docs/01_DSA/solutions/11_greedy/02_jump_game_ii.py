"""
================================================================================
PROBLEM: Jump Game II (LeetCode 45)
Difficulty: Medium | Pattern: Greedy/BFS
================================================================================

PROBLEM STATEMENT:
You are given a 0-indexed array of integers nums of length n. You are initially 
positioned at nums[0].

Each element nums[i] represents the maximum length of a forward jump from index i. 
In other words, if you are at nums[i], you can jump to any nums[i + j] where:
- 0 <= j <= nums[i] and
- i + j < n

Return the minimum number of jumps to reach nums[n - 1]. The test cases are 
generated such that you can reach nums[n - 1].

EXAMPLES:
    Input: nums = [2,3,1,1,4]
    Output: 2
    Explanation: The minimum number of jumps to reach the last index is 2. 
    Jump 1 step from index 0 to 1, then 3 steps to the last index.

    Input: nums = [2,3,0,1,4]
    Output: 2

CONSTRAINTS:
- 1 <= nums.length <= 10^4
- 0 <= nums[i] <= 1000
- It's guaranteed that you can reach nums[n - 1]

================================================================================
"""
from typing import List


# ============================================================================
# SOLUTION 1: Greedy (Optimal)
# ============================================================================
def jump(nums: List[int]) -> int:
    """
    Track current jump's boundary and farthest we can reach.
    When we reach current boundary, we must jump.
    
    Time: O(n)
    Space: O(1)
    """
    n = len(nums)
    if n <= 1:
        return 0
    
    jumps = 0
    current_end = 0  # End of current jump range
    farthest = 0     # Farthest we can reach
    
    for i in range(n - 1):  # Don't need to jump from last index
        farthest = max(farthest, i + nums[i])
        
        if i == current_end:  # Must jump
            jumps += 1
            current_end = farthest
            
            if current_end >= n - 1:
                break
    
    return jumps


# ============================================================================
# SOLUTION 2: BFS Level-Order
# ============================================================================
def jump_bfs(nums: List[int]) -> int:
    """
    BFS: Each level represents one jump.
    Find minimum levels (jumps) to reach end.
    
    Time: O(n)
    Space: O(1)
    """
    n = len(nums)
    if n <= 1:
        return 0
    
    level = 0
    current_end = 0
    next_end = 0
    i = 0
    
    while current_end < n - 1:
        level += 1
        # Explore all nodes in current level
        while i <= current_end:
            next_end = max(next_end, i + nums[i])
            i += 1
        current_end = next_end
    
    return level


# ============================================================================
# SOLUTION 3: DP (Less efficient)
# ============================================================================
def jump_dp(nums: List[int]) -> int:
    """
    dp[i] = minimum jumps to reach index i
    
    Time: O(n²)
    Space: O(n)
    """
    n = len(nums)
    dp = [float('inf')] * n
    dp[0] = 0
    
    for i in range(n):
        for j in range(1, nums[i] + 1):
            if i + j < n:
                dp[i + j] = min(dp[i + j], dp[i] + 1)
    
    return dp[n - 1]


# ============================================================================
# SOLUTION 4: Greedy with explicit tracking
# ============================================================================
def jump_explicit(nums: List[int]) -> int:
    """
    More explicit version with clear variables.
    
    Time: O(n)
    Space: O(1)
    """
    n = len(nums)
    if n <= 1:
        return 0
    
    jumps = 0
    left = 0   # Start of current jump range
    right = 0  # End of current jump range
    
    while right < n - 1:
        farthest = 0
        for i in range(left, right + 1):
            farthest = max(farthest, i + nums[i])
        
        left = right + 1
        right = farthest
        jumps += 1
    
    return jumps


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Standard case
    nums1 = [2, 3, 1, 1, 4]
    print(f"nums = {nums1}")
    print(f"Greedy: {jump(nums1)}")
    print(f"BFS: {jump_bfs(nums1)}")
    # Expected: 2 (0 -> 1 -> 4)
    print()
    
    # Test Case 2: With zero
    nums2 = [2, 3, 0, 1, 4]
    print(f"nums = {nums2}")
    print(f"Result: {jump(nums2)}")
    # Expected: 2
    print()
    
    # Test Case 3: Single element
    nums3 = [0]
    print(f"nums = {nums3}")
    print(f"Result: {jump(nums3)}")
    # Expected: 0
    print()
    
    # Test Case 4: All ones
    nums4 = [1, 1, 1, 1, 1]
    print(f"nums = {nums4}")
    print(f"Result: {jump(nums4)}")
    # Expected: 4
    print()
    
    # Test Case 5: Large first jump
    nums5 = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    print(f"nums = {nums5}")
    print(f"Result: {jump(nums5)}")
    # Expected: 1


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. GREEDY INSIGHT:
   
   Within each jump's range, find the farthest we can reach.
   Jump to that position (implicitly).
   
   current_end = boundary of current jump
   farthest = max reach from positions in current jump

2. WHY GREEDY IS OPTIMAL:
   
   From positions 0 to current_end, we pick the one
   that reaches farthest. This gives minimum jumps.
   
   Any other choice would reach less far or equal,
   so it can't be better.

3. WHEN TO JUMP:
   
   When we reach current_end (i == current_end),
   we must make our next jump.
   
   Update: current_end = farthest

4. BFS INTERPRETATION:
   
   Level 0: [0]
   Level 1: [1, 2, ..., nums[0]]
   Level 2: Farthest reachable from level 1
   
   Number of levels = minimum jumps

5. DON'T ITERATE TO n-1:
   
   Stop at n-2! We don't need to process the last index.
   
   If farthest >= n-1, we're done.

6. DIFFERENCE FROM JUMP GAME I:
   
   Jump Game I: Can we reach end? (boolean)
   Jump Game II: Minimum jumps to reach end (count)
   
   Same greedy pattern, but counting jumps.

7. TIME/SPACE:
   
   Greedy: O(n) time, O(1) space
   DP: O(n²) time, O(n) space
   
   Greedy is clearly better!

8. COMMON MISTAKES:
   
   ❌ Iterating to n-1 instead of n-2
   ❌ Not handling single element
   ❌ Counting jumps incorrectly

9. RELATED PROBLEMS:
   
   - Jump Game (LC 55)
   - Jump Game III (LC 1306)
   - Video Stitching (LC 1024)

10. practice TIP:
    
    "I'll use greedy. I track two things:
    1. current_end: boundary of current jump
    2. farthest: max reach from current range
    
    When I reach current_end, I must jump.
    The jump count increases, and current_end becomes farthest.
    
    I iterate to n-2 because I don't need to jump FROM the last index.
    
    Time: O(n), Space: O(1)."
    
    Draw the BFS level interpretation if asked!

================================================================================
"""
