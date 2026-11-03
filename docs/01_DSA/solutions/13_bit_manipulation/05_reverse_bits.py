"""
================================================================================
PROBLEM: Reverse Bits (LeetCode 190)
Difficulty: Easy | Pattern: Bit Manipulation
================================================================================

PROBLEM STATEMENT:
Reverse the bits of a given 32-bit unsigned integer.

EXAMPLES:
    Input:  n = 00000010100101000001111010011100  (43261596)
    Output:    00111001011110000010100101000000  (964176192)

    Input:  n = 11111111111111111111111111111101  (4294967293)
    Output:    10111111111111111111111111111111  (3221225471)

CONSTRAINTS:
- The input is a 32-bit unsigned integer.

FOLLOW-UP: If this function is called many times, how would you optimize it?
(Answer: cache results in byte-sized chunks.)

================================================================================
"""


# ============================================================================
# SOLUTION 1: Bit-by-Bit (Clear and Standard)
# ============================================================================
def reverseBits(n: int) -> int:
    """
    Pull the lowest bit of n, push it onto the left side of result, repeat 32x.

        result = (result << 1) | (n & 1)
        n >>= 1

    Time:  O(32) = O(1)
    Space: O(1)
    """
    result = 0
    for _ in range(32):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result


# ============================================================================
# SOLUTION 2: Divide and Conquer (Swap Halves)
# ============================================================================
def reverseBits_mask(n: int) -> int:
    """
    Swap adjacent groups of bits: 16s, then 8s, 4s, 2s, 1s. Each step is O(1),
    giving log(32) = 5 operations total -- great when called repeatedly.

    Time:  O(1)
    Space: O(1)
    """
    n = ((n >> 16) | (n << 16)) & 0xFFFFFFFF
    n = ((n & 0xFF00FF00) >> 8) | ((n & 0x00FF00FF) << 8)
    n = ((n & 0xF0F0F0F0) >> 4) | ((n & 0x0F0F0F0F) << 4)
    n = ((n & 0xCCCCCCCC) >> 2) | ((n & 0x33333333) << 2)
    n = ((n & 0xAAAAAAAA) >> 1) | ((n & 0x55555555) << 1)
    return n & 0xFFFFFFFF


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    print(f"43261596   -> {reverseBits(43261596)}")    # 964176192
    print(f"4294967293 -> {reverseBits(4294967293)}")  # 3221225471
    print(f"1          -> {reverseBits(1)}")           # 2147483648
    assert reverseBits(43261596) == reverseBits_mask(43261596)


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. CORE LOOP IDIOM (memorize this):
       result = (result << 1) | (n & 1)
   Shift the accumulator left to make room, OR in n's current lowest bit.

2. THE FOLLOW-UP ANSWER (optimization for many calls):
   Precompute the reversal of every 8-bit byte into a lookup table (256 entries).
   Then reverse a 32-bit number by reversing its 4 bytes and swapping their
   positions -- turning 32 iterations into 4 table lookups.

3. THE 0xFFFFFFFF MASK:
   Python ints are arbitrary precision, so mask with 0xFFFFFFFF to stay within
   32 bits. This is a common gotcha that does not exist in C/Java.

4. practice TIP:
   The bit-by-bit version is enough to pass. Mention the byte-cache follow-up
   to show you understand amortized optimization.
"""
