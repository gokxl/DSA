"""
================================================================================
PROBLEM: Maximum Product Subarray (LeetCode 152)
Difficulty: Medium | Pattern: DP
================================================================================

PROBLEM STATEMENT:
Given an integer array nums, find a subarray that has the largest product, 
and return the product.

The test cases are generated so that the answer will fit in a 32-bit integer.

EXAMPLES:
    Input: nums = [2,3,-2,4]
    Output: 6
    Explanation: [2,3] has the largest product 6.

    Input: nums = [-2,0,-1]
    Output: 0
    Explanation: The result cannot be 2, because [-2,-1] is not a contiguous subarray.

CONSTRAINTS:
- 1 <= nums.length <= 2 * 10^4
- -10 <= nums[i] <= 10
- The product of any subarray of nums is guaranteed to fit in a 32-bit integer

================================================================================
"""
from typing import List


# ============================================================================
# SOLUTION 1: Track Min and Max (Optimal)
# ============================================================================
def maxProduct(nums: List[int]) -> int:
    """
    Track both maximum and minimum products ending at each position.
    
    Key insight: A negative number can turn min into max!
    
    Time: O(n)
    Space: O(1)
    """
    if not nums:
        return 0
    
    max_so_far = nums[0]
    min_so_far = nums[0]  # Track min for negative numbers
    result = nums[0]
    
    for i in range(1, len(nums)):
        num = nums[i]
        
        # When multiplying by negative, min and max swap roles
        if num < 0:
            max_so_far, min_so_far = min_so_far, max_so_far
        
        max_so_far = max(num, max_so_far * num)
        min_so_far = min(num, min_so_far * num)
        
        result = max(result, max_so_far)
    
    return result


# ============================================================================
# SOLUTION 2: Calculate all three options explicitly
# ============================================================================
def maxProduct_explicit(nums: List[int]) -> int:
    """
    At each position, new max/min is one of:
    - num itself (start fresh)
    - prev_max * num
    - prev_min * num (negative × negative)
    
    Time: O(n)
    Space: O(1)
    """
    max_prod = nums[0]
    min_prod = nums[0]
    result = nums[0]
    
    for i in range(1, len(nums)):
        candidates = (nums[i], max_prod * nums[i], min_prod * nums[i])
        max_prod = max(candidates)
        min_prod = min(candidates)
        result = max(result, max_prod)
    
    return result


# ============================================================================
# SOLUTION 3: Two passes (from both directions)
# ============================================================================
def maxProduct_two_pass(nums: List[int]) -> int:
    """
    Key insight: Max product is either prefix product or suffix product.
    
    Why? If even number of negatives, whole array is max.
    If odd negatives, max is either before last negative or after first.
    
    Zero resets the product.
    
    Time: O(n)
    Space: O(1)
    """
    n = len(nums)
    result = float('-inf')
    
    # Forward pass
    product = 1
    for i in range(n):
        product *= nums[i]
        result = max(result, product)
        if product == 0:
            product = 1
    
    # Backward pass
    product = 1
    for i in range(n - 1, -1, -1):
        product *= nums[i]
        result = max(result, product)
        if product == 0:
            product = 1
    
    return result


# ============================================================================
# SOLUTION 4: DP Array
# ============================================================================
def maxProduct_dp(nums: List[int]) -> int:
    """
    DP with arrays (less space efficient but clearer).
    
    Time: O(n)
    Space: O(n)
    """
    n = len(nums)
    max_dp = [0] * n  # max product ending at i
    min_dp = [0] * n  # min product ending at i
    
    max_dp[0] = min_dp[0] = nums[0]
    result = nums[0]
    
    for i in range(1, n):
        if nums[i] >= 0:
            max_dp[i] = max(nums[i], max_dp[i - 1] * nums[i])
            min_dp[i] = min(nums[i], min_dp[i - 1] * nums[i])
        else:
            max_dp[i] = max(nums[i], min_dp[i - 1] * nums[i])
            min_dp[i] = min(nums[i], max_dp[i - 1] * nums[i])
        
        result = max(result, max_dp[i])
    
    return result


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Standard case
    nums1 = [2, 3, -2, 4]
    print(f"nums = {nums1}")
    print(f"Min/Max: {maxProduct(nums1)}")
    print(f"Two pass: {maxProduct_two_pass(nums1)}")
    # Expected: 6 ([2,3])
    print()
    
    # Test Case 2: With zero
    nums2 = [-2, 0, -1]
    print(f"nums = {nums2}")
    print(f"Result: {maxProduct(nums2)}")
    # Expected: 0
    print()
    
    # Test Case 3: All negative
    nums3 = [-2, -3, -4]
    print(f"nums = {nums3}")
    print(f"Result: {maxProduct(nums3)}")
    # Expected: 12 ([-3,-4])
    print()
    
    # Test Case 4: Single negative
    nums4 = [-2]
    print(f"nums = {nums4}")
    print(f"Result: {maxProduct(nums4)}")
    # Expected: -2
    print()
    
    # Test Case 5: Mix of positives and negatives
    nums5 = [2, -5, -2, -4, 3]
    print(f"nums = {nums5}")
    print(f"Result: {maxProduct_explicit(nums5)}")
    # Expected: 24 ([2,-5,-2,-4,3] = 240, but let's verify)
    # Actually: [2,-5,-2,-4,3] = 2*-5*-2*-4*3 = -240
    # [2,-5,-2,-4] = 80, which is correct
    print()


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. WHY TRACK MINIMUM?
   
   Negative × Negative = Positive!
   
   Current minimum (large negative) can become maximum
   when multiplied by a negative number.
   
   Example: min = -6, num = -2 → -6 × -2 = 12 (new max!)

2. WHEN TO SWAP MIN/MAX:
   
   When current number is negative:
   - Old max × negative = new min candidate
   - Old min × negative = new max candidate
   
   So swap before calculating!

3. THREE CHOICES AT EACH POSITION:
   
   - Start fresh: just nums[i]
   - Extend max: max_prod × nums[i]
   - Extend min: min_prod × nums[i] (for negative × negative)
   
   new_max = max(all three)
   new_min = min(all three)

4. ZERO RESETS EVERYTHING:
   
   Any product containing 0 is 0.
   When we hit 0, we must start fresh.
   
   max_so_far = max(0, ...) handles this.

5. TWO-PASS INTUITION:
   
   Without zeros, if even negatives: whole array is answer.
   If odd negatives: either exclude first negative's prefix
   or exclude last negative's suffix.
   
   Forward and backward passes capture both.

6. COMPARISON TO KADANE'S:
   
   Max Sum Subarray: max_here = max(num, max_here + num)
   Max Product: Need both max AND min tracking
   
   Product is trickier due to negatives!

7. EDGE CASES:
   
   - Single element (return it)
   - All zeros (return 0)
   - All negatives (return max of even-length products)
   - Contains zero (splits into subproblems)

8. COMMON MISTAKES:
   
   ❌ Forgetting to track minimum
   ❌ Not handling zero correctly
   ❌ Not considering starting fresh (just num)

9. RELATED PROBLEMS:
   
   - Maximum Subarray (LC 53) - Kadane's algorithm
   - Product of Array Except Self (LC 238)
   - Maximum Length of Subarray with Positive Product (LC 1567)

10. HOW TO EXPLAIN IT:
    
    "Unlike max sum subarray, products have a twist: negative
    times negative is positive!
    
    So I track both max and min products ending at each position.
    When I hit a negative number, the current min might become
    the new max.
    
    At each step: new_max = max(num, prev_max × num, prev_min × num)
    
    This handles all cases including zeros (which reset to starting fresh)."

================================================================================
"""
