"""
================================================================================
PROBLEM: Sliding Window Maximum (LeetCode 239)
Difficulty: Hard | Pattern: Sliding Window + Monotonic Deque
================================================================================

PROBLEM STATEMENT:
You are given an array of integers nums, there is a sliding window of size k 
which is moving from the very left of the array to the very right. You can 
only see the k numbers in the window. Each time the sliding window moves 
right by one position.

Return the max sliding window.

EXAMPLES:
    Input: nums = [1,3,-1,-3,5,3,6,7], k = 3
    Output: [3,3,5,5,6,7]
    
    Explanation:
    Window position                Max
    ---------------               -----
    [1  3  -1] -3  5  3  6  7       3
     1 [3  -1  -3] 5  3  6  7       3
     1  3 [-1  -3  5] 3  6  7       5
     1  3  -1 [-3  5  3] 6  7       5
     1  3  -1  -3 [5  3  6] 7       6
     1  3  -1  -3  5 [3  6  7]      7

    Input: nums = [1], k = 1
    Output: [1]

CONSTRAINTS:
- 1 <= nums.length <= 10^5
- -10^4 <= nums[i] <= 10^4
- 1 <= k <= nums.length

================================================================================
"""

from typing import List
from collections import deque
import heapq


# ============================================================================
# SOLUTION 1: Monotonic Deque (Optimal)
# ============================================================================
def maxSlidingWindow(nums: List[int], k: int) -> List[int]:
    """
    Use a monotonic decreasing deque to track potential maximums.
    
    Deque stores INDICES. Front is always the current max.
    
    Key insight:
    - If nums[i] >= nums[j] and i > j, nums[j] can never be the max
    - Remove all smaller elements from back before adding
    
    Time: O(n) - each element added and removed at most once
    Space: O(k) - deque size is at most k
    """
    if not nums or k == 0:
        return []
    
    # Monotonic decreasing deque (stores indices)
    dq = deque()
    result = []
    
    for i, num in enumerate(nums):
        # Remove elements outside the window
        while dq and dq[0] <= i - k:
            dq.popleft()
        
        # Remove elements smaller than current (they can never be max)
        while dq and nums[dq[-1]] < num:
            dq.pop()
        
        # Add current index
        dq.append(i)
        
        # If we've filled the first window, start recording
        if i >= k - 1:
            result.append(nums[dq[0]])  # Front is always the max
    
    return result


# ============================================================================
# SOLUTION 2: Max Heap with Lazy Deletion
# ============================================================================
def maxSlidingWindow_heap(nums: List[int], k: int) -> List[int]:
    """
    Use a max heap (negative values for min heap).
    Lazy delete elements outside window when they would be the max.
    
    Time: O(n log n) - heap operations
    Space: O(n) - heap can grow large with lazy deletion
    """
    if not nums or k == 0:
        return []
    
    # Max heap: (-value, index)
    heap = []
    result = []
    
    for i, num in enumerate(nums):
        # Add current element
        heapq.heappush(heap, (-num, i))
        
        # Remove elements outside window (lazy deletion)
        while heap[0][1] <= i - k:
            heapq.heappop(heap)
        
        # If we've filled the first window
        if i >= k - 1:
            result.append(-heap[0][0])
    
    return result


# ============================================================================
# SOLUTION 3: Brute Force (For comparison)
# ============================================================================
def maxSlidingWindow_brute(nums: List[int], k: int) -> List[int]:
    """
    Brute force: Find max in each window.
    
    Time: O(n * k)
    Space: O(1) excluding output
    """
    if not nums or k == 0:
        return []
    
    result = []
    for i in range(len(nums) - k + 1):
        result.append(max(nums[i:i + k]))
    
    return result


# ============================================================================
# SOLUTION 4: Dynamic Programming (Block-based)
# ============================================================================
def maxSlidingWindow_dp(nums: List[int], k: int) -> List[int]:
    """
    Divide array into blocks of size k.
    Precompute left_max and right_max arrays.
    
    left_max[i] = max from start of block to i
    right_max[i] = max from i to end of block
    
    For window [i, i+k-1]:
    max = max(right_max[i], left_max[i+k-1])
    
    Time: O(n)
    Space: O(n)
    """
    n = len(nums)
    if n * k == 0:
        return []
    if k == 1:
        return nums
    
    left_max = [0] * n
    right_max = [0] * n
    
    # Build left_max: max from left within each block
    for i in range(n):
        if i % k == 0:
            left_max[i] = nums[i]
        else:
            left_max[i] = max(left_max[i - 1], nums[i])
    
    # Build right_max: max from right within each block
    for i in range(n - 1, -1, -1):
        if i == n - 1 or (i + 1) % k == 0:
            right_max[i] = nums[i]
        else:
            right_max[i] = max(right_max[i + 1], nums[i])
    
    # Build result
    result = []
    for i in range(n - k + 1):
        result.append(max(right_max[i], left_max[i + k - 1]))
    
    return result


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Standard example
    nums1, k1 = [1, 3, -1, -3, 5, 3, 6, 7], 3
    print(f"Input: nums = {nums1}, k = {k1}")
    print(f"Output (Deque): {maxSlidingWindow(nums1, k1)}")
    print(f"Output (Heap): {maxSlidingWindow_heap(nums1, k1)}")
    print(f"Output (DP): {maxSlidingWindow_dp(nums1, k1)}")
    # Expected: [3, 3, 5, 5, 6, 7]
    print()
    
    # Test Case 2: Single element
    nums2, k2 = [1], 1
    print(f"Input: nums = {nums2}, k = {k2}")
    print(f"Output: {maxSlidingWindow(nums2, k2)}")
    # Expected: [1]
    print()
    
    # Test Case 3: k equals array length
    nums3, k3 = [1, 3, -1, -3, 5], 5
    print(f"Input: nums = {nums3}, k = {k3}")
    print(f"Output: {maxSlidingWindow(nums3, k3)}")
    # Expected: [5]
    print()
    
    # Test Case 4: Decreasing array
    nums4, k4 = [9, 8, 7, 6, 5], 2
    print(f"Input: nums = {nums4}, k = {k4}")
    print(f"Output: {maxSlidingWindow(nums4, k4)}")
    # Expected: [9, 8, 7, 6]
    print()
    
    # Test Case 5: Increasing array
    nums5, k5 = [1, 2, 3, 4, 5], 2
    print(f"Input: nums = {nums5}, k = {k5}")
    print(f"Output: {maxSlidingWindow(nums5, k5)}")
    # Expected: [2, 3, 4, 5]
    print()
    
    # Test Case 6: All same elements
    nums6, k6 = [5, 5, 5, 5], 3
    print(f"Input: nums = {nums6}, k = {k6}")
    print(f"Output: {maxSlidingWindow(nums6, k6)}")
    # Expected: [5, 5]


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. WHY MONOTONIC DEQUE?
   
   Problem: Finding max in each window naively is O(k) per window = O(nk)
   
   Insight: When we see a larger element, smaller elements before it
            can NEVER be the maximum (they'll leave the window first)
   
   Solution: Maintain a decreasing deque of candidates
   - Front is always the current max
   - Pop smaller elements from back when adding larger one
   - Pop front when it leaves the window

2. MONOTONIC DEQUE INVARIANT:
   
   deque: [i1, i2, i3, ...] where nums[i1] >= nums[i2] >= nums[i3] >= ...
   
   - Decreasing order of values
   - Increasing order of indices
   - Front = current window maximum
   - All elements are potential future maximums

3. VISUAL WALKTHROUGH for [1,3,-1,-3,5,3,6,7], k=3:
   
   i=0: dq=[] → add 0 → dq=[0]                      (value 1)
   i=1: 3>1, pop 0 → add 1 → dq=[1]                 (value 3)
   i=2: -1<3, add 2 → dq=[1,2]                      (values 3,-1)
        Window complete! max = nums[1] = 3
   
   i=3: -3<-1, add 3 → dq=[1,2,3]                   (values 3,-1,-3)
        max = nums[1] = 3
   
   i=4: 5>-3, pop 3; 5>-1, pop 2; 5>3, pop 1
        add 4 → dq=[4]                              (value 5)
        max = nums[4] = 5
   
   ... continue

4. WHY HEAP APPROACH IS WORSE:
   
   - O(n log n) vs O(n) for deque
   - Lazy deletion can make heap grow to O(n) size
   - But heap is easier to implement if you forget deque!

5. DP APPROACH (ADVANCED):
   
   Blocks: [1,3,-1] [-3,5,3] [6,7]
   
   left_max[i] = max from block start to i
   right_max[i] = max from i to block end
   
   For window spanning blocks:
   max = max(right_max[window_start], left_max[window_end])

6. TEMPLATE FOR MONOTONIC DEQUE:

   dq = deque()  # stores indices
   
   for i, num in enumerate(nums):
       # 1. Remove out-of-window elements from front
       while dq and dq[0] <= i - window_size:
           dq.popleft()
       
       # 2. Remove smaller elements from back (for max)
       #    Or remove larger elements (for min)
       while dq and nums[dq[-1]] < num:
           dq.pop()
       
       # 3. Add current index
       dq.append(i)
       
       # 4. Front is the answer for current window

7. VARIATIONS:
   
   - Sliding Window Minimum: Use INCREASING deque
   - Both Min and Max: Two deques
   - Sum in window: Simple prefix sum
   - Median in window: Two heaps or sorted list

8. COMMON MISTAKES:
   - Storing values instead of indices in deque
   - Forgetting to remove out-of-window elements
   - Wrong condition for removing from back (< vs <=)
   - Starting result collection too early (before k elements)

9. RELATED PROBLEMS:
   - Shortest Subarray with Sum at Least K (LC 862)
   - Constrained Subsequence Sum (LC 1425)
   - Jump Game VI (LC 1696)
   - Max Value of Equation (LC 1499)

10. practice TIP:
    
    Start by explaining the brute force O(nk) approach.
    Then explain why monotonic deque helps:
    "Elements that are smaller than a newer element can never be the max"

================================================================================
"""
