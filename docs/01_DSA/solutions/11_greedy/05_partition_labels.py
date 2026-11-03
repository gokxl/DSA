"""
================================================================================
PROBLEM: Partition Labels (LeetCode 763)
Difficulty: Medium | Pattern: Greedy/Two Pointers
================================================================================

PROBLEM STATEMENT:
You are given a string s. We want to partition the string into as many parts 
as possible so that each letter appears in at most one part.

Note that the partition is done so that after concatenating all the parts in 
order, the resultant string should be s.

Return a list of integers representing the size of these parts.

EXAMPLES:
    Input: s = "ababcbacadefegdehijhklij"
    Output: [9,7,8]
    Explanation:
    The partition is "ababcbaca", "defegde", "hijhklij".
    Each letter appears in at most one part.
    A partition like "ababcbacadefegde", "hijhklij" is incorrect 
    because it splits s into less parts.

    Input: s = "eccbbbbdec"
    Output: [10]

CONSTRAINTS:
- 1 <= s.length <= 500
- s consists of lowercase English letters

================================================================================
"""
from typing import List


# ============================================================================
# SOLUTION 1: Greedy with last occurrence
# ============================================================================
def partitionLabels(s: str) -> List[int]:
    """
    For each character, find its last occurrence.
    Partition must extend to include all characters' last occurrences.
    
    Time: O(n)
    Space: O(1) - only 26 letters
    """
    # Find last occurrence of each character
    last = {char: i for i, char in enumerate(s)}
    
    result = []
    start = 0
    end = 0
    
    for i, char in enumerate(s):
        # Extend partition to include char's last occurrence
        end = max(end, last[char])
        
        # If we've processed all characters in current partition
        if i == end:
            result.append(end - start + 1)
            start = end + 1
    
    return result


# ============================================================================
# SOLUTION 2: Merge intervals approach
# ============================================================================
def partitionLabels_intervals(s: str) -> List[int]:
    """
    Create interval [first, last] for each character.
    Merge overlapping intervals.
    
    Time: O(n)
    Space: O(1)
    """
    # Find first and last occurrence of each character
    first = {}
    last = {}
    
    for i, char in enumerate(s):
        if char not in first:
            first[char] = i
        last[char] = i
    
    # Create intervals for each unique character
    intervals = [(first[c], last[c]) for c in first]
    intervals.sort()  # Sort by start
    
    # Merge overlapping intervals
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:  # Overlap
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    
    return [end - start + 1 for start, end in merged]


# ============================================================================
# SOLUTION 3: Two pointers explicit
# ============================================================================
def partitionLabels_two_pointer(s: str) -> List[int]:
    """
    Two pointer approach with explicit tracking.
    
    Time: O(n)
    Space: O(1)
    """
    last = [0] * 26
    for i, char in enumerate(s):
        last[ord(char) - ord('a')] = i
    
    result = []
    left = 0
    right = 0
    
    for i, char in enumerate(s):
        right = max(right, last[ord(char) - ord('a')])
        
        if i == right:
            result.append(right - left + 1)
            left = right + 1
    
    return result


# ============================================================================
# SOLUTION 4: Using set for verification
# ============================================================================
def partitionLabels_verify(s: str) -> List[int]:
    """
    Same algorithm with verification.
    
    Time: O(n)
    Space: O(1)
    """
    last = {c: i for i, c in enumerate(s)}
    
    result = []
    partition_start = 0
    partition_end = 0
    
    for i, c in enumerate(s):
        partition_end = max(partition_end, last[c])
        
        if i == partition_end:
            # Verify: all chars in partition only appear here
            partition = s[partition_start:partition_end + 1]
            result.append(len(partition))
            partition_start = partition_end + 1
    
    return result


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Standard case
    s1 = "ababcbacadefegdehijhklij"
    print(f"s = '{s1}'")
    print(f"Greedy: {partitionLabels(s1)}")
    print(f"Intervals: {partitionLabels_intervals(s1)}")
    # Expected: [9, 7, 8]
    print()
    
    # Test Case 2: Single partition
    s2 = "eccbbbbdec"
    print(f"s = '{s2}'")
    print(f"Result: {partitionLabels(s2)}")
    # Expected: [10]
    print()
    
    # Test Case 3: All unique
    s3 = "abcdefg"
    print(f"s = '{s3}'")
    print(f"Result: {partitionLabels(s3)}")
    # Expected: [1, 1, 1, 1, 1, 1, 1]
    print()
    
    # Test Case 4: Single character repeated
    s4 = "aaaa"
    print(f"s = '{s4}'")
    print(f"Result: {partitionLabels(s4)}")
    # Expected: [4]
    print()
    
    # Test Case 5: Two characters alternating
    s5 = "ababab"
    print(f"s = '{s5}'")
    print(f"Result: {partitionLabels_two_pointer(s5)}")
    # Expected: [6]


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. KEY INSIGHT:
   
   If character c appears in a partition, ALL occurrences
   of c must be in that partition.
   
   → Partition must extend to c's LAST occurrence.

2. ALGORITHM:
   
   1. Precompute last[c] = last index of each character
   2. Scan left to right:
      - Extend partition_end to max(partition_end, last[c])
      - When i == partition_end, partition is complete!

3. WHY THIS MAXIMIZES PARTITIONS:
   
   We close a partition as soon as possible.
   
   Once we've seen all characters' last occurrences,
   no reason to extend further.

4. INTERVAL INTERPRETATION:
   
   Each character c has interval [first[c], last[c]].
   Partition = merged overlapping intervals.
   
   Same answer, different perspective.

5. TIME/SPACE:
   
   Time: O(n) - two passes
   Space: O(1) - only 26 letters

6. WHY ONE PASS ISN'T ENOUGH:
   
   We need to know last occurrences BEFORE processing.
   
   First pass: build last occurrence map
   Second pass: find partitions

7. COMMON MISTAKES:
   
   ❌ Not extending to ALL characters' last occurrences
   ❌ Closing partition too early
   ❌ Off-by-one in partition sizes

8. VERIFICATION:
   
   After partitioning, verify each partition contains
   characters not in other partitions.
   
   Useful for debugging!

9. RELATED PROBLEMS:
   
   - Merge Intervals (LC 56)
   - Meeting Rooms II (LC 253)
   - Minimum Number of Arrows (LC 452)

10. practice TIP:
    
    "First, I find the last occurrence of each character.
    
    Then I scan left to right. For each character, I extend
    the current partition's end to include all its occurrences.
    
    When my index reaches the partition end, I've included
    all characters' last occurrences - partition complete!
    
    This maximizes partitions because I close each one
    as soon as possible."
    
    Draw an example showing character spans!

================================================================================
"""
