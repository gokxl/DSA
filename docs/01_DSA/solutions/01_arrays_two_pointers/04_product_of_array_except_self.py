"""
================================================================================
PROBLEM: Product of Array Except Self (LeetCode 238)
Difficulty: Medium | Pattern: Arrays - Prefix/Suffix
================================================================================

PROBLEM STATEMENT:
Given an integer array `nums`, return an array `answer` such that `answer[i]` 
is equal to the product of all the elements of `nums` except `nums[i]`.

REQUIREMENTS:
- Must run in O(n) time
- CANNOT use the division operation
- The product of any prefix or suffix is guaranteed to fit in a 32-bit integer

EXAMPLES:
    Input: nums = [1,2,3,4]
    Output: [24,12,8,6]
    Explanation:
        answer[0] = 2*3*4 = 24
        answer[1] = 1*3*4 = 12
        answer[2] = 1*2*4 = 8
        answer[3] = 1*2*3 = 6

    Input: nums = [-1,1,0,-3,3]
    Output: [0,0,9,0,0]
    Explanation: Only answer[2] is non-zero because it excludes the 0

CONSTRAINTS:
- 2 <= nums.length <= 10^5
- -30 <= nums[i] <= 30
- Product of any prefix/suffix fits in 32-bit integer

================================================================================
"""

from typing import List


# ============================================================================
# SOLUTION 1: Division (Doesn't meet requirements, but mention it)
# ============================================================================
def productExceptSelf_division(nums: List[int]) -> List[int]:
    """
    Calculate total product, then divide by each element.
    NOTE: This DOESN'T meet the "no division" requirement!
    Also fails when there are zeros.
    
    Time: O(n)
    Space: O(1)
    """
    total_product = 1
    zero_count = 0
    
    for num in nums:
        if num == 0:
            zero_count += 1
        else:
            total_product *= num
    
    result = []
    for num in nums:
        if zero_count > 1:
            result.append(0)
        elif zero_count == 1:
            result.append(0 if num != 0 else total_product)
        else:
            result.append(total_product // num)
    
    return result


# ============================================================================
# SOLUTION 2: Two Arrays - Prefix and Suffix Products
# ============================================================================
def productExceptSelf_two_arrays(nums: List[int]) -> List[int]:
    """
    Key insight: answer[i] = (product of all left elements) × (product of all right elements)
    
    1. Create prefix array: prefix[i] = nums[0] * nums[1] * ... * nums[i-1]
    2. Create suffix array: suffix[i] = nums[i+1] * nums[i+2] * ... * nums[n-1]
    3. answer[i] = prefix[i] * suffix[i]
    
    Time: O(n) - three passes
    Space: O(n) - two extra arrays
    """
    n = len(nums)
    
    # prefix[i] = product of elements BEFORE index i
    prefix = [1] * n
    for i in range(1, n):
        prefix[i] = prefix[i-1] * nums[i-1]
    
    # suffix[i] = product of elements AFTER index i
    suffix = [1] * n
    for i in range(n-2, -1, -1):
        suffix[i] = suffix[i+1] * nums[i+1]
    
    # Combine
    result = [prefix[i] * suffix[i] for i in range(n)]
    
    return result


# ============================================================================
# SOLUTION 3: Space Optimized (Optimal - Use this in practice)
# ============================================================================
def productExceptSelf(nums: List[int]) -> List[int]:
    """
    Use the result array to store prefix products, then multiply with suffix
    products in a single pass from right to left.
    
    Time: O(n) - two passes
    Space: O(1) - output array doesn't count as extra space
    """
    n = len(nums)
    result = [1] * n
    
    # First pass: calculate prefix products
    # result[i] = product of all elements to the LEFT of i
    prefix = 1
    for i in range(n):
        result[i] = prefix
        prefix *= nums[i]
    
    # Second pass: multiply by suffix products
    # result[i] *= product of all elements to the RIGHT of i
    suffix = 1
    for i in range(n - 1, -1, -1):
        result[i] *= suffix
        suffix *= nums[i]
    
    return result


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Standard case
    nums1 = [1, 2, 3, 4]
    print(f"Input: {nums1}")
    print(f"Output: {productExceptSelf(nums1)}")
    # Expected: [24, 12, 8, 6]
    print()
    
    # Test Case 2: Contains zero
    nums2 = [-1, 1, 0, -3, 3]
    print(f"Input: {nums2}")
    print(f"Output: {productExceptSelf(nums2)}")
    # Expected: [0, 0, 9, 0, 0]
    print()
    
    # Test Case 3: Two elements
    nums3 = [2, 3]
    print(f"Input: {nums3}")
    print(f"Output: {productExceptSelf(nums3)}")
    # Expected: [3, 2]
    print()
    
    # Test Case 4: Contains negative numbers
    nums4 = [-1, -2, -3]
    print(f"Input: {nums4}")
    print(f"Output: {productExceptSelf(nums4)}")
    # Expected: [6, 3, 2]
    print()
    
    # Test Case 5: Multiple zeros
    nums5 = [0, 0, 1]
    print(f"Input: {nums5}")
    print(f"Output: {productExceptSelf(nums5)}")
    # Expected: [0, 0, 0]


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. THE CORE INSIGHT:
   answer[i] = (product of all elements before i) × (product of all elements after i)
   answer[i] = prefix[i] × suffix[i]

2. EXAMPLE WALKTHROUGH:
   nums = [1, 2, 3, 4]
   
   Prefix products (running left to right):
   prefix[0] = 1         (nothing before index 0)
   prefix[1] = 1         (only 1 before index 1)
   prefix[2] = 1*2 = 2   (1, 2 before index 2)
   prefix[3] = 1*2*3 = 6 (1, 2, 3 before index 3)
   
   Suffix products (running right to left):
   suffix[3] = 1         (nothing after index 3)
   suffix[2] = 4         (only 4 after index 2)
   suffix[1] = 4*3 = 12  (3, 4 after index 1)
   suffix[0] = 4*3*2 = 24 (2, 3, 4 after index 0)
   
   Result:
   result[0] = prefix[0] * suffix[0] = 1 * 24 = 24
   result[1] = prefix[1] * suffix[1] = 1 * 12 = 12
   result[2] = prefix[2] * suffix[2] = 2 * 4 = 8
   result[3] = prefix[3] * suffix[3] = 6 * 1 = 6

3. WHY NO DIVISION?
   - Zeros in array cause division by zero
   - Interviewers want to test prefix/suffix thinking
   - It's a common constraint in similar problems

4. SPACE OPTIMIZATION TRICK:
   - Use result array for prefix
   - Use single variable for suffix (running product)
   - This achieves O(1) extra space

5. EDGE CASES:
   - Single zero: only that position's result is non-zero
   - Multiple zeros: all results are zero
   - Negative numbers: handle naturally
   - Array of length 2: simple swap of elements

6. RELATED PATTERNS:
   - Prefix Sum (cumulative sum)
   - Running Maximum/Minimum
   - Any "excluding current element" problems

================================================================================
practice COMMUNICATION:
================================================================================

"The key insight is that for each position i, I need the product of everything 
before it AND everything after it. If I precompute prefix products from left 
and suffix products from right, I can get each answer in O(1).

To optimize space, I'll use the result array itself to store prefix products, 
then do a second pass from right to left, multiplying by a running suffix 
product. This gives O(n) time and O(1) extra space."

================================================================================
"""
