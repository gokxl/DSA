"""
================================================================================
PROBLEM: Container With Most Water (LeetCode 11)
Difficulty: Medium | Pattern: Arrays & Two Pointers
================================================================================

PROBLEM STATEMENT:
Given n non-negative integers height[i] representing heights of vertical lines,
find two lines that together with the x-axis form a container that holds the 
most water.

Note: You may not slant the container.

EXAMPLES:
    Input: height = [1,8,6,2,5,4,8,3,7]
    Output: 49
    Explanation: Lines at index 1 (height=8) and index 8 (height=7)
                 Area = min(8,7) * (8-1) = 7 * 7 = 49

    Input: height = [1,1]
    Output: 1

    Input: height = [4,3,2,1,4]
    Output: 16
    Explanation: Lines at index 0 and 4, Area = 4 * 4 = 16

CONSTRAINTS:
- n == height.length
- 2 <= n <= 10^5
- 0 <= height[i] <= 10^4

================================================================================
"""

from typing import List


# ============================================================================
# SOLUTION 1: Brute Force (Don't use, but mention)
# ============================================================================
def maxArea_bruteforce(height: List[int]) -> int:
    """
    Check every pair of lines and calculate area.
    
    Time: O(n^2)
    Space: O(1)
    """
    max_area = 0
    n = len(height)
    
    for i in range(n):
        for j in range(i + 1, n):
            width = j - i
            h = min(height[i], height[j])
            area = width * h
            max_area = max(max_area, area)
    
    return max_area


# ============================================================================
# SOLUTION 2: Two Pointers (Optimal)
# ============================================================================
def maxArea(height: List[int]) -> int:
    """
    Start with widest container (left and right ends).
    Greedily move the pointer with smaller height inward.
    
    WHY THIS WORKS:
    - Area = min(height[left], height[right]) * (right - left)
    - If we move the TALLER pointer, width decreases and height can't increase
      beyond the shorter one, so area can only decrease or stay same.
    - If we move the SHORTER pointer, width decreases but height might increase
      enough to compensate, so area might increase.
    
    Time: O(n) - single pass
    Space: O(1)
    """
    left, right = 0, len(height) - 1
    max_area = 0
    
    while left < right:
        # Calculate current area
        width = right - left
        h = min(height[left], height[right])
        current_area = width * h
        max_area = max(max_area, current_area)
        
        # Move the pointer with smaller height
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    
    return max_area


# ============================================================================
# SOLUTION 2 VARIATION: With early termination optimization
# ============================================================================
def maxArea_optimized(height: List[int]) -> int:
    """
    Same as above but skip heights that can't improve the answer.
    
    Time: O(n) worst case, but faster in practice
    Space: O(1)
    """
    left, right = 0, len(height) - 1
    max_area = 0
    
    while left < right:
        h = min(height[left], height[right])
        max_area = max(max_area, h * (right - left))
        
        # Skip all lines shorter than current minimum
        while left < right and height[left] <= h:
            left += 1
        while left < right and height[right] <= h:
            right -= 1
    
    return max_area


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Standard case
    height1 = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    print(f"Input: {height1}")
    print(f"Output: {maxArea(height1)}")
    # Expected: 49
    print()
    
    # Test Case 2: Minimum array
    height2 = [1, 1]
    print(f"Input: {height2}")
    print(f"Output: {maxArea(height2)}")
    # Expected: 1
    print()
    
    # Test Case 3: Symmetric array
    height3 = [4, 3, 2, 1, 4]
    print(f"Input: {height3}")
    print(f"Output: {maxArea(height3)}")
    # Expected: 16
    print()
    
    # Test Case 4: Increasing array
    height4 = [1, 2, 3, 4, 5]
    print(f"Input: {height4}")
    print(f"Output: {maxArea(height4)}")
    # Expected: 6 (index 0 and 4: min(1,5)*4 = 4, or index 1 and 4: min(2,5)*3 = 6)
    print()
    
    # Test Case 5: Decreasing array
    height5 = [5, 4, 3, 2, 1]
    print(f"Input: {height5}")
    print(f"Output: {maxArea(height5)}")
    # Expected: 6


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. THE GREEDY INSIGHT (Most Important):
   - "Why move the shorter pointer and not the taller one?"
   - If we have height[left] < height[right]:
     * Current area is limited by height[left]
     * If we move right pointer inward:
       - Width decreases
       - Height stays <= height[left] (still limited by shorter)
       - Area can ONLY decrease
     * If we move left pointer inward:
       - Width decreases
       - BUT height might increase if we find taller line
       - Area MIGHT increase
   
2. PROOF OF CORRECTNESS:
   - We never miss the optimal solution because:
   - When we move a pointer, we're eliminating pairs that CANNOT be optimal
   - The pairs we eliminate have the same or smaller area than current

3. VISUAL UNDERSTANDING:
   - Draw the container on paper
   - Show width (horizontal) and height (minimum of two lines)
   - Demonstrate why moving shorter pointer makes sense

4. COMMON MISTAKES:
   - Confusing this with Trapping Rain Water (different problem!)
   - Not understanding why greedy works here

5. TIME COMPLEXITY PROOF:
   - Each iteration, either left++ or right--
   - At most n iterations total
   - O(n) time

6. RELATED PROBLEMS:
   - Trapping Rain Water (LC 42) - similar visualization but different logic
   - Best Time to Buy/Sell Stock - also uses two pointers greedy

================================================================================
EXPLANATION WALKTHROUGH:
================================================================================

1. "Let me understand the problem - we need to find two lines that maximize
    the water container area, where area = min(heights) × width"

2. "Brute force would be O(n²) - check every pair. Let me think of something
    better..."

3. "Key insight: if I start with the widest container (endpoints), and 
    I want to potentially find a larger area, I MUST increase the height
    since width can only decrease."

4. "So I should move the pointer with the smaller height, hoping to find
    a taller line that compensates for the lost width."

5. "This greedy approach works because we never skip a potentially optimal
    solution - we only eliminate pairs that can't be better than current."

================================================================================
"""
