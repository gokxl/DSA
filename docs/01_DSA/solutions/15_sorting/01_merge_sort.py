"""
================================================================================
PROBLEM: Merge Sort (Sort an Array - LeetCode 912)
Difficulty: Medium | Pattern: Sorting / Divide and Conquer
================================================================================

PROBLEM STATEMENT:
Given an array of integers nums, sort the array in ascending order and return
it. You must solve it in O(n log n) time without using built-in sort.

Merge Sort is the canonical stable, guaranteed O(n log n) algorithm. It is also
the foundation for "count inversions" and "merge k lists" style problems.

EXAMPLES:
    Input: nums = [5, 2, 3, 1]
    Output: [1, 2, 3, 5]

    Input: nums = [5, 1, 1, 2, 0, 0]
    Output: [0, 0, 1, 1, 2, 5]

CONSTRAINTS:
- 1 <= nums.length <= 5 * 10^4
- -5 * 10^4 <= nums[i] <= 5 * 10^4

================================================================================
"""


# ============================================================================
# SOLUTION 1: Top-Down Merge Sort (Recursive, Optimal)
# ============================================================================
def mergeSort(nums: list[int]) -> list[int]:
    """
    Divide the array in half, sort each half recursively, then merge the two
    sorted halves back together.

    Time:  O(n log n)  -- log n levels, O(n) merge work per level
    Space: O(n)        -- temporary arrays during merge
    Stable: yes
    """
    if len(nums) <= 1:
        return nums

    mid = len(nums) // 2
    left = mergeSort(nums[:mid])
    right = mergeSort(nums[mid:])
    return _merge(left, right)


def _merge(left: list[int], right: list[int]) -> list[int]:
    """Merge two sorted lists into one sorted list. Time O(n), Space O(n)."""
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        # '<=' keeps equal elements in original order -> stability.
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    print(f"[5, 2, 3, 1]        -> {mergeSort([5, 2, 3, 1])}")
    print(f"[5, 1, 1, 2, 0, 0]  -> {mergeSort([5, 1, 1, 2, 0, 0])}")
    print(f"[1]                 -> {mergeSort([1])}")
    print(f"[]                  -> {mergeSort([])}")
    print(f"[3, -1, 0, -5, 8]   -> {mergeSort([3, -1, 0, -5, 8])}")


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. WHY MERGE SORT MATTERS:
   - Guaranteed O(n log n) in the WORST case (quicksort is O(n^2) worst case).
   - Stable (preserves order of equal keys) -- important for multi-key sorts.
   - The merge step is the engine behind Merge K Sorted Lists (LC 23) and
     Count of Smaller Numbers After Self (LC 315 / inversion counting).

2. THE MERGE STEP IS THE CORE SKILL:
   Two pointers walking two sorted lists, always taking the smaller head. Make
   sure you can write _merge flawlessly -- it reappears everywhere.

3. STABILITY DETAIL:
   Using `left[i] <= right[j]` (not `<`) takes from the left half on ties,
   preserving original relative order. Flipping to `<` would break stability.

4. SPACE vs QUICKSORT:
   Merge sort needs O(n) auxiliary space; quicksort sorts in place with O(log n)
   stack. Mention this trade-off -- it is a common follow-up.

5. HOW TO EXPLAIN IT:
   If asked to sort without built-ins, merge sort is the safest choice because
   its O(n log n) bound holds regardless of input (no adversarial pivot risk).
"""
