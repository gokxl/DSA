"""
================================================================================
PROBLEM: GCD and LCM (Euclidean Algorithm)
Difficulty: Easy | Pattern: Math / Number Theory
================================================================================

PROBLEM STATEMENT:
Compute the Greatest Common Divisor (GCD) and Least Common Multiple (LCM) of
two integers. These are building blocks that show up inside many practice
problems (fractions, cycles, array reductions like LC 1071/1979/914).

DEFINITIONS:
    GCD(a, b): the largest integer that divides both a and b.
    LCM(a, b): the smallest positive integer divisible by both a and b.

RELATIONSHIP:
    LCM(a, b) = a * b / GCD(a, b)

EXAMPLES:
    GCD(12, 18) = 6      LCM(12, 18) = 36
    GCD(7, 13)  = 1      LCM(7, 13)  = 91   (coprime)
    GCD(0, 5)   = 5      LCM(0, 5)   = 0

================================================================================
"""


# ============================================================================
# SOLUTION 1: Euclidean Algorithm - Iterative (Optimal)
# ============================================================================
def gcd(a: int, b: int) -> int:
    """
    GCD(a, b) = GCD(b, a mod b), shrinking the problem until b becomes 0.

    Time:  O(log(min(a, b)))
    Space: O(1)
    """
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    """
    LCM via the GCD relationship. Divide before multiply to limit overflow in
    fixed-width languages (not an issue in Python).

    Time:  O(log(min(a, b)))
    Space: O(1)
    """
    if a == 0 or b == 0:
        return 0
    return abs(a) // gcd(a, b) * abs(b)


# ============================================================================
# SOLUTION 2: Euclidean Algorithm - Recursive
# ============================================================================
def gcd_recursive(a: int, b: int) -> int:
    """
    Classic recursive form. Time: O(log(min(a,b))). Space: O(log) stack.
    """
    if b == 0:
        return abs(a)
    return gcd_recursive(b, a % b)


# ============================================================================
# SOLUTION 3: GCD of a Whole Array
# ============================================================================
def gcd_of_array(nums: list[int]) -> int:
    """
    GCD is associative, so fold it across the array.
    Early-exit once it reaches 1 (cannot get smaller).

    Time:  O(n * log(max))
    Space: O(1)
    """
    result = nums[0]
    for num in nums[1:]:
        result = gcd(result, num)
        if result == 1:
            break
    return result


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    print(f"gcd(12, 18) -> {gcd(12, 18)}")   # 6
    print(f"gcd(7, 13)  -> {gcd(7, 13)}")    # 1
    print(f"gcd(0, 5)   -> {gcd(0, 5)}")     # 5
    print(f"lcm(12, 18) -> {lcm(12, 18)}")   # 36
    print(f"lcm(4, 6)   -> {lcm(4, 6)}")     # 12
    print(f"gcd_of_array([12, 18, 24]) -> {gcd_of_array([12, 18, 24])}")  # 6


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. THE EUCLIDEAN INSIGHT:
   Any common divisor of a and b also divides (a mod b). So replacing a with
   (a mod b) preserves the GCD while shrinking the numbers fast -- O(log) steps.

2. LCM FROM GCD:
   LCM(a, b) = a / GCD(a, b) * b. Always divide first to keep intermediate
   values small (overflow safety in C++/Java).

3. WHERE THIS SHOWS UP:
   - Simplifying fractions.
   - Cycle/period problems (when two cycles realign => LCM).
   - LC 1071 (GCD of Strings), LC 914 (X of a Kind), LC 1979.
   - Python ships math.gcd and math.lcm -- know them, but be able to derive.

4. practice TIP:
   Memorize the two-line iterative gcd: `while b: a, b = b, a % b`. It is one of
   the highest-value snippets to have in muscle memory.
"""
