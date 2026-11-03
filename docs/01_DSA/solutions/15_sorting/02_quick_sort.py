"""
================================================================================
PROBLEM: Quick Sort (Sort an Array - LeetCode 912)
Difficulty: Medium | Pattern: Sorting / Divide and Conquer
================================================================================

PROBLEM STATEMENT:
Sort an array of integers in ascending order using Quick Sort. Quick Sort sorts
in place and is the basis for Quickselect (Kth Largest Element).

EXAMPLES:
    Input: nums = [5, 2, 3, 1]
    Output: [1, 2, 3, 5]

    Input: nums = [3, 3, 1, 2, 1]
    Output: [1, 1, 2, 3, 3]

CONSTRAINTS:
- 1 <= nums.length <= 5 * 10^4
- -5 * 10^4 <= nums[i] <= 5 * 10^4

================================================================================
"""

import random


# ============================================================================
# SOLUTION 1: In-Place Quick Sort with Randomized Pivot (Optimal)
# ============================================================================
def quickSort(nums: list[int]) -> list[int]:
    """
    Pick a pivot, partition so that smaller elements go left and larger go
    right, then recurse on each side. Randomizing the pivot avoids the O(n^2)
    worst case on already-sorted input.

    Time:  O(n log n) average, O(n^2) worst (rare with random pivot)
    Space: O(log n) average recursion stack; O(n) worst case (in-place)
    Stable: no
    """
    def partition(low: int, high: int) -> int:
        # Randomized pivot -> swap it to the end as the pivot slot.
        pivot_idx = random.randint(low, high)
        nums[pivot_idx], nums[high] = nums[high], nums[pivot_idx]
        pivot = nums[high]

        i = low  # boundary: everything left of i is < pivot
        for j in range(low, high):
            if nums[j] < pivot:
                nums[i], nums[j] = nums[j], nums[i]
                i += 1
        # Place pivot into its final sorted position.
        nums[i], nums[high] = nums[high], nums[i]
        return i

    def sort(low: int, high: int) -> None:
        if low < high:
            p = partition(low, high)
            sort(low, p - 1)
            sort(p + 1, high)

    sort(0, len(nums) - 1)
    return nums


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    print(f"[5, 2, 3, 1]      -> {quickSort([5, 2, 3, 1])}")
    print(f"[3, 3, 1, 2, 1]   -> {quickSort([3, 3, 1, 2, 1])}")
    print(f"[1]               -> {quickSort([1])}")
    print(f"[5, 4, 3, 2, 1]   -> {quickSort([5, 4, 3, 2, 1])}")
    print(f"[-2, 0, -5, 8, 3] -> {quickSort([-2, 0, -5, 8, 3])}")


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. THE PARTITION STEP IS EVERYTHING:
   Lomuto partition keeps a boundary i: elements left of i are < pivot. Walk j
   across the range, swapping smaller elements into the boundary. Finally drop
   the pivot at i. Master this -- Quickselect reuses it directly.

2. WHY RANDOMIZE THE PIVOT:
   A fixed pivot (first/last) degrades to O(n^2) on sorted or reverse-sorted
   input -- a classic adversarial case. A random pivot makes that vanishingly
   unlikely, giving reliable O(n log n) average time.

3. QUICKSORT vs MERGESORT (know the trade-offs):
   - Quicksort: in place, O(log n) space, usually faster constants, NOT stable,
     O(n^2) worst case.
   - Mergesort: stable, guaranteed O(n log n), but needs O(n) extra space.

4. THE PAYOFF -- QUICKSELECT:
   If you only need the k-th element, recurse into ONE side after partition.
   That drops average time to O(n). See 03_quickselect_kth_largest.py.

5. HOW TO EXPLAIN IT:
   State the worst case up front and explain the random-pivot mitigation. It
   shows you understand WHY the algorithm is safe, not just how to code it.
"""
