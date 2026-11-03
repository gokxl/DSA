"""
================================================================================
PROBLEM: Gas Station (LeetCode 134)
Difficulty: Medium | Pattern: Greedy
================================================================================

PROBLEM STATEMENT:
There are n gas stations along a circular route, where the amount of gas at the 
ith station is gas[i].

You have a car with an unlimited gas tank and it costs cost[i] of gas to travel 
from the ith station to its next (i + 1)th station. You begin the journey with 
an empty tank at one of the gas stations.

Given two integer arrays gas and cost, return the starting gas station's index 
if you can travel around the circuit once in the clockwise direction, otherwise 
return -1. If there exists a solution, it is guaranteed to be unique.

EXAMPLES:
    Input: gas = [1,2,3,4,5], cost = [3,4,5,1,2]
    Output: 3
    Explanation:
    Start at station 3 (index 3) and fill up with 4 unit of gas. Tank = 0 + 4 = 4
    Travel to station 4. Tank = 4 - 1 + 5 = 8
    Travel to station 0. Tank = 8 - 2 + 1 = 7
    Travel to station 1. Tank = 7 - 3 + 2 = 6
    Travel to station 2. Tank = 6 - 4 + 3 = 5
    Travel to station 3. Cost = 5. Tank = 5 - 5 = 0
    Return to starting point with 0 gas, completing the circuit.

    Input: gas = [2,3,4], cost = [3,4,3]
    Output: -1
    Explanation: Cannot complete circuit from any station.

CONSTRAINTS:
- n == gas.length == cost.length
- 1 <= n <= 10^5
- 0 <= gas[i], cost[i] <= 10^4

================================================================================
"""
from typing import List


# ============================================================================
# SOLUTION 1: Greedy (One Pass)
# ============================================================================
def canCompleteCircuit(gas: List[int], cost: List[int]) -> int:
    """
    Key insight: If total gas >= total cost, solution exists.
    
    If we can't reach station i+1 from start, start at i+1.
    
    Time: O(n)
    Space: O(1)
    """
    total_tank = 0
    current_tank = 0
    start = 0
    
    for i in range(len(gas)):
        diff = gas[i] - cost[i]
        total_tank += diff
        current_tank += diff
        
        # Can't reach next station from current start
        if current_tank < 0:
            start = i + 1  # Try starting from next station
            current_tank = 0
    
    # If total gas >= total cost, start position works
    return start if total_tank >= 0 else -1


# ============================================================================
# SOLUTION 2: Find minimum point
# ============================================================================
def canCompleteCircuit_min_point(gas: List[int], cost: List[int]) -> int:
    """
    Find the point where cumulative sum is minimum.
    Start from the station AFTER that point.
    
    Time: O(n)
    Space: O(1)
    """
    n = len(gas)
    total = 0
    min_tank = float('inf')
    min_index = 0
    
    for i in range(n):
        total += gas[i] - cost[i]
        if total < min_tank:
            min_tank = total
            min_index = i
    
    # If total is negative, no solution
    if total < 0:
        return -1
    
    # Start from station after minimum point
    return (min_index + 1) % n


# ============================================================================
# SOLUTION 3: Brute Force (for understanding)
# ============================================================================
def canCompleteCircuit_brute(gas: List[int], cost: List[int]) -> int:
    """
    Try each starting position.
    
    Time: O(n²)
    Space: O(1)
    """
    n = len(gas)
    
    for start in range(n):
        tank = 0
        success = True
        
        for i in range(n):
            station = (start + i) % n
            tank += gas[station] - cost[station]
            
            if tank < 0:
                success = False
                break
        
        if success:
            return start
    
    return -1


# ============================================================================
# SOLUTION 4: Two pointers (circular)
# ============================================================================
def canCompleteCircuit_two_pointer(gas: List[int], cost: List[int]) -> int:
    """
    Two pointer approach on circular array.
    
    Time: O(n)
    Space: O(1)
    """
    n = len(gas)
    start, end = n - 1, 0
    total = gas[start] - cost[start]
    
    while start > end:
        if total >= 0:
            # Can extend from end
            total += gas[end] - cost[end]
            end += 1
        else:
            # Need more gas, try earlier start
            start -= 1
            total += gas[start] - cost[start]
    
    return start if total >= 0 else -1


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Has solution
    gas1, cost1 = [1, 2, 3, 4, 5], [3, 4, 5, 1, 2]
    print(f"gas = {gas1}, cost = {cost1}")
    print(f"Greedy: {canCompleteCircuit(gas1, cost1)}")
    print(f"Min Point: {canCompleteCircuit_min_point(gas1, cost1)}")
    # Expected: 3
    print()
    
    # Test Case 2: No solution
    gas2, cost2 = [2, 3, 4], [3, 4, 3]
    print(f"gas = {gas2}, cost = {cost2}")
    print(f"Result: {canCompleteCircuit(gas2, cost2)}")
    # Expected: -1
    print()
    
    # Test Case 3: Single station
    gas3, cost3 = [5], [4]
    print(f"gas = {gas3}, cost = {cost3}")
    print(f"Result: {canCompleteCircuit(gas3, cost3)}")
    # Expected: 0
    print()
    
    # Test Case 4: All same
    gas4, cost4 = [3, 3, 3], [3, 3, 3]
    print(f"gas = {gas4}, cost = {cost4}")
    print(f"Result: {canCompleteCircuit(gas4, cost4)}")
    # Expected: 0
    print()
    
    # Test Case 5: Start from index 0
    gas5, cost5 = [5, 1, 2, 3, 4], [4, 4, 1, 5, 1]
    print(f"gas = {gas5}, cost = {cost5}")
    print(f"Result: {canCompleteCircuit(gas5, cost5)}")
    # Expected: 4


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. TOTAL GAS VS TOTAL COST:
   
   If sum(gas) < sum(cost): No solution exists!
   If sum(gas) >= sum(cost): Exactly one solution exists.
   
   This is the key mathematical insight.

2. GREEDY INSIGHT:
   
   If we can't reach station j from station i,
   then stations i+1, i+2, ..., j-1 also can't reach j.
   
   Why? They would have less gas than starting at i.
   
   So we skip directly to j as new starting point!

3. ONE PASS ALGORITHM:
   
   - Track total_tank (overall feasibility)
   - Track current_tank (current attempt)
   - When current_tank < 0, reset start to i+1
   
   If total_tank >= 0 at end, start is valid.

4. MINIMUM POINT INSIGHT:
   
   The valid starting point is right after where
   cumulative sum is minimum.
   
   Starting there gives us the "best head start".

5. WHY START AFTER MINIMUM?
   
   At minimum point, we've used the most gas relative to gained.
   Starting after it, we collect gas before hitting that tough segment.

6. UNIQUENESS:
   
   Problem guarantees unique solution if exists.
   Otherwise multiple could work if total balanced.

7. COMMON MISTAKES:
   
   ❌ Not checking total feasibility
   ❌ Overcounting when wrapping around
   ❌ Starting from wrong position after failure

8. PROOF OF CORRECTNESS:
   
   If we fail at position j starting from i:
   - We had some gas at each point i to j-1
   - Still couldn't reach j
   - Starting later means less gas at some point
   - Therefore later starts also fail
   
   So skip to j is valid!

9. RELATED PROBLEMS:
   
   - Minimum Cost to Hire K Workers (similar greedy)
   - Task Scheduler
   - Circular Array Loop

10. HOW TO EXPLAIN IT:
    
    "First, I check if sum(gas) >= sum(cost). If not, no solution.
    
    Then I use greedy: if I can't reach station j from start i,
    I know stations i+1 to j-1 also can't reach j
    (they'd have less gas). So I start fresh from j.
    
    At the end, if total gas is sufficient, my final start works.
    
    Time: O(n), Space: O(1)."
    
    Explain WHY skipping stations works!

================================================================================
"""
