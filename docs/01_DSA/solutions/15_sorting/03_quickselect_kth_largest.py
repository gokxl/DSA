"""
================================================================================
PROBLEM: Kth Largest Element in an Array (LeetCode 215)
Difficulty: Medium | Pattern: Sorting / Quickselect
================================================================================

PROBLEM STATEMENT:
Given an integer array nums and an integer k, return the kth largest element in
the array. Note that it is the kth largest element in sorted order, not the kth
distinct element.

Can you solve it without sorting (better than O(n log n))?

EXAMPLES:
    Input: nums = [3, 2, 1, 5, 6, 4], k = 2
    Output: 5

    Input: nums = [3, 2, 3, 1, 2, 4, 5, 5, 6], k = 4
    Output: 4

CONSTRAINTS:
- 1 <= k <= nums.length <= 10^5
- -10^4 <= nums[i] <= 10^4

================================================================================
"""

import heapq
import random


# ============================================================================
# SOLUTION 1: Quickselect (Optimal Average O(n))
# ============================================================================
def findKthLargest(nums: list[int], k: int) -> int:
    """
    The kth largest is the (n - k)th smallest in sorted order. Partition like
    quicksort, but recurse into only the side that contains the target index.

    Time:  O(n) average, O(n^2) worst (random pivot makes worst case rare)
    Space: O(1) in place (iterative)
    """
    target = len(nums) - k  # index this element would occupy if sorted ascending

    def partition(low: int, high: int) -> int:
        pivot_idx = random.randint(low, high)
        nums[pivot_idx], nums[high] = nums[high], nums[pivot_idx]
        pivot = nums[high]

        i = low
        for j in range(low, high):
            if nums[j] < pivot:
                nums[i], nums[j] = nums[j], nums[i]
                i += 1
        nums[i], nums[high] = nums[high], nums[i]
        return i

    low, high = 0, len(nums) - 1
    while low <= high:
        p = partition(low, high)
        if p == target:
            return nums[p]
        elif p < target:
            low = p + 1   # target is to the right
        else:
            high = p - 1  # target is to the left
    return -1  # unreachable for valid input


# ============================================================================
# SOLUTION 2: Min-Heap of Size K
# ============================================================================
def findKthLargest_heap(nums: list[int], k: int) -> int:
    """
    Keep a min-heap of the k largest seen so far. The heap root is the answer.
    Great when k is small or data streams in.

    Time:  O(n log k)
    Space: O(k)
    """
    min_heap: list[int] = []
    for num in nums:
        heapq.heappush(min_heap, num)
        if len(min_heap) > k:
            heapq.heappop(min_heap)  # discard the smallest
    return min_heap[0]


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    print(f"[3,2,1,5,6,4], k=2          -> {findKthLargest([3, 2, 1, 5, 6, 4], 2)}")   # 5
    print(f"[3,2,3,1,2,4,5,5,6], k=4    -> "
          f"{findKthLargest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4)}")                          # 4
    print(f"[1], k=1                    -> {findKthLargest([1], 1)}")                   # 1
    print(f"heap: [3,2,1,5,6,4], k=2    -> {findKthLargest_heap([3, 2, 1, 5, 6, 4], 2)}")  # 5


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. KNOW BOTH SOLUTIONS AND THEIR TRADE-OFFS:
   - Quickselect: O(n) average time, O(1) space. Best when you have all data in
     memory and want the fastest average runtime.
   - Min-heap of size k: O(n log k) time, O(k) space. Best when k is small or
     the data arrives as a STREAM (you cannot random-access it).

2. THE INDEX TRANSLATION:
   kth LARGEST == (n - k)th SMALLEST (0-indexed). Getting this mapping right is
   the single most common bug on this problem.

3. WHY QUICKSELECT BEATS FULL SORT:
   After partitioning you only recurse into ONE side, so the work halves each
   step on average: n + n/2 + n/4 + ... = O(n), versus O(n log n) for a sort.

4. RANDOM PIVOT:
   Same reason as quicksort -- avoids O(n^2) on sorted/adversarial input.

5. practice TIP:
   Ask the interviewer about constraints: streaming vs in-memory, size of k.
   That conversation naturally leads you to pick heap vs quickselect and shows
   senior-level judgment.
"""
