"""
================================================================================
PROBLEM: Sort Colors / Dutch National Flag (LeetCode 75)
Difficulty: Medium | Pattern: Sorting / Three-Way Partition
================================================================================

PROBLEM STATEMENT:
Given an array nums with n objects colored red, white, or blue, sort them
in-place so that objects of the same color are adjacent, in the order red,
white, and blue.

We use 0, 1, and 2 to represent red, white, and blue respectively.

You must solve this without using the library's sort function, in ONE PASS and
O(1) extra space.

EXAMPLES:
    Input: nums = [2, 0, 2, 1, 1, 0]
    Output: [0, 0, 1, 1, 2, 2]

    Input: nums = [2, 0, 1]
    Output: [0, 1, 2]

CONSTRAINTS:
- n == nums.length
- 1 <= n <= 300
- nums[i] is either 0, 1, or 2.

================================================================================
"""


# ============================================================================
# SOLUTION 1: Dutch National Flag - Three Pointers (Optimal, One Pass)
# ============================================================================
def sortColors(nums: list[int]) -> None:
    """
    Maintain three regions with pointers:
        [0 .. low-1]   -> all 0s
        [low .. mid-1] -> all 1s
        [high+1 .. end]-> all 2s
        [mid .. high]  -> unprocessed

    Walk mid forward:
        0 -> swap into low region, advance low and mid
        1 -> already in place, advance mid
        2 -> swap to high region, shrink high (do NOT advance mid: the swapped-in
             value is still unexamined)

    Time:  O(n), single pass
    Space: O(1), in place
    """
    low, mid, high = 0, 0, len(nums) - 1

    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:  # nums[mid] == 2
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1


# ============================================================================
# SOLUTION 2: Counting Sort (Two Pass - simpler to reason about)
# ============================================================================
def sortColors_counting(nums: list[int]) -> None:
    """
    Count how many 0s, 1s, 2s exist, then overwrite the array in order.

    Time:  O(n), two passes
    Space: O(1)  (fixed-size count array)
    """
    counts = [0, 0, 0]
    for num in nums:
        counts[num] += 1

    i = 0
    for color in range(3):
        for _ in range(counts[color]):
            nums[i] = color
            i += 1


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    a = [2, 0, 2, 1, 1, 0]
    sortColors(a)
    print(f"[2,0,2,1,1,0] -> {a}")  # [0, 0, 1, 1, 2, 2]

    b = [2, 0, 1]
    sortColors(b)
    print(f"[2,0,1]       -> {b}")  # [0, 1, 2]

    c = [0]
    sortColors(c)
    print(f"[0]           -> {c}")  # [0]

    d = [1, 2, 0, 2, 1, 0, 1]
    sortColors_counting(d)
    print(f"counting sort -> {d}")  # [0, 0, 1, 1, 1, 2, 2]


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. DUTCH NATIONAL FLAG ALGORITHM (Dijkstra):
   The classic three-pointer in-place partition into < / == / > a pivot. Here
   the pivot is implicitly 1. This pattern generalizes to any 3-way split.

2. THE ONE SUBTLE BUG:
   When you swap a 2 to the back, do NOT advance mid. The element you pulled
   from `high` has not been examined yet. For a 0-swap you CAN advance mid,
   because low <= mid guarantees the swapped value is a known 1.

3. ONE PASS vs TWO PASS:
   Counting sort (two pass) is trivial and perfectly acceptable, but the
   interviewer usually wants the ONE-pass, O(1)-space DNF solution.

4. WHERE THREE-WAY PARTITION HELPS ELSEWHERE:
   Quicksort with many duplicate keys uses 3-way partitioning to avoid O(n^2).
   Same core idea as this problem.

5. practice TIP:
   Draw the four regions (0s | 1s | unknown | 2s) and narrate how each move
   shrinks the unknown region. The invariant makes the pointer logic obvious.
"""
