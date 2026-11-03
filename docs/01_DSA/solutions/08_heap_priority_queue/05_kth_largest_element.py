"""
================================================================================
PROBLEM: Kth Largest Element in an Array (LeetCode 215)
Difficulty: Medium | Pattern: Heap / Quick Select
================================================================================

PROBLEM STATEMENT:
Given an integer array nums and an integer k, return the kth largest element 
in the array.

Note that it is the kth largest element in the sorted order, not the kth 
distinct element.

Can you solve it without sorting?

EXAMPLES:
    Input: nums = [3,2,1,5,6,4], k = 2
    Output: 5
    
    Input: nums = [3,2,3,1,2,4,5,5,6], k = 4
    Output: 4

CONSTRAINTS:
- 1 <= k <= nums.length <= 10^5
- -10^4 <= nums[i] <= 10^4

================================================================================
"""
from typing import List
import heapq
import random


# ============================================================================
# SOLUTION 1: Min-Heap of Size K (Optimal for streaming)
# ============================================================================
def findKthLargest_heap(nums: List[int], k: int) -> int:
    """
    Use min-heap of size k to track k largest elements.
    
    Time: O(n log k)
    Space: O(k)
    """
    min_heap = []
    
    for num in nums:
        heapq.heappush(min_heap, num)
        if len(min_heap) > k:
            heapq.heappop(min_heap)  # Remove smallest
    
    return min_heap[0]  # kth largest is the smallest among k largest


# ============================================================================
# SOLUTION 2: Quick Select (Optimal average time)
# ============================================================================
def findKthLargest_quickselect(nums: List[int], k: int) -> int:
    """
    Quick Select algorithm - partition like quicksort but only recurse one side.
    
    Time: O(n) average, O(n²) worst case
    Space: O(1)
    """
    # Convert kth largest to kth smallest from end
    k = len(nums) - k
    
    def partition(left: int, right: int) -> int:
        pivot = nums[right]
        i = left
        
        for j in range(left, right):
            if nums[j] <= pivot:
                nums[i], nums[j] = nums[j], nums[i]
                i += 1
        
        nums[i], nums[right] = nums[right], nums[i]
        return i
    
    def quickselect(left: int, right: int) -> int:
        if left == right:
            return nums[left]
        
        pivot_idx = partition(left, right)
        
        if k == pivot_idx:
            return nums[k]
        elif k < pivot_idx:
            return quickselect(left, pivot_idx - 1)
        else:
            return quickselect(pivot_idx + 1, right)
    
    return quickselect(0, len(nums) - 1)


# ============================================================================
# SOLUTION 3: Randomized Quick Select (Better worst case)
# ============================================================================
def findKthLargest_randomized(nums: List[int], k: int) -> int:
    """
    Quick Select with random pivot selection.
    Avoids worst case for sorted/nearly-sorted arrays.
    
    Time: O(n) average (better constants with randomization)
    Space: O(1)
    """
    k = len(nums) - k  # Convert to index
    
    def partition(left: int, right: int) -> int:
        # Random pivot
        pivot_idx = random.randint(left, right)
        nums[pivot_idx], nums[right] = nums[right], nums[pivot_idx]
        
        pivot = nums[right]
        i = left
        
        for j in range(left, right):
            if nums[j] <= pivot:
                nums[i], nums[j] = nums[j], nums[i]
                i += 1
        
        nums[i], nums[right] = nums[right], nums[i]
        return i
    
    left, right = 0, len(nums) - 1
    
    while left <= right:
        pivot_idx = partition(left, right)
        
        if pivot_idx == k:
            return nums[k]
        elif k < pivot_idx:
            right = pivot_idx - 1
        else:
            left = pivot_idx + 1
    
    return -1  # Should never reach


# ============================================================================
# SOLUTION 4: Using heapq.nlargest
# ============================================================================
def findKthLargest_nlargest(nums: List[int], k: int) -> int:
    """
    Python's built-in - uses heap internally.
    
    Time: O(n log k) when k << n
    Space: O(k)
    """
    return heapq.nlargest(k, nums)[-1]


# ============================================================================
# SOLUTION 5: Max-Heap (For reference)
# ============================================================================
def findKthLargest_maxheap(nums: List[int], k: int) -> int:
    """
    Build max-heap, pop k-1 times.
    
    Time: O(n + k log n)
    Space: O(n) for heap
    """
    # Negate for max-heap
    max_heap = [-x for x in nums]
    heapq.heapify(max_heap)
    
    for _ in range(k - 1):
        heapq.heappop(max_heap)
    
    return -max_heap[0]


# ============================================================================
# SOLUTION 6: Sorting (Simple but not optimal)
# ============================================================================
def findKthLargest_sort(nums: List[int], k: int) -> int:
    """
    Sort and return kth element from end.
    
    Time: O(n log n)
    Space: O(n) or O(1) depending on sort implementation
    """
    nums.sort()
    return nums[-k]


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Standard case
    nums1, k1 = [3, 2, 1, 5, 6, 4], 2
    print(f"nums={nums1}, k={k1}")
    print(f"Heap: {findKthLargest_heap(nums1.copy(), k1)}")
    print(f"QuickSelect: {findKthLargest_quickselect(nums1.copy(), k1)}")
    print(f"nlargest: {findKthLargest_nlargest(nums1.copy(), k1)}")
    # Expected: 5
    print()
    
    # Test Case 2: With duplicates
    nums2, k2 = [3, 2, 3, 1, 2, 4, 5, 5, 6], 4
    print(f"nums={nums2}, k={k2}")
    print(f"Result: {findKthLargest_heap(nums2.copy(), k2)}")
    # Expected: 4 (sorted: [1,2,2,3,3,4,5,5,6], 4th largest = 4)
    print()
    
    # Test Case 3: k = 1 (maximum)
    nums3, k3 = [1, 2, 3, 4, 5], 1
    print(f"nums={nums3}, k={k3}")
    print(f"Result: {findKthLargest_randomized(nums3.copy(), k3)}")
    # Expected: 5
    print()
    
    # Test Case 4: k = n (minimum)
    nums4, k4 = [1, 2, 3, 4, 5], 5
    print(f"nums={nums4}, k={k4}")
    print(f"Result: {findKthLargest_heap(nums4.copy(), k4)}")
    # Expected: 1
    print()
    
    # Test Case 5: Negative numbers
    nums5, k5 = [-1, -2, -3, -4], 2
    print(f"nums={nums5}, k={k5}")
    print(f"Result: {findKthLargest_heap(nums5.copy(), k5)}")
    # Expected: -2


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. TWO MAIN APPROACHES:
   
   Min-Heap of size k:
   - Time: O(n log k)
   - Space: O(k)
   - Great for streaming data
   
   Quick Select:
   - Time: O(n) average
   - Space: O(1)
   - Better for static arrays

2. WHY MIN-HEAP (NOT MAX-HEAP)?
   
   We want k largest elements.
   Min-heap of size k keeps track of them:
   - Always remove smallest when full
   - At end, heap has k largest
   - Top of min-heap = smallest of k largest = kth largest

3. QUICK SELECT INSIGHT:
   
   Like quicksort, but only recurse on one side.
   
   After partition:
   - Pivot is in final sorted position
   - If pivot_idx == k, found it!
   - If k < pivot_idx, search left
   - If k > pivot_idx, search right

4. KTH LARGEST VS KTH SMALLEST:
   
   kth largest = (n-k)th smallest
   
   If using 0-indexed:
   - Index of kth largest = len(nums) - k

5. RANDOMIZED QUICK SELECT:
   
   Random pivot avoids worst case for:
   - Already sorted arrays
   - Reverse sorted arrays
   
   Expected time: O(n) with very high probability

6. COMPARISON:
   
   | Approach      | Time      | Space | Best For          |
   |---------------|-----------|-------|-------------------|
   | Min-Heap      | O(n log k)| O(k)  | Streaming data    |
   | Quick Select  | O(n) avg  | O(1)  | Static arrays     |
   | Sorting       | O(n log n)| O(n)  | Simple impl       |

7. STREAMING VARIANT:
   
   "Kth Largest Element in a Stream" (LC 703)
   - Use min-heap of size k
   - Each add: O(log k)

8. COMMON MISTAKES:
   
   ❌ Using max-heap (less efficient)
   ❌ Off-by-one with kth index
   ❌ Not handling duplicates (they count!)

9. RELATED PROBLEMS:
   
   - Kth Smallest Element in BST (LC 230)
   - Top K Frequent Elements (LC 347)
   - K Closest Points to Origin (LC 973)

10. HOW TO EXPLAIN IT:
    
    "For static arrays, I'd use Quick Select for O(n) average time.
    For streaming data, I'd use a min-heap of size k for O(n log k).
    
    The heap approach is simpler and works well when k is much
    smaller than n. The heap keeps track of the k largest elements,
    and the top (minimum) of the heap is the kth largest overall."
    
    Know both approaches - interviewer might ask for specific one!

================================================================================
"""
