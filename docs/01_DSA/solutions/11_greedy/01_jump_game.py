"""
================================================================================
PROBLEM: Jump Game (LeetCode 55)
Difficulty: Medium | Pattern: Greedy
================================================================================

PROBLEM STATEMENT:
You are given an integer array nums. You are initially positioned at the array's 
first index, and each element in the array represents your maximum jump length 
at that position.

Return true if you can reach the last index, or false otherwise.

EXAMPLES:
    Input: nums = [2,3,1,1,4]
    Output: true
    Explanation: Jump 1 step from index 0 to 1, then 3 steps to the last index.

    Input: nums = [3,2,1,0,4]
    Output: false
    Explanation: You will always arrive at index 3. Its maximum jump length is 0,
    which makes it impossible to reach the last index.

CONSTRAINTS:
- 1 <= nums.length <= 10^4
- 0 <= nums[i] <= 10^5

================================================================================
"""
from typing import List


# ============================================================================
# SOLUTION 1: Greedy (Forward - Track max reach)
# ============================================================================
def canJump(nums: List[int]) -> bool:
    """
    Track the farthest index we can reach.
    If current index exceeds max_reach, we're stuck.
    
    Time: O(n)
    Space: O(1)
    """
    max_reach = 0
    
    for i in range(len(nums)):
        if i > max_reach:
            return False
        max_reach = max(max_reach, i + nums[i])
        
        # Early termination
        if max_reach >= len(nums) - 1:
            return True
    
    return True


# ============================================================================
# SOLUTION 2: Greedy (Backward - Track good position)
# ============================================================================
def canJump_backward(nums: List[int]) -> bool:
    """
    Work backward: find positions that can reach the goal.
    Update goal to nearest such position.
    
    Time: O(n)
    Space: O(1)
    """
    goal = len(nums) - 1
    
    for i in range(len(nums) - 2, -1, -1):
        if i + nums[i] >= goal:
            goal = i
    
    return goal == 0


# ============================================================================
# SOLUTION 3: DP (Less efficient but educational)
# ============================================================================
def canJump_dp(nums: List[int]) -> bool:
    """
    dp[i] = True if we can reach index i
    
    Time: O(n²) - slower than greedy
    Space: O(n)
    """
    n = len(nums)
    dp = [False] * n
    dp[0] = True
    
    for i in range(1, n):
        for j in range(i - 1, -1, -1):
            if dp[j] and j + nums[j] >= i:
                dp[i] = True
                break
    
    return dp[n - 1]


# ============================================================================
# SOLUTION 4: BFS (Graph interpretation)
# ============================================================================
from collections import deque

def canJump_bfs(nums: List[int]) -> bool:
    """
    Treat as graph: index i has edges to i+1, i+2, ..., i+nums[i]
    BFS to find if last index is reachable.
    
    Time: O(n)
    Space: O(n)
    """
    n = len(nums)
    if n == 1:
        return True
    
    visited = [False] * n
    queue = deque([0])
    visited[0] = True
    
    while queue:
        i = queue.popleft()
        
        for j in range(i + 1, min(i + nums[i] + 1, n)):
            if j == n - 1:
                return True
            if not visited[j]:
                visited[j] = True
                queue.append(j)
    
    return False


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Can reach
    nums1 = [2, 3, 1, 1, 4]
    print(f"nums = {nums1}")
    print(f"Greedy Forward: {canJump(nums1)}")
    print(f"Greedy Backward: {canJump_backward(nums1)}")
    # Expected: True
    print()
    
    # Test Case 2: Cannot reach
    nums2 = [3, 2, 1, 0, 4]
    print(f"nums = {nums2}")
    print(f"Result: {canJump(nums2)}")
    # Expected: False
    print()
    
    # Test Case 3: Single element
    nums3 = [0]
    print(f"nums = {nums3}")
    print(f"Result: {canJump(nums3)}")
    # Expected: True (already at last index)
    print()
    
    # Test Case 4: All zeros except first
    nums4 = [1, 0, 0, 0]
    print(f"nums = {nums4}")
    print(f"Result: {canJump(nums4)}")
    # Expected: False
    print()
    
    # Test Case 5: Large jump at start
    nums5 = [10, 0, 0, 0, 0]
    print(f"nums = {nums5}")
    print(f"Result: {canJump(nums5)}")
    # Expected: True


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. GREEDY INSIGHT:
   
   At each position, update the farthest we can reach.
   
   max_reach = max(max_reach, i + nums[i])
   
   If we can't reach current position, we're stuck!

2. WHY GREEDY WORKS:
   
   If we can reach position i, we can also reach all positions < i.
   
   So tracking max_reach captures all reachable positions.
   No need to explore all paths.

3. BACKWARD APPROACH:
   
   Alternative: work backward from goal.
   
   If position i can reach the goal, i becomes new goal.
   Final check: can we reach goal from position 0?

4. FORWARD VS BACKWARD:
   
   Forward: "How far can I go?"
   Backward: "Where can I come from?"
   
   Both O(n), same idea different perspective.

5. COMMON PATTERN:
   
   Many jump problems use this max_reach pattern:
   - Jump Game II (min jumps)
   - Frog Jump
   - Video Stitching

6. GRAPH INTERPRETATION:
   
   Think of it as reachability in a DAG.
   Edge from i to j if j <= i + nums[i].
   
   But greedy is simpler and faster!

7. EDGE CASES:
   
   - Single element: always True (already at end)
   - nums[0] = 0 and n > 1: always False
   - All zeros: False if n > 1

8. COMMON MISTAKES:
   
   ❌ Using BFS/DFS when greedy works
   ❌ Not handling single element case
   ❌ Off-by-one in max_reach comparison

9. RELATED PROBLEMS:
   
   - Jump Game II (LC 45) - min jumps
   - Jump Game III (LC 1306) - can jump left/right
   - Jump Game IV (LC 1345) - same value jumps

10. practice TIP:
    
    "I'll use greedy. At each position, I track the maximum
    index I can reach. If I ever reach a position beyond
    max_reach, I'm stuck.
    
    max_reach = max(max_reach, i + nums[i])
    
    If max_reach >= n-1, I can reach the end.
    Time: O(n), Space: O(1)."
    
    Mention the backward approach as alternative!

================================================================================
"""
