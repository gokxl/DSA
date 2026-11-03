"""
================================================================================
PROBLEM: Koko Eating Bananas (LeetCode 875)
Difficulty: Medium | Pattern: Binary Search on Answer
================================================================================

PROBLEM STATEMENT:
Koko loves to eat bananas. There are n piles of bananas, the ith pile has piles[i] 
bananas. The guards have gone and will come back in h hours.

Koko can decide her bananas-per-hour eating speed of k. Each hour, she chooses 
some pile of bananas and eats k bananas from that pile. If the pile has less 
than k bananas, she eats all of them instead and will not eat any more bananas 
during this hour.

Koko likes to eat slowly but still wants to finish eating all the bananas 
before the guards return.

Return the minimum integer k such that she can eat all the bananas within h hours.

EXAMPLES:
    Input: piles = [3,6,7,11], h = 8
    Output: 4
    Explanation:
        - At k=4: ceil(3/4) + ceil(6/4) + ceil(7/4) + ceil(11/4)
                = 1 + 2 + 2 + 3 = 8 hours ✓

    Input: piles = [30,11,23,4,20], h = 5
    Output: 30
    Explanation: Each pile must be finished in 1 hour.

    Input: piles = [30,11,23,4,20], h = 6
    Output: 23

CONSTRAINTS:
- 1 <= piles.length <= 10^4
- piles.length <= h <= 10^9
- 1 <= piles[i] <= 10^9

================================================================================
"""

from typing import List
import math


# ============================================================================
# SOLUTION 1: Binary Search on Answer (Optimal)
# ============================================================================
def minEatingSpeed(piles: List[int], h: int) -> int:
    """
    Binary search on eating speed k.
    
    Key insight:
    - Minimum speed = 1
    - Maximum speed = max(piles) (can finish any pile in 1 hour)
    - For a given k, check if Koko can finish in h hours
    - Find minimum k that works
    
    Time: O(n * log(max(piles)))
    Space: O(1)
    """
    def can_finish(k: int) -> bool:
        """Check if Koko can eat all bananas at speed k in h hours."""
        hours_needed = 0
        for pile in piles:
            hours_needed += math.ceil(pile / k)
            # Early termination
            if hours_needed > h:
                return False
        return True
    
    # Binary search on speed
    left, right = 1, max(piles)
    
    while left < right:
        mid = left + (right - left) // 2
        
        if can_finish(mid):
            # Can finish, try smaller speed
            right = mid
        else:
            # Cannot finish, need higher speed
            left = mid + 1
    
    return left


# ============================================================================
# SOLUTION 2: Without math.ceil
# ============================================================================
def minEatingSpeed_no_ceil(piles: List[int], h: int) -> int:
    """
    Same approach but without using math.ceil.
    
    ceil(a/b) = (a + b - 1) // b
    
    Time: O(n * log(max(piles)))
    Space: O(1)
    """
    def hours_to_eat(k: int) -> int:
        """Calculate total hours needed at speed k."""
        return sum((pile + k - 1) // k for pile in piles)
    
    left, right = 1, max(piles)
    
    while left < right:
        mid = left + (right - left) // 2
        
        if hours_to_eat(mid) <= h:
            right = mid
        else:
            left = mid + 1
    
    return left


# ============================================================================
# SOLUTION 3: With explicit bounds calculation
# ============================================================================
def minEatingSpeed_explicit(piles: List[int], h: int) -> int:
    """
    More explicit calculation of bounds.
    
    Lower bound: ceil(sum(piles) / h) - if we spread eating evenly
    Upper bound: max(piles) - finish each pile in at most 1 hour
    
    Time: O(n * log(max(piles)))
    Space: O(1)
    """
    total_bananas = sum(piles)
    n = len(piles)
    
    # Lower bound: minimum speed to finish if we could split piles perfectly
    lower = max(1, (total_bananas + h - 1) // h)
    # Upper bound: finish any pile in 1 hour
    upper = max(piles)
    
    def can_finish(k):
        hours = 0
        for pile in piles:
            hours += (pile + k - 1) // k
        return hours <= h
    
    while lower < upper:
        mid = lower + (upper - lower) // 2
        
        if can_finish(mid):
            upper = mid
        else:
            lower = mid + 1
    
    return lower


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Standard example
    piles1, h1 = [3, 6, 7, 11], 8
    print(f"Input: piles = {piles1}, h = {h1}")
    print(f"Output (Optimal): {minEatingSpeed(piles1, h1)}")
    print(f"Output (No ceil): {minEatingSpeed_no_ceil(piles1, h1)}")
    # Expected: 4
    print()
    
    # Test Case 2: Each pile in one hour
    piles2, h2 = [30, 11, 23, 4, 20], 5
    print(f"Input: piles = {piles2}, h = {h2}")
    print(f"Output: {minEatingSpeed(piles2, h2)}")
    # Expected: 30
    print()
    
    # Test Case 3: More time available
    piles3, h3 = [30, 11, 23, 4, 20], 6
    print(f"Input: piles = {piles3}, h = {h3}")
    print(f"Output: {minEatingSpeed(piles3, h3)}")
    # Expected: 23
    print()
    
    # Test Case 4: Single pile
    piles4, h4 = [312884470], 968709470
    print(f"Input: piles = {piles4}, h = {h4}")
    print(f"Output: {minEatingSpeed(piles4, h4)}")
    # Expected: 1
    print()
    
    # Test Case 5: Large h
    piles5, h5 = [1, 1, 1, 999999999], 10
    print(f"Input: piles = {piles5}, h = {h5}")
    print(f"Output: {minEatingSpeed(piles5, h5)}")
    # Each pile has plenty of time
    print()
    
    # Verification for test 1:
    k = 4
    hours = sum(math.ceil(p / k) for p in piles1)
    print(f"Verification: At k=4, hours needed = {hours}")


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. BINARY SEARCH ON ANSWER PATTERN:
   
   This is a classic "minimize the maximum" problem.
   
   Instead of binary searching on array elements:
   - Binary search on the ANSWER SPACE (possible values of k)
   - For each candidate k, verify if it works
   
   Template:
   - Search space: [min_possible, max_possible]
   - Predicate: can_achieve(x)
   - Find minimum x where can_achieve(x) is True

2. WHY BINARY SEARCH WORKS:
   
   Monotonicity: If Koko can finish at speed k, she can also finish
   at any speed > k.
   
   We want the MINIMUM k, so:
   - If can_finish(mid): try smaller → right = mid
   - If cannot: need bigger → left = mid + 1

3. CHOOSING SEARCH BOUNDS:
   
   - Lower bound: 1 (minimum possible speed)
   - Upper bound: max(piles) (even the largest pile in 1 hour)
   
   Tighter lower bound: ceil(sum(piles) / h)
   (if we could magically spread bananas evenly)

4. HOURS CALCULATION:
   
   For pile of size p at speed k:
   hours = ceil(p / k)
   
   Without math.ceil:
   hours = (p + k - 1) // k
   
   This is because even 1 banana takes a full hour.

5. VISUAL EXAMPLE for piles=[3,6,7,11], h=8:
   
   Speed 1: 3 + 6 + 7 + 11 = 27 hours ✗
   Speed 4: 1 + 2 + 2 + 3 = 8 hours ✓
   Speed 3: 1 + 2 + 3 + 4 = 10 hours ✗
   Speed 5: 1 + 2 + 2 + 3 = 8 hours ✓ (but 4 is smaller)
   
   Binary search converges to k = 4

6. COMPLEXITY ANALYSIS:
   
   - Binary search: O(log(max(piles)))
   - Each check: O(n)
   - Total: O(n * log(max(piles)))
   
   This is much better than O(n * max(piles)) brute force!

7. COMMON MISTAKES:
   
   - Forgetting to ceil the division
   - Wrong bounds (upper bound should be max, not sum)
   - Not handling edge cases (single pile, h = n)

8. SIMILAR "BINARY SEARCH ON ANSWER" PROBLEMS:
   
   - Capacity To Ship Packages (LC 1011) - Very similar!
   - Split Array Largest Sum (LC 410)
   - Minimize Max Distance to Gas Station (LC 774)
   - Magnetic Force Between Two Balls (LC 1552)
   
   All follow the same pattern:
   1. Define search space for answer
   2. Write verification function
   3. Binary search for optimal answer

9. DISCUSSION POINTS:
   
   Q: Why not just try all speeds from 1 to max?
   A: That's O(max * n) which could be 10^9 * 10^4 = too slow
      Binary search reduces to O(log(max) * n)
   
   Q: How did you determine the bounds?
   A: Lower: 1 (can't eat 0 bananas/hour)
      Upper: max(piles) (any pile in 1 hour is always enough)

10. TEMPLATE FOR BINARY SEARCH ON ANSWER:

    def solve(params):
        def is_valid(candidate):
            # Return True if candidate works
            pass
        
        left, right = MIN_POSSIBLE, MAX_POSSIBLE
        
        while left < right:
            mid = (left + right) // 2
            
            if is_valid(mid):
                right = mid  # For finding minimum
                # left = mid + 1  # For finding maximum
            else:
                left = mid + 1  # For finding minimum
                # right = mid - 1  # For finding maximum
        
        return left

================================================================================
"""
