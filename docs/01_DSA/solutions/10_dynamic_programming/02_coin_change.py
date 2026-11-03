"""
================================================================================
PROBLEM: Coin Change (LeetCode 322)
Difficulty: Medium | Pattern: DP (Unbounded Knapsack)
================================================================================

PROBLEM STATEMENT:
You are given an integer array coins representing coins of different 
denominations and an integer amount representing a total amount of money.

Return the fewest number of coins that you need to make up that amount. 
If that amount of money cannot be made up by any combination of the coins, 
return -1.

You may assume that you have an infinite number of each kind of coin.

EXAMPLES:
    Input: coins = [1,2,5], amount = 11
    Output: 3
    Explanation: 11 = 5 + 5 + 1

    Input: coins = [2], amount = 3
    Output: -1

    Input: coins = [1], amount = 0
    Output: 0

CONSTRAINTS:
- 1 <= coins.length <= 12
- 1 <= coins[i] <= 2^31 - 1
- 0 <= amount <= 10^4

================================================================================
"""
from typing import List


# ============================================================================
# SOLUTION 1: Bottom-Up DP
# ============================================================================
def coinChange(coins: List[int], amount: int) -> int:
    """
    dp[i] = minimum coins needed to make amount i
    
    For each amount, try each coin and take minimum.
    
    Time: O(amount × n) where n = number of coin types
    Space: O(amount)
    """
    # dp[i] = min coins for amount i
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0  # Base case: 0 coins for amount 0
    
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i and dp[i - coin] != float('inf'):
                dp[i] = min(dp[i], dp[i - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1


# ============================================================================
# SOLUTION 2: BFS (Shortest Path)
# ============================================================================
from collections import deque

def coinChange_bfs(coins: List[int], amount: int) -> int:
    """
    Think of it as shortest path problem.
    
    Each amount is a node, each coin is an edge.
    BFS finds shortest path (minimum coins).
    
    Time: O(amount × n)
    Space: O(amount)
    """
    if amount == 0:
        return 0
    
    visited = [False] * (amount + 1)
    queue = deque([0])
    visited[0] = True
    steps = 0
    
    while queue:
        steps += 1
        size = len(queue)
        
        for _ in range(size):
            curr = queue.popleft()
            
            for coin in coins:
                next_amount = curr + coin
                
                if next_amount == amount:
                    return steps
                
                if next_amount < amount and not visited[next_amount]:
                    visited[next_amount] = True
                    queue.append(next_amount)
    
    return -1


# ============================================================================
# SOLUTION 3: Top-Down DP with Memoization
# ============================================================================
def coinChange_memo(coins: List[int], amount: int) -> int:
    """
    Top-down approach with memoization.
    
    Time: O(amount × n)
    Space: O(amount)
    """
    from functools import lru_cache
    
    @lru_cache(maxsize=None)
    def dp(remain: int) -> int:
        if remain < 0:
            return float('inf')
        if remain == 0:
            return 0
        
        min_coins = float('inf')
        for coin in coins:
            result = dp(remain - coin)
            min_coins = min(min_coins, result + 1)
        
        return min_coins
    
    result = dp(amount)
    return result if result != float('inf') else -1


# ============================================================================
# SOLUTION 4: Optimized with Early Termination
# ============================================================================
def coinChange_optimized(coins: List[int], amount: int) -> int:
    """
    Same DP but with coins sorted for potential optimization.
    
    Time: O(amount × n)
    Space: O(amount)
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    # Sort coins in descending order for potential early termination
    coins = sorted(coins, reverse=True)
    
    for i in range(1, amount + 1):
        for coin in coins:
            if coin > i:
                continue
            if dp[i - coin] == float('inf'):
                continue
            
            dp[i] = min(dp[i], dp[i - coin] + 1)
            
            # If we found a solution, larger coins won't help
            if dp[i] == dp[i - coin] + 1:
                break
    
    return dp[amount] if dp[amount] != float('inf') else -1


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Standard case
    coins1, amount1 = [1, 2, 5], 11
    print(f"Coins: {coins1}, Amount: {amount1}")
    print(f"DP: {coinChange(coins1, amount1)}")
    print(f"BFS: {coinChange_bfs(coins1, amount1)}")
    print(f"Memo: {coinChange_memo(coins1, amount1)}")
    # Expected: 3 (5 + 5 + 1)
    print()
    
    # Test Case 2: Impossible
    coins2, amount2 = [2], 3
    print(f"Coins: {coins2}, Amount: {amount2}")
    print(f"Result: {coinChange(coins2, amount2)}")
    # Expected: -1
    print()
    
    # Test Case 3: Zero amount
    coins3, amount3 = [1], 0
    print(f"Coins: {coins3}, Amount: {amount3}")
    print(f"Result: {coinChange(coins3, amount3)}")
    # Expected: 0
    print()
    
    # Test Case 4: Greedy doesn't work
    coins4, amount4 = [1, 3, 4], 6
    print(f"Coins: {coins4}, Amount: {amount4}")
    print(f"Result: {coinChange(coins4, amount4)}")
    # Expected: 2 (3 + 3), not 3 (4 + 1 + 1)
    print()
    
    # Test Case 5: Large amount
    coins5, amount5 = [1, 5, 10, 25], 100
    print(f"Coins: {coins5}, Amount: {amount5}")
    print(f"Result: {coinChange(coins5, amount5)}")
    # Expected: 4 (25 × 4)


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. UNBOUNDED KNAPSACK PATTERN:
   
   Same coin can be used multiple times.
   
   dp[i] = min(dp[i - coin] + 1) for all coins
   
   This is the classic unbounded knapsack variant.

2. WHY GREEDY DOESN'T WORK:
   
   coins = [1, 3, 4], amount = 6
   
   Greedy: 4 + 1 + 1 = 3 coins ❌
   Optimal: 3 + 3 = 2 coins ✓
   
   Need DP to find global optimum!

3. RECURRENCE:
   
   dp[amount] = min(dp[amount - coin] + 1) for all valid coins
   
   "If I use this coin, what's the min for remaining amount?"

4. BASE CASE:
   
   dp[0] = 0 (zero coins for zero amount)
   dp[i] = infinity initially (impossible until proven otherwise)

5. BFS INTERPRETATION:
   
   View amounts as graph nodes.
   Edge from i to i+coin for each coin.
   BFS finds shortest path (fewest coins).
   
   Same complexity as DP!

6. TIME/SPACE:
   
   Time: O(amount × n)
   Space: O(amount)
   
   n = number of coin denominations

7. COIN CHANGE II (LC 518):
   
   Count NUMBER of ways (not minimum coins).
   Different recurrence:
   
   dp[i] += dp[i - coin]
   
   Order of loops matters for avoiding duplicates!

8. COMMON MISTAKES:
   
   ❌ Using greedy (taking largest coin first)
   ❌ Not handling impossible case (-1)
   ❌ Off-by-one in loop bounds

9. RELATED PROBLEMS:
   
   - Coin Change II (LC 518) - count ways
   - Minimum Cost for Tickets (LC 983)
   - Perfect Squares (LC 279)

10. practice TIP:
    
    "Greedy doesn't work here because largest coins aren't
    always optimal. I'll use DP where dp[i] is the minimum
    coins for amount i.
    
    For each amount, I try each coin: if I use this coin,
    what's the minimum for the remaining amount?
    
    dp[i] = min(dp[i - coin] + 1) for all valid coins
    
    Time: O(amount × n), Space: O(amount)."
    
    Give the greedy counterexample upfront!

================================================================================
"""
