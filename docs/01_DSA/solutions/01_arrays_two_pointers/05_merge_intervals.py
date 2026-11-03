"""
================================================================================
PROBLEM: Merge Intervals (LeetCode 56)
Difficulty: Medium | Pattern: Intervals
================================================================================

PROBLEM STATEMENT:
Given an array of intervals where intervals[i] = [start_i, end_i], merge all 
overlapping intervals, and return an array of the non-overlapping intervals 
that cover all the intervals in the input.

EXAMPLES:
    Input: intervals = [[1,3],[2,6],[8,10],[15,18]]
    Output: [[1,6],[8,10],[15,18]]
    Explanation: [1,3] and [2,6] overlap, merge to [1,6]

    Input: intervals = [[1,4],[4,5]]
    Output: [[1,5]]
    Explanation: [1,4] and [4,5] touch at 4, so they are merged

    Input: intervals = [[1,4],[2,3]]
    Output: [[1,4]]
    Explanation: [2,3] is completely contained in [1,4]

CONSTRAINTS:
- 1 <= intervals.length <= 10^4
- intervals[i].length == 2
- 0 <= start_i <= end_i <= 10^4

================================================================================
"""

from typing import List


# ============================================================================
# SOLUTION: Sort + Linear Merge (Optimal)
# ============================================================================
def merge(intervals: List[List[int]]) -> List[List[int]]:
    """
    1. Sort intervals by start time
    2. For each interval, either merge with last or add new
    
    OVERLAP CONDITION: current.start <= previous.end
    
    Time: O(n log n) - dominated by sorting
    Space: O(1) or O(n) depending on sort implementation
    """
    if not intervals:
        return []
    
    # Sort by start time
    intervals.sort(key=lambda x: x[0])
    
    # Start with first interval
    merged = [intervals[0]]
    
    for start, end in intervals[1:]:
        last_end = merged[-1][1]
        
        if start <= last_end:  # Overlapping
            # Extend the last interval (use max for contained intervals)
            merged[-1][1] = max(last_end, end)
        else:
            # No overlap, add new interval
            merged.append([start, end])
    
    return merged


# ============================================================================
# ALTERNATIVE: More explicit version
# ============================================================================
def merge_verbose(intervals: List[List[int]]) -> List[List[int]]:
    """
    Same logic but more explicit for understanding.
    """
    if not intervals:
        return []
    
    intervals.sort(key=lambda x: x[0])
    
    merged = []
    current_start = intervals[0][0]
    current_end = intervals[0][1]
    
    for i in range(1, len(intervals)):
        start, end = intervals[i]
        
        if start <= current_end:
            # Overlapping - extend current interval
            current_end = max(current_end, end)
        else:
            # Not overlapping - save current, start new
            merged.append([current_start, current_end])
            current_start = start
            current_end = end
    
    # Don't forget the last interval!
    merged.append([current_start, current_end])
    
    return merged


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Standard overlapping
    intervals1 = [[1, 3], [2, 6], [8, 10], [15, 18]]
    print(f"Input: {intervals1}")
    print(f"Output: {merge(intervals1)}")
    # Expected: [[1, 6], [8, 10], [15, 18]]
    print()
    
    # Test Case 2: Touching intervals
    intervals2 = [[1, 4], [4, 5]]
    print(f"Input: {intervals2}")
    print(f"Output: {merge(intervals2)}")
    # Expected: [[1, 5]]
    print()
    
    # Test Case 3: Contained interval
    intervals3 = [[1, 4], [2, 3]]
    print(f"Input: {intervals3}")
    print(f"Output: {merge(intervals3)}")
    # Expected: [[1, 4]]
    print()
    
    # Test Case 4: No overlap
    intervals4 = [[1, 2], [4, 5], [7, 8]]
    print(f"Input: {intervals4}")
    print(f"Output: {merge(intervals4)}")
    # Expected: [[1, 2], [4, 5], [7, 8]]
    print()
    
    # Test Case 5: Single interval
    intervals5 = [[1, 5]]
    print(f"Input: {intervals5}")
    print(f"Output: {merge(intervals5)}")
    # Expected: [[1, 5]]
    print()
    
    # Test Case 6: All merge into one
    intervals6 = [[1, 4], [0, 4]]
    print(f"Input: {intervals6}")
    print(f"Output: {merge(intervals6)}")
    # Expected: [[0, 4]]
    print()
    
    # Test Case 7: Unsorted input
    intervals7 = [[1, 4], [0, 0]]
    print(f"Input: {intervals7}")
    print(f"Output: {merge(intervals7)}")
    # Expected: [[0, 0], [1, 4]]


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. ALWAYS SORT FIRST FOR INTERVAL PROBLEMS
   - Sort by start time
   - This ensures we process intervals in order
   - Overlapping intervals will be adjacent after sorting

2. OVERLAP CONDITIONS (Critical to remember):
   - Overlapping: current.start <= previous.end
   - NOT overlapping: current.start > previous.end
   - Note: [1,4] and [4,5] are considered overlapping (touching)

3. THREE CASES TO HANDLE:
   a) No overlap: add new interval
   b) Overlap: extend end
   c) Contained ([1,5] and [2,3]): use max(end) - same as overlap case

4. COMMON EDGE CASES:
   - Single interval
   - All intervals merge to one
   - No intervals overlap
   - Intervals completely contained in another
   - Unsorted input (that's why we sort first!)

5. WHY max(last_end, end)?
   - Handles the contained case: [1,5] and [2,3] should give [1,5]
   - Without max, we'd incorrectly get [1,3]

6. RELATED PROBLEMS (Google loves intervals!):
   - Insert Interval (LC 57)
   - Meeting Rooms (LC 252)
   - Meeting Rooms II (LC 253)
   - Non-overlapping Intervals (LC 435)
   - Interval List Intersections (LC 986)

================================================================================
VISUAL REPRESENTATION:
================================================================================

Before sorting:  [[1,3], [2,6], [8,10], [15,18]]

Timeline:
1---3
  2-------6
           8--10
                    15--18

After merge: [[1,6], [8,10], [15,18]]

1---------6
           8--10
                    15--18

================================================================================
practice WALKTHROUGH:
================================================================================

"For interval problems, my first instinct is to sort - this usually helps.

Let me sort by start time. Now I can iterate through and for each interval,
check if it overlaps with the previous one.

Overlap condition: if current start <= previous end, they overlap.

If overlap: extend the end to max(previous_end, current_end)
If no overlap: add as new interval

The max is important to handle contained intervals like [1,5] containing [2,3]."

================================================================================
"""
