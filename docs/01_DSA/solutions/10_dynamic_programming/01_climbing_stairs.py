"""
================================================================================
PROBLEM: Climbing Stairs (LeetCode 70)
Difficulty: Easy | Pattern: DP (1D)
================================================================================

PROBLEM STATEMENT:
You are climbing a staircase. It takes n steps to reach the top.

Each time you can either climb 1 or 2 steps. In how many distinct ways can 
you climb to the top?

EXAMPLES:
    Input: n = 2
    Output: 2
    Explanation: There are two ways:
    1. 1 step + 1 step
    2. 2 steps

    Input: n = 3
    Output: 3
    Explanation: There are three ways:
    1. 1 step + 1 step + 1 step
    2. 1 step + 2 steps
    3. 2 steps + 1 step

CONSTRAINTS:
- 1 <= n <= 45

================================================================================
"""


# ============================================================================
# SOLUTION 1: Dynamic Programming (Bottom-Up)
# ============================================================================
def climbStairs_dp(n: int) -> int:
    """
    DP: dp[i] = ways to reach step i
    dp[i] = dp[i-1] + dp[i-2] (come from 1 or 2 steps before)
    
    This is the Fibonacci sequence!
    
    Time: O(n)
    Space: O(n)
    """
    if n <= 2:
        return n
    
    dp = [0] * (n + 1)
    dp[1] = 1
    dp[2] = 2
    
    for i in range(3, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    
    return dp[n]


# ============================================================================
# SOLUTION 2: Space Optimized DP
# ============================================================================
def climbStairs_optimized(n: int) -> int:
    """
    Only need last two values, so use two variables.
    
    Time: O(n)
    Space: O(1)
    """
    if n <= 2:
        return n
    
    prev2, prev1 = 1, 2  # dp[1], dp[2]
    
    for i in range(3, n + 1):
        current = prev1 + prev2
        prev2 = prev1
        prev1 = current
    
    return prev1


# ============================================================================
# SOLUTION 3: Recursion with Memoization (Top-Down)
# ============================================================================
def climbStairs_memo(n: int) -> int:
    """
    Top-down approach with memoization.
    
    Time: O(n)
    Space: O(n)
    """
    from functools import lru_cache
    
    @lru_cache(maxsize=None)
    def climb(i: int) -> int:
        if i <= 2:
            return i
        return climb(i - 1) + climb(i - 2)
    
    return climb(n)


# ============================================================================
# SOLUTION 4: Matrix Exponentiation (O(log n))
# ============================================================================
def climbStairs_matrix(n: int) -> int:
    """
    Use matrix exponentiation for O(log n) time.
    
    [F(n+1)]   [1 1]^n   [F(1)]
    [F(n)  ] = [1 0]   × [F(0)]
    
    Time: O(log n)
    Space: O(1)
    """
    def multiply(A, B):
        return [
            [A[0][0] * B[0][0] + A[0][1] * B[1][0],
             A[0][0] * B[0][1] + A[0][1] * B[1][1]],
            [A[1][0] * B[0][0] + A[1][1] * B[1][0],
             A[1][0] * B[0][1] + A[1][1] * B[1][1]]
        ]
    
    def matrix_power(M, p):
        result = [[1, 0], [0, 1]]  # Identity matrix
        
        while p > 0:
            if p % 2 == 1:
                result = multiply(result, M)
            M = multiply(M, M)
            p //= 2
        
        return result
    
    if n <= 2:
        return n
    
    M = [[1, 1], [1, 0]]
    result = matrix_power(M, n)
    
    return result[0][0]


# ============================================================================
# SOLUTION 5: Binet's Formula (Closed Form)
# ============================================================================
def climbStairs_formula(n: int) -> int:
    """
    Use Fibonacci closed-form formula.
    
    F(n) = (phi^n - psi^n) / sqrt(5)
    where phi = (1 + sqrt(5)) / 2
    
    Time: O(1) if we ignore pow complexity
    Space: O(1)
    
    Note: May have precision issues for large n
    """
    import math
    
    sqrt5 = math.sqrt(5)
    phi = (1 + sqrt5) / 2
    psi = (1 - sqrt5) / 2
    
    # Climbing stairs is F(n+1), not F(n)
    return round((phi ** (n + 1) - psi ** (n + 1)) / sqrt5)


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test cases
    for n in [1, 2, 3, 4, 5, 10, 20, 45]:
        dp = climbStairs_dp(n)
        opt = climbStairs_optimized(n)
        memo = climbStairs_memo(n)
        
        print(f"n = {n}: DP = {dp}, Optimized = {opt}, Memo = {memo}")
    
    print()
    
    # Verify with matrix and formula
    print("Comparing methods for n = 10:")
    print(f"DP: {climbStairs_dp(10)}")
    print(f"Matrix: {climbStairs_matrix(10)}")
    print(f"Formula: {climbStairs_formula(10)}")


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. THIS IS FIBONACCI:
   
   Ways to reach step n = ways from n-1 + ways from n-2
   
   dp[n] = dp[n-1] + dp[n-2]
   
   Same recurrence as Fibonacci!

2. BASE CASES:
   
   dp[1] = 1 (one way: 1 step)
   dp[2] = 2 (two ways: 1+1 or 2)
   
   Or: dp[0] = 1, dp[1] = 1 (treating 0 as ground)

3. SPACE OPTIMIZATION:
   
   Only need last 2 values → O(1) space
   
   prev2, prev1 = 1, 2
   for i in range(3, n+1):
       prev2, prev1 = prev1, prev1 + prev2

4. TOP-DOWN VS BOTTOM-UP:
   
   Top-down (memoization): Start from n, recursively compute
   Bottom-up (tabulation): Start from base cases, build up
   
   Both O(n) time, but bottom-up often faster (no recursion overhead)

5. MATRIX EXPONENTIATION:
   
   For O(log n) time! Useful for very large n.
   
   [F(n+1)]   [1 1]^n
   [F(n)  ] = [1 0]
   
   Use binary exponentiation for O(log n).

6. FOLLOW-UP: K STEPS AT A TIME:
   
   If can take 1, 2, ..., k steps:
   dp[i] = sum(dp[i-j] for j in range(1, k+1))
   
   Time: O(n × k)
   Can optimize to O(n) with sliding window.

7. SIMILAR PROBLEMS:
   
   - House Robber (LC 198)
   - Decode Ways (LC 91)
   - Min Cost Climbing Stairs (LC 746)

8. COMMON MISTAKES:
   
   ❌ Starting loop from wrong index
   ❌ Wrong base cases
   ❌ Off-by-one errors in space optimization

9. INTUITION:
   
   At step n, you either:
   - Took 1 step from n-1 (dp[n-1] ways)
   - Took 2 steps from n-2 (dp[n-2] ways)
   
   Total = sum of both possibilities

10. HOW TO EXPLAIN IT:
    
    "This is essentially Fibonacci. Each step can be reached
    from 1 step before or 2 steps before.
    
    dp[i] = dp[i-1] + dp[i-2]
    
    I can optimize space to O(1) since I only need the
    last two values. For O(log n) time, I could use
    matrix exponentiation."
    
    Mention the Fibonacci connection immediately!

================================================================================
"""
