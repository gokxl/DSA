"""
================================================================================
PROBLEM: Combination Sum (LeetCode 39)
Difficulty: Medium | Pattern: Backtracking
================================================================================

PROBLEM STATEMENT:
Given an array of distinct integers candidates and a target integer target, 
return a list of all unique combinations of candidates where the chosen 
numbers sum to target. You may return the combinations in any order.

The same number may be chosen from candidates an unlimited number of times. 
Two combinations are unique if the frequency of at least one of the chosen 
numbers is different.

EXAMPLES:
    Input: candidates = [2,3,6,7], target = 7
    Output: [[2,2,3],[7]]
    Explanation:
    2 + 2 + 3 = 7
    7 = 7
    These are the only two combinations.

    Input: candidates = [2,3,5], target = 8
    Output: [[2,2,2,2],[2,3,3],[3,5]]

    Input: candidates = [2], target = 1
    Output: []
    No combinations sum to 1.

CONSTRAINTS:
- 1 <= candidates.length <= 30
- 2 <= candidates[i] <= 40
- All elements of candidates are distinct
- 1 <= target <= 40

================================================================================
"""
from typing import List


# ============================================================================
# SOLUTION 1: Backtracking (Classic)
# ============================================================================
def combinationSum(candidates: List[int], target: int) -> List[List[int]]:
    """
    Backtracking with unlimited reuse of elements.
    
    Key: Use start index to avoid duplicates like [2,3] and [3,2].
    Key: DON'T increment index when reusing same element.
    
    Time: O(n^(T/M)) where T=target, M=min candidate
    Space: O(T/M) recursion depth
    """
    result = []
    
    def backtrack(start: int, current: List[int], remaining: int) -> None:
        if remaining == 0:
            result.append(current[:])
            return
        
        if remaining < 0:
            return
        
        for i in range(start, len(candidates)):
            current.append(candidates[i])
            # DON'T move to i+1, stay at i for reuse
            backtrack(i, current, remaining - candidates[i])
            current.pop()
    
    backtrack(0, [], target)
    return result


# ============================================================================
# SOLUTION 2: With Early Termination (Optimized)
# ============================================================================
def combinationSum_optimized(candidates: List[int], target: int) -> List[List[int]]:
    """
    Sort candidates and terminate early when candidate > remaining.
    
    Time: O(n^(T/M)) with better constants
    Space: O(T/M)
    """
    candidates.sort()
    result = []
    
    def backtrack(start: int, current: List[int], remaining: int) -> None:
        if remaining == 0:
            result.append(current[:])
            return
        
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break  # All further candidates too large
            
            current.append(candidates[i])
            backtrack(i, current, remaining - candidates[i])
            current.pop()
    
    backtrack(0, [], target)
    return result


# ============================================================================
# SOLUTION 3: Dynamic Programming (For counting only)
# ============================================================================
def combinationSum_dp_count(candidates: List[int], target: int) -> int:
    """
    DP to count number of combinations (not enumerate).
    Useful as follow-up or for very large targets.
    
    Time: O(n × target)
    Space: O(target)
    """
    # dp[i] = number of ways to make sum i
    dp = [0] * (target + 1)
    dp[0] = 1
    
    for candidate in candidates:
        for i in range(candidate, target + 1):
            dp[i] += dp[i - candidate]
    
    return dp[target]


# ============================================================================
# SOLUTION 4: Iterative with explicit stack
# ============================================================================
def combinationSum_iterative(candidates: List[int], target: int) -> List[List[int]]:
    """
    Iterative approach using stack.
    
    Time: O(n^(T/M))
    Space: O(T/M)
    """
    candidates.sort()
    result = []
    stack = [(0, [], target)]  # (start_index, current_combo, remaining)
    
    while stack:
        start, current, remaining = stack.pop()
        
        if remaining == 0:
            result.append(current)
            continue
        
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break
            
            # Push new state (don't need to backtrack manually)
            stack.append((i, current + [candidates[i]], remaining - candidates[i]))
    
    return result


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Standard case
    candidates1, target1 = [2, 3, 6, 7], 7
    print(f"Candidates: {candidates1}, Target: {target1}")
    print(f"Result: {combinationSum(candidates1, target1)}")
    # Expected: [[2,2,3], [7]]
    print()
    
    # Test Case 2: Multiple combinations
    candidates2, target2 = [2, 3, 5], 8
    print(f"Candidates: {candidates2}, Target: {target2}")
    print(f"Result: {combinationSum_optimized(candidates2, target2)}")
    # Expected: [[2,2,2,2], [2,3,3], [3,5]]
    print()
    
    # Test Case 3: No solution
    candidates3, target3 = [2], 1
    print(f"Candidates: {candidates3}, Target: {target3}")
    print(f"Result: {combinationSum(candidates3, target3)}")
    # Expected: []
    print()
    
    # Test Case 4: Single candidate repeated
    candidates4, target4 = [3], 9
    print(f"Candidates: {candidates4}, Target: {target4}")
    print(f"Result: {combinationSum(candidates4, target4)}")
    # Expected: [[3,3,3]]
    print()
    
    # Test Case 5: Count only
    candidates5, target5 = [2, 3, 5], 8
    print(f"Candidates: {candidates5}, Target: {target5}")
    print(f"Count: {combinationSum_dp_count(candidates5, target5)}")
    # Expected: 3


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. KEY DIFFERENCE FROM REGULAR COMBINATIONS:
   
   Regular: Each element used at most once → backtrack(i+1, ...)
   This problem: Unlimited reuse → backtrack(i, ...)
   
   The "stay at i" allows [2,2,2,...] type combinations.

2. WHY START INDEX?
   
   Prevents duplicates like [2,3] and [3,2].
   We only consider candidates >= current position.
   
   This ensures combinations are in sorted order.

3. EARLY TERMINATION:
   
   Sort candidates first.
   If candidates[i] > remaining, all further are also > remaining.
   
   for i in range(start, len(candidates)):
       if candidates[i] > remaining:
           break  # Not continue!

4. BACKTRACKING TEMPLATE:
   
   def backtrack(start, current, remaining):
       if remaining == 0:
           result.append(current[:])
           return
       
       for i in range(start, n):
           if early_termination_condition:
               break
           
           current.append(candidates[i])
           backtrack(i, current, remaining - candidates[i])  # i, not i+1!
           current.pop()

5. COMBINATION SUM VARIANTS:
   
   LC 39: Unlimited reuse, unique candidates
   LC 40: Each used once, duplicates in candidates
   LC 216: Fixed k numbers, use 1-9, each once
   LC 377: Count combinations (DP)

6. TIME COMPLEXITY ANALYSIS:
   
   Worst case: target filled with smallest candidate
   Depth = target / min(candidates)
   Branching factor = n
   
   Total: O(n^(T/M))

7. DP ALTERNATIVE:
   
   For COUNTING combinations (not enumerating):
   
   dp[i] = number of ways to make sum i
   dp[0] = 1
   
   For each candidate c:
       for i from c to target:
           dp[i] += dp[i - c]

8. COMMON MISTAKES:
   
   ❌ Using i+1 instead of i (doesn't allow reuse)
   ❌ Not using start index (creates duplicates)
   ❌ Forgetting to copy result

9. RELATED PROBLEMS:
   
   - Coin Change (LC 322) - minimum coins
   - Combination Sum II (LC 40)
   - Combination Sum III (LC 216)
   - Perfect Squares (LC 279)

10. practice TIP:
    
    "I'll use backtracking with a start index to avoid duplicates.
    The key insight is that I DON'T increment the index when
    recursing, allowing unlimited reuse of each element.
    
    I'll also sort the candidates first for early termination:
    if a candidate exceeds remaining target, all further ones
    will too, so I break.
    
    Time: O(n^(T/M)) where T is target and M is smallest candidate."

================================================================================
"""
