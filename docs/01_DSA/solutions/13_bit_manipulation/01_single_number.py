"""
================================================================================
PROBLEM: Single Number (LeetCode 136)
Difficulty: Easy | Pattern: Bit Manipulation
================================================================================

PROBLEM STATEMENT:
Given a non-empty array of integers nums, every element appears twice except
for one. Find that single one.

You must implement a solution with O(n) time and O(1) extra space.

EXAMPLES:
    Input: nums = [2, 2, 1]
    Output: 1

    Input: nums = [4, 1, 2, 1, 2]
    Output: 4

    Input: nums = [1]
    Output: 1

CONSTRAINTS:
- 1 <= nums.length <= 3 * 10^4
- -3 * 10^4 <= nums[i] <= 3 * 10^4
- Each element appears twice except for one which appears once.

================================================================================
"""


# ============================================================================
# SOLUTION 1: XOR (Optimal)
# ============================================================================
def singleNumber(nums: list[int]) -> int:
    """
    XOR has two magic properties:
        x ^ x = 0   (a number XORed with itself cancels out)
        x ^ 0 = x   (XOR with zero leaves the number unchanged)
    XOR is also commutative, so pairs cancel regardless of order,
    leaving only the unique number.

    Time:  O(n)
    Space: O(1)
    """
    result = 0
    for num in nums:
        result ^= num
    return result


# ============================================================================
# SOLUTION 2: HashSet (Uses extra space - for contrast)
# ============================================================================
def singleNumber_set(nums: list[int]) -> int:
    """
    Add on first sight, remove on second. What remains is the single number.

    Time:  O(n)
    Space: O(n)  -- violates the O(1) requirement, shown only for comparison
    """
    seen: set[int] = set()
    for num in nums:
        if num in seen:
            seen.remove(num)
        else:
            seen.add(num)
    return seen.pop()


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    print(f"[2, 2, 1]        -> {singleNumber([2, 2, 1])}")        # 1
    print(f"[4, 1, 2, 1, 2]  -> {singleNumber([4, 1, 2, 1, 2])}")  # 4
    print(f"[1]              -> {singleNumber([1])}")              # 1
    print(f"[-1, -1, -2]     -> {singleNumber([-1, -1, -2])}")     # -2


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. WHY XOR WORKS:
   For [4, 1, 2, 1, 2]:
       0 ^ 4 = 4
       4 ^ 1 = 5
       5 ^ 2 = 7
       7 ^ 1 = 6
       6 ^ 2 = 4   <- the duplicates (1,1) and (2,2) canceled out

2. THE TWO PROPERTIES TO MEMORIZE:
   - self-inverse:  x ^ x = 0
   - identity:      x ^ 0 = x
   - commutative/associative: order does not matter

3. FOLLOW-UPS YOU SHOULD KNOW:
   - Single Number II (LC 137): every element appears 3x except one.
     Use bit counting mod 3, or (ones, twos) state machine.
   - Single Number III (LC 260): exactly TWO numbers appear once.
     XOR everything, isolate lowest set bit to split into two groups.

4. HOW TO EXPLAIN IT:
   Mention you can do it with a HashSet in O(n) space first, then upgrade
   to the O(1) XOR trick. Showing the progression reads well.
"""
