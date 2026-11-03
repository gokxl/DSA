"""
================================================================================
PROBLEM: Find Peak Element (LeetCode 162)
Difficulty: Medium | Pattern: Binary Search + Local Maximum
================================================================================

PROBLEM STATEMENT:
A peak element is an element that is strictly greater than its neighbors.

Given a 0-indexed integer array nums, find a peak element, and return its index. 
If the array contains multiple peaks, return the index to ANY of the peaks.

You may imagine that nums[-1] = nums[n] = -∞. In other words, an element is 
always considered to be strictly greater than a neighbor that is outside the array.

You must write an algorithm that runs in O(log n) time.

EXAMPLES:
    Input: nums = [1,2,3,1]
    Output: 2
    Explanation: 3 is a peak element. Index 2 is returned.

    Input: nums = [1,2,1,3,5,6,4]
    Output: 5
    Explanation: Could return index 1 (peak 2) or index 5 (peak 6).

CONSTRAINTS:
- 1 <= nums.length <= 1000
- -2^31 <= nums[i] <= 2^31 - 1
- nums[i] != nums[i + 1] for all valid i

================================================================================
"""

from typing import List


# ============================================================================
# SOLUTION 1: Binary Search (Optimal)
# ============================================================================
def findPeakElement(nums: List[int]) -> int:
    """
    Key insight: If nums[mid] < nums[mid+1], peak MUST exist on the right.
    
    Why? The array ends at -∞, so if we're going up, we must come down 
    somewhere, creating a peak.
    
    Time: O(log n)
    Space: O(1)
    """
    left, right = 0, len(nums) - 1
    
    while left < right:
        mid = left + (right - left) // 2
        
        if nums[mid] < nums[mid + 1]:
            # Ascending slope: peak is on the right
            left = mid + 1
        else:
            # Descending slope: peak is on the left (including mid)
            right = mid
    
    return left


# ============================================================================
# SOLUTION 2: Binary Search with Explicit Comparison
# ============================================================================
def findPeakElement_explicit(nums: List[int]) -> int:
    """
    More explicit version: check both neighbors.
    
    Time: O(log n)
    Space: O(1)
    """
    n = len(nums)
    
    if n == 1:
        return 0
    
    # Check boundaries first
    if nums[0] > nums[1]:
        return 0
    if nums[n - 1] > nums[n - 2]:
        return n - 1
    
    left, right = 1, n - 2
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if nums[mid] > nums[mid - 1] and nums[mid] > nums[mid + 1]:
            # Found a peak
            return mid
        elif nums[mid] < nums[mid + 1]:
            # Ascending: go right
            left = mid + 1
        else:
            # Descending: go left
            right = mid - 1
    
    return left


# ============================================================================
# SOLUTION 3: Iterative Linear Scan (For comparison)
# ============================================================================
def findPeakElement_linear(nums: List[int]) -> int:
    """
    Simple O(n) solution: find first descending point.
    
    Time: O(n)
    Space: O(1)
    """
    for i in range(len(nums) - 1):
        if nums[i] > nums[i + 1]:
            return i
    
    return len(nums) - 1


# ============================================================================
# SOLUTION 4: Recursive Binary Search
# ============================================================================
def findPeakElement_recursive(nums: List[int]) -> int:
    """
    Recursive version of binary search.
    
    Time: O(log n)
    Space: O(log n) for call stack
    """
    def search(left: int, right: int) -> int:
        if left == right:
            return left
        
        mid = left + (right - left) // 2
        
        if nums[mid] < nums[mid + 1]:
            return search(mid + 1, right)
        else:
            return search(left, mid)
    
    return search(0, len(nums) - 1)


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Single peak in middle
    nums1 = [1, 2, 3, 1]
    print(f"Input: {nums1}")
    print(f"Output (Binary): {findPeakElement(nums1)}")
    print(f"Output (Explicit): {findPeakElement_explicit(nums1)}")
    print(f"Output (Recursive): {findPeakElement_recursive(nums1)}")
    # Expected: 2
    print()
    
    # Test Case 2: Multiple peaks
    nums2 = [1, 2, 1, 3, 5, 6, 4]
    print(f"Input: {nums2}")
    result = findPeakElement(nums2)
    print(f"Output: {result} (valid peaks: 1 or 5)")
    # Expected: 1 or 5
    print()
    
    # Test Case 3: Single element
    nums3 = [1]
    print(f"Input: {nums3}")
    print(f"Output: {findPeakElement(nums3)}")
    # Expected: 0
    print()
    
    # Test Case 4: Two elements (ascending)
    nums4 = [1, 2]
    print(f"Input: {nums4}")
    print(f"Output: {findPeakElement(nums4)}")
    # Expected: 1
    print()
    
    # Test Case 5: Two elements (descending)
    nums5 = [2, 1]
    print(f"Input: {nums5}")
    print(f"Output: {findPeakElement(nums5)}")
    # Expected: 0
    print()
    
    # Test Case 6: Strictly increasing
    nums6 = [1, 2, 3, 4, 5]
    print(f"Input: {nums6}")
    print(f"Output: {findPeakElement(nums6)}")
    # Expected: 4
    print()
    
    # Test Case 7: Strictly decreasing
    nums7 = [5, 4, 3, 2, 1]
    print(f"Input: {nums7}")
    print(f"Output: {findPeakElement(nums7)}")
    # Expected: 0


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. KEY INSIGHT: BINARY SEARCH ON UNSORTED ARRAY!
   
   This problem shows binary search can work on unsorted arrays
   when we're looking for a LOCAL property (not a global target).
   
   We're not searching for a specific value, but for a local maximum.

2. WHY BINARY SEARCH WORKS:
   
   Imagine nums = [1, 2, 3, ...?...]
   
   At position mid:
   - If nums[mid] < nums[mid+1]: We're ascending!
     Since nums[n] = -∞, we MUST come down eventually.
     So a peak MUST exist on the right side.
   
   - If nums[mid] > nums[mid+1]: We're descending!
     Either mid is a peak, or there's a peak on the left.
     So a peak exists on left side (including mid).

3. VISUAL EXPLANATION:
   
   nums = [1, 2, 1, 3, 5, 6, 4]
   -∞                          -∞
   
        2       6 ← peaks
       / \     / \
      1   1   5   4
             /
            3
   
   Binary search converges to one of the peaks.

4. THE GUARANTEE:
   
   A peak is ALWAYS guaranteed because:
   - nums[-1] = nums[n] = -∞
   - Adjacent elements are different
   - Therefore, there's always a "hill" somewhere

5. LOOP INVARIANT:
   
   At any point, [left, right] contains at least one peak.
   
   - If ascending at mid → peak in [mid+1, right]
   - If descending at mid → peak in [left, mid]
   
   We never eliminate the peak from our search range!

6. SUBTLE POINT - WHY right = mid, NOT mid - 1:
   
   When nums[mid] > nums[mid+1]:
   - mid itself could be a peak!
   - We can't exclude it
   - So right = mid (not mid - 1)

7. EDGE CASES:
   
   - Single element: Always a peak (neighbors are -∞)
   - Strictly increasing: Last element is peak
   - Strictly decreasing: First element is peak
   - Two elements: Higher one is peak

8. COMPARISON WITH LINEAR SCAN:
   
   Linear scan finds FIRST point where we start descending:
   for i in range(n-1):
       if nums[i] > nums[i+1]:
           return i
   return n-1
   
   This is O(n) but simpler. Binary search is O(log n).

9. RELATED PROBLEMS:
   - Find Peak Element II (2D matrix) - LC 1901
   - Find in Mountain Array - LC 1095
   - Peak Index in Mountain Array - LC 852
   - Find Minimum in Rotated Array - LC 153

10. practice TIP:
    
    When asked "Why can we use binary search on unsorted array?":
    
    "Because we're looking for a LOCAL property (peak), not a global 
    target. By comparing mid with mid+1, we can always determine which 
    half contains at least one peak."

================================================================================
"""
