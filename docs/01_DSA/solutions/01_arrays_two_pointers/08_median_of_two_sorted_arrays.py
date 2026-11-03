"""
================================================================================
PROBLEM: Median of Two Sorted Arrays (LeetCode 4)
Difficulty: Hard | Pattern: Binary Search + Partitioning
================================================================================

PROBLEM STATEMENT:
Given two sorted arrays nums1 and nums2 of size m and n respectively, 
return the median of the two sorted arrays.

The overall run time complexity should be O(log(m+n)).

EXAMPLES:
    Input: nums1 = [1,3], nums2 = [2]
    Output: 2.00000
    Explanation: merged = [1,2,3], median = 2.0

    Input: nums1 = [1,2], nums2 = [3,4]
    Output: 2.50000
    Explanation: merged = [1,2,3,4], median = (2 + 3) / 2 = 2.5

    Input: nums1 = [], nums2 = [1]
    Output: 1.0

CONSTRAINTS:
- nums1.length == m
- nums2.length == n
- 0 <= m <= 1000
- 0 <= n <= 1000
- 1 <= m + n <= 2000
- -10^6 <= nums1[i], nums2[i] <= 10^6

================================================================================
"""

from typing import List


# ============================================================================
# SOLUTION 1: Binary Search on Partition (Optimal)
# ============================================================================
def findMedianSortedArrays(nums1: List[int], nums2: List[int]) -> float:
    """
    Binary search to find the correct partition.
    
    Key insight: 
    - Median divides combined array into two equal halves
    - Left half has (m + n + 1) // 2 elements
    - Binary search on smaller array to find partition point
    
    For valid partition:
    - max_left1 <= min_right2
    - max_left2 <= min_right1
    
    Time: O(log(min(m, n)))
    Space: O(1)
    """
    # Ensure nums1 is the smaller array for efficiency
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    
    m, n = len(nums1), len(nums2)
    
    # Handle edge case where nums1 is empty
    if m == 0:
        mid = n // 2
        if n % 2 == 1:
            return float(nums2[mid])
        return (nums2[mid - 1] + nums2[mid]) / 2.0
    
    left, right = 0, m
    half_len = (m + n + 1) // 2  # Size of left half
    
    while left <= right:
        # Partition point for nums1
        partition1 = (left + right) // 2
        # Partition point for nums2 (derived from partition1)
        partition2 = half_len - partition1
        
        # Elements around partition
        # Use -inf and +inf for boundaries
        max_left1 = float('-inf') if partition1 == 0 else nums1[partition1 - 1]
        min_right1 = float('inf') if partition1 == m else nums1[partition1]
        
        max_left2 = float('-inf') if partition2 == 0 else nums2[partition2 - 1]
        min_right2 = float('inf') if partition2 == n else nums2[partition2]
        
        # Check if we found the correct partition
        if max_left1 <= min_right2 and max_left2 <= min_right1:
            # Found valid partition
            if (m + n) % 2 == 1:
                # Odd total length: median is max of left half
                return float(max(max_left1, max_left2))
            else:
                # Even total length: median is avg of max_left and min_right
                return (max(max_left1, max_left2) + min(min_right1, min_right2)) / 2.0
        elif max_left1 > min_right2:
            # partition1 is too far right, move left
            right = partition1 - 1
        else:
            # partition1 is too far left, move right
            left = partition1 + 1
    
    return 0.0  # Should never reach here


# ============================================================================
# SOLUTION 2: Merge and Find (Simple but O(m+n))
# ============================================================================
def findMedianSortedArrays_merge(nums1: List[int], nums2: List[int]) -> float:
    """
    Simple approach: Merge arrays and find median.
    
    Time: O(m + n) - merge step
    Space: O(m + n) - merged array
    
    Note: This doesn't meet the O(log(m+n)) requirement but is useful
    for understanding the problem and as a backup solution.
    """
    # Merge two sorted arrays
    merged = []
    i = j = 0
    
    while i < len(nums1) and j < len(nums2):
        if nums1[i] <= nums2[j]:
            merged.append(nums1[i])
            i += 1
        else:
            merged.append(nums2[j])
            j += 1
    
    # Add remaining elements
    merged.extend(nums1[i:])
    merged.extend(nums2[j:])
    
    # Find median
    n = len(merged)
    if n % 2 == 1:
        return float(merged[n // 2])
    else:
        return (merged[n // 2 - 1] + merged[n // 2]) / 2.0


# ============================================================================
# SOLUTION 3: Optimized Merge (Stop at median)
# ============================================================================
def findMedianSortedArrays_optimized_merge(nums1: List[int], nums2: List[int]) -> float:
    """
    Instead of full merge, stop when we've seen enough elements.
    Only need to track the elements around median position.
    
    Time: O((m + n) / 2)
    Space: O(1)
    
    Still doesn't meet O(log(m+n)) but better than full merge.
    """
    m, n = len(nums1), len(nums2)
    total = m + n
    mid = total // 2
    
    i = j = 0
    prev = curr = 0
    
    for _ in range(mid + 1):
        prev = curr
        
        if i >= m:
            curr = nums2[j]
            j += 1
        elif j >= n:
            curr = nums1[i]
            i += 1
        elif nums1[i] <= nums2[j]:
            curr = nums1[i]
            i += 1
        else:
            curr = nums2[j]
            j += 1
    
    if total % 2 == 1:
        return float(curr)
    else:
        return (prev + curr) / 2.0


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Odd total length
    nums1_1, nums2_1 = [1, 3], [2]
    print(f"Input: nums1 = {nums1_1}, nums2 = {nums2_1}")
    print(f"Output (Binary Search): {findMedianSortedArrays(nums1_1, nums2_1)}")
    print(f"Output (Merge): {findMedianSortedArrays_merge(nums1_1, nums2_1)}")
    # Expected: 2.0
    print()
    
    # Test Case 2: Even total length
    nums1_2, nums2_2 = [1, 2], [3, 4]
    print(f"Input: nums1 = {nums1_2}, nums2 = {nums2_2}")
    print(f"Output (Binary Search): {findMedianSortedArrays(nums1_2, nums2_2)}")
    print(f"Output (Merge): {findMedianSortedArrays_merge(nums1_2, nums2_2)}")
    # Expected: 2.5
    print()
    
    # Test Case 3: Empty array
    nums1_3, nums2_3 = [], [1]
    print(f"Input: nums1 = {nums1_3}, nums2 = {nums2_3}")
    print(f"Output (Binary Search): {findMedianSortedArrays(nums1_3, nums2_3)}")
    # Expected: 1.0
    print()
    
    # Test Case 4: Single elements
    nums1_4, nums2_4 = [1], [2]
    print(f"Input: nums1 = {nums1_4}, nums2 = {nums2_4}")
    print(f"Output (Binary Search): {findMedianSortedArrays(nums1_4, nums2_4)}")
    # Expected: 1.5
    print()
    
    # Test Case 5: Different sizes
    nums1_5, nums2_5 = [1, 3, 5, 7], [2, 4, 6, 8, 10]
    print(f"Input: nums1 = {nums1_5}, nums2 = {nums2_5}")
    print(f"Output (Binary Search): {findMedianSortedArrays(nums1_5, nums2_5)}")
    print(f"Output (Merge): {findMedianSortedArrays_merge(nums1_5, nums2_5)}")
    # merged = [1,2,3,4,5,6,7,8,10], median = 5.0
    print()
    
    # Test Case 6: No overlap
    nums1_6, nums2_6 = [1, 2], [7, 8, 9]
    print(f"Input: nums1 = {nums1_6}, nums2 = {nums2_6}")
    print(f"Output (Binary Search): {findMedianSortedArrays(nums1_6, nums2_6)}")
    # merged = [1,2,7,8,9], median = 7.0


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. PROBLEM UNDERSTANDING:
   
   Median of combined array [1, 2] + [3, 4] = [1, 2, 3, 4]
   - Odd length: middle element
   - Even length: average of two middle elements
   
   Challenge: Do this in O(log(m+n)) without actually merging!

2. KEY INSIGHT - PARTITIONING:
   
   Median divides array into two equal halves.
   
   nums1:  [.....L1 | R1......]
   nums2:  [.....L2 | R2......]
   
   Left half = elements before partition
   Right half = elements after partition
   
   For valid partition:
   - max(L1, L2) <= min(R1, R2)
   - All left elements <= all right elements

3. BINARY SEARCH STRATEGY:
   
   - Binary search on smaller array (optimize to O(log(min(m,n))))
   - For each partition1 in nums1, derive partition2 in nums2
   - partition2 = half_len - partition1
   - half_len = (m + n + 1) // 2
   
   Check validity:
   - L1 <= R2 and L2 <= R1 → Found it!
   - L1 > R2 → Move partition1 left
   - L2 > R1 → Move partition1 right

4. HANDLING EDGE CASES:
   
   - partition1 = 0: L1 = -infinity (nothing on left)
   - partition1 = m: R1 = +infinity (nothing on right)
   - Same for partition2
   
   Use float('-inf') and float('inf') for boundaries.

5. WHY (m + n + 1) // 2?
   
   - Ensures left half has equal or one more element
   - Works for both odd and even total lengths
   - For odd: median is max(L1, L2)
   - For even: median is (max(L1, L2) + min(R1, R2)) / 2

6. VISUAL EXAMPLE:
   
   nums1 = [1, 3, 5]
   nums2 = [2, 4, 6]
   
   total = 6, half_len = 3
   
   Try partition1 = 1 (1 element on left from nums1):
     partition2 = 3 - 1 = 2 (2 elements on left from nums2)
     
     nums1: [1 | 3, 5]     L1 = 1, R1 = 3
     nums2: [2, 4 | 6]     L2 = 4, R2 = 6
     
     Check: L1 <= R2? 1 <= 6 ✓
            L2 <= R1? 4 <= 3 ✗
     
   Move partition1 right...
   
   Try partition1 = 2:
     partition2 = 3 - 2 = 1
     
     nums1: [1, 3 | 5]     L1 = 3, R1 = 5
     nums2: [2 | 4, 6]     L2 = 2, R2 = 4
     
     Check: L1 <= R2? 3 <= 4 ✓
            L2 <= R1? 2 <= 5 ✓
     
     Valid! Median = (max(3, 2) + min(5, 4)) / 2 = (3 + 4) / 2 = 3.5

7. COMMON practice VARIATIONS:
   
   Q: What if arrays can have duplicates?
   A: Algorithm still works, duplicates handled naturally
   
   Q: What if one array is much larger?
   A: Always binary search on smaller → O(log(min(m, n)))
   
   Q: What if both arrays are empty?
   A: Edge case - return 0 or error

8. COMPLEXITY ANALYSIS:
   
   - Time: O(log(min(m, n))) - binary search on smaller array
   - Space: O(1) - only variables for partitions and values
   
   Key: We're not merging, just finding the right partition!

9. WHY THIS IS A GOOGLE FAVORITE:
   
   - Tests binary search mastery
   - Requires creative thinking (partition instead of merge)
   - Multiple edge cases to handle
   - Clear O(log) requirement tests algorithm knowledge

================================================================================
"""
