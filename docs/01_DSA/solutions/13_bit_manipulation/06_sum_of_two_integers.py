"""
================================================================================
PROBLEM: Sum of Two Integers (LeetCode 371)
Difficulty: Medium | Pattern: Bit Manipulation
================================================================================

PROBLEM STATEMENT:
Given two integers a and b, return the sum of the two integers without using
the operators + and -.

EXAMPLES:
    Input: a = 1, b = 2
    Output: 3

    Input: a = 2, b = 3
    Output: 5

    Input: a = -2, b = 3
    Output: 1

CONSTRAINTS:
- -1000 <= a, b <= 1000

================================================================================
"""


# ============================================================================
# SOLUTION 1: XOR for Sum + AND for Carry (Optimal)
# ============================================================================
def getSum(a: int, b: int) -> int:
    """
    Binary addition decomposed:
        a ^ b         -> sum of bits WITHOUT carry
        (a & b) << 1  -> the carry bits, shifted into position
    Repeat until there is no carry left.

    Python ints are infinite width, so we mask to 32 bits and reinterpret the
    sign manually.

    Time:  O(1)  (at most 32 carry propagations)
    Space: O(1)
    """
    mask = 0xFFFFFFFF
    MAX_INT = 0x7FFFFFFF

    while b & mask:
        carry = (a & b) << 1
        a = a ^ b
        b = carry

    a &= mask
    # If a sits in the negative range of 32-bit two's complement, convert it.
    return a if a <= MAX_INT else ~(a ^ mask)


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    print(f"getSum(1, 2)   -> {getSum(1, 2)}")    # 3
    print(f"getSum(2, 3)   -> {getSum(2, 3)}")    # 5
    print(f"getSum(-2, 3)  -> {getSum(-2, 3)}")   # 1
    print(f"getSum(-1, 1)  -> {getSum(-1, 1)}")   # 0
    print(f"getSum(-5, -7) -> {getSum(-5, -7)}")  # -12


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. THE CORE IDEA (binary addition by hand):
   - XOR gives the sum ignoring carries (0+0=0, 1+0=1, 1+1=0).
   - AND finds the positions that generate a carry; shift left by 1.
   - Loop: new_a = sum-without-carry, new_b = carry, until carry is 0.

2. WHY THE MASKING DANCE:
   Python has unbounded integers, so negative numbers never "wrap" like a real
   32-bit register. We emulate 32-bit two's complement with 0xFFFFFFFF, then
   convert values above 0x7FFFFFFF back to Python negatives.

3. SUBTRACTION VARIANT:
   a - b is the same algorithm with b negated: getSum(a, getSum(~b, 1)).

4. practice TIP:
   In Java/C++ you can drop all the masking -- the loop `while (b != 0)` with
   native int overflow just works. Say that explicitly so the interviewer knows
   the masking is a Python-specific concern, not a flaw in your logic.
"""
