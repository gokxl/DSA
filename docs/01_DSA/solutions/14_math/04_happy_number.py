"""
================================================================================
PROBLEM: Happy Number (LeetCode 202)
Difficulty: Easy | Pattern: Math / Cycle Detection
================================================================================

PROBLEM STATEMENT:
Write an algorithm to determine if a number n is happy.

A happy number is defined by the following process:
- Starting with any positive integer, replace the number by the sum of the
  squares of its digits.
- Repeat until the number equals 1 (happy), or it loops endlessly in a cycle
  that never includes 1 (not happy).

Return true if n is a happy number, false otherwise.

EXAMPLES:
    Input: n = 19
    Output: true
    Explanation:
        1^2 + 9^2 = 82
        8^2 + 2^2 = 68
        6^2 + 8^2 = 100
        1^2 + 0^2 + 0^2 = 1

    Input: n = 2
    Output: false

CONSTRAINTS:
- 1 <= n <= 2^31 - 1

================================================================================
"""


# ============================================================================
# SOLUTION 1: Floyd's Cycle Detection (O(1) Space, Optimal)
# ============================================================================
def isHappy(n: int) -> bool:
    """
    The digit-square process either reaches 1 or falls into a cycle. That is
    exactly the "linked list cycle" structure -> use slow/fast pointers.

    Time:  O(log n) per step, bounded total steps
    Space: O(1)
    """
    def next_number(x: int) -> int:
        total = 0
        while x:
            x, digit = divmod(x, 10)
            total += digit * digit
        return total

    slow = n
    fast = next_number(n)
    while fast != 1 and slow != fast:
        slow = next_number(slow)
        fast = next_number(next_number(fast))
    return fast == 1


# ============================================================================
# SOLUTION 2: HashSet to Detect Repeats
# ============================================================================
def isHappy_set(n: int) -> bool:
    """
    Remember every number we have seen. If one repeats before we hit 1, we are
    in a cycle -> not happy.

    Time:  O(log n) per step
    Space: O(k) for the set of seen numbers
    """
    seen: set[int] = set()
    while n != 1 and n not in seen:
        seen.add(n)
        n = sum(int(d) ** 2 for d in str(n))
    return n == 1


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    print(f"isHappy(19) -> {isHappy(19)}")  # True
    print(f"isHappy(2)  -> {isHappy(2)}")   # False
    print(f"isHappy(1)  -> {isHappy(1)}")   # True
    print(f"isHappy(7)  -> {isHappy(7)}")   # True
    print(f"isHappy(4)  -> {isHappy(4)}")   # False


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. THE REFRAME THAT UNLOCKS IT:
   "Does this sequence end at 1 or loop forever?" is cycle detection. Recognizing
   that lets you reuse Floyd's tortoise-and-hare for O(1) space.

2. WHY THE PROCESS ALWAYS TERMINATES:
   For any number, the digit-square sum shrinks into a small bounded range
   (below ~243 for reasonable inputs), so by pigeonhole it must eventually
   repeat -> guaranteed to hit 1 or a cycle. No infinite growth.

3. TWO VALID APPROACHES:
   - HashSet: simplest to write, O(k) space.
   - Floyd's cycle: O(1) space, the "better" answer to state.

4. practice TIP:
   Lead with the HashSet (fast to code, easy to explain), then say "I can drop
   to O(1) space by treating it as cycle detection" and show Floyd's. That
   progression is exactly what Google looks for.
"""
