"""
================================================================================
PROBLEM: Non-overlapping Intervals (LeetCode 435)
Difficulty: Medium | Pattern: Greedy (Interval Scheduling)
================================================================================

PROBLEM STATEMENT:
Given an array of intervals intervals where intervals[i] = [starti, endi], 
return the minimum number of intervals you need to remove to make the rest 
of the intervals non-overlapping.

EXAMPLES:
    Input: intervals = [[1,2],[2,3],[3,4],[1,3]]
    Output: 1
    Explanation: [1,3] can be removed and the rest are non-overlapping.

    Input: intervals = [[1,2],[1,2],[1,2]]
    Output: 2
    Explanation: You need to remove two [1,2] to make non-overlapping.

    Input: intervals = [[1,2],[2,3]]
    Output: 0
    Explanation: Already non-overlapping (touching is okay).

CONSTRAINTS:
- 1 <= intervals.length <= 10^5
- intervals[i].length == 2
- -5 * 10^4 <= starti < endi <= 5 * 10^4

================================================================================
"""
from typing import List


# ============================================================================
# SOLUTION 1: Greedy (Sort by end time)
# ============================================================================
def eraseOverlapIntervals(intervals: List[List[int]]) -> int:
    """
    Classic interval scheduling: Sort by end time.
    Always keep the interval that ends earliest.
    
    Time: O(n log n)
    Space: O(1) or O(n) for sorting
    """
    if not intervals:
        return 0
    
    # Sort by end time
    intervals.sort(key=lambda x: x[1])
    
    count = 0  # Number of removals
    prev_end = intervals[0][1]
    
    for i in range(1, len(intervals)):
        if intervals[i][0] < prev_end:  # Overlap!
            count += 1
            # Keep the one with earlier end (don't update prev_end)
        else:
            prev_end = intervals[i][1]
    
    return count


# ============================================================================
# SOLUTION 2: Count non-overlapping (then subtract)
# ============================================================================
def eraseOverlapIntervals_count_keep(intervals: List[List[int]]) -> int:
    """
    Count max non-overlapping intervals, subtract from total.
    
    Time: O(n log n)
    Space: O(1)
    """
    if not intervals:
        return 0
    
    intervals.sort(key=lambda x: x[1])
    
    keep = 1  # Keep first interval
    prev_end = intervals[0][1]
    
    for i in range(1, len(intervals)):
        if intervals[i][0] >= prev_end:  # No overlap
            keep += 1
            prev_end = intervals[i][1]
    
    return len(intervals) - keep


# ============================================================================
# SOLUTION 3: Sort by start time
# ============================================================================
def eraseOverlapIntervals_by_start(intervals: List[List[int]]) -> int:
    """
    Sort by start time, track what to keep.
    When overlap, keep the one ending earlier.
    
    Time: O(n log n)
    Space: O(1)
    """
    if not intervals:
        return 0
    
    intervals.sort()  # Sort by start
    
    count = 0
    prev_end = intervals[0][1]
    
    for i in range(1, len(intervals)):
        if intervals[i][0] < prev_end:  # Overlap
            count += 1
            # Keep the one with earlier end
            prev_end = min(prev_end, intervals[i][1])
        else:
            prev_end = intervals[i][1]
    
    return count


# ============================================================================
# SOLUTION 4: DP (Less efficient, for comparison)
# ============================================================================
def eraseOverlapIntervals_dp(intervals: List[List[int]]) -> int:
    """
    DP: dp[i] = max non-overlapping intervals ending at i
    Similar to LIS.
    
    Time: O(n²)
    Space: O(n)
    """
    if not intervals:
        return 0
    
    intervals.sort()
    n = len(intervals)
    
    # dp[i] = max non-overlapping ending at i
    dp = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if intervals[j][1] <= intervals[i][0]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    return n - max(dp)


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Remove one
    intervals1 = [[1, 2], [2, 3], [3, 4], [1, 3]]
    print(f"intervals = {intervals1}")
    print(f"Sort by end: {eraseOverlapIntervals(intervals1)}")
    print(f"Count keep: {eraseOverlapIntervals_count_keep(intervals1)}")
    # Expected: 1
    print()
    
    # Test Case 2: Remove two
    intervals2 = [[1, 2], [1, 2], [1, 2]]
    print(f"intervals = {intervals2}")
    print(f"Result: {eraseOverlapIntervals(intervals2)}")
    # Expected: 2
    print()
    
    # Test Case 3: No removal needed
    intervals3 = [[1, 2], [2, 3]]
    print(f"intervals = {intervals3}")
    print(f"Result: {eraseOverlapIntervals(intervals3)}")
    # Expected: 0 (touching is not overlapping)
    print()
    
    # Test Case 4: Nested intervals
    intervals4 = [[1, 100], [2, 3], [3, 4], [4, 5]]
    print(f"intervals = {intervals4}")
    print(f"Result: {eraseOverlapIntervals_by_start(intervals4)}")
    # Expected: 1 (remove [1,100])
    print()
    
    # Test Case 5: All overlapping
    intervals5 = [[1, 10], [2, 9], [3, 8], [4, 7]]
    print(f"intervals = {intervals5}")
    print(f"Result: {eraseOverlapIntervals(intervals5)}")
    # Expected: 3 (keep only the smallest one)


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. INTERVAL SCHEDULING MAXIMIZATION:
   
   This is the classic "Activity Selection Problem".
   
   Goal: Keep maximum non-overlapping intervals.
   Remove = Total - Keep

2. WHY SORT BY END TIME?
   
   Earliest finishing interval leaves most room for others.
   
   Greedy choice: Always pick interval that ends earliest
   among non-conflicting options.

3. TOUCHING IS NOT OVERLAPPING:
   
   [1,2] and [2,3] do NOT overlap!
   
   Check: intervals[i][0] < prev_end (strict <, not <=)

4. SORT BY START VS END:
   
   Sort by end: Simpler, just check if current starts before prev ends.
   Sort by start: When overlap, keep the one ending earlier.
   
   Both work, end-time sorting is cleaner.

5. GREEDY PROOF:
   
   Suppose earliest-end isn't optimal.
   Swap it with the "optimal" first choice.
   The new solution has same or more room.
   Contradiction!

6. RELATED PROBLEMS:
   
   - Merge Intervals (LC 56)
   - Meeting Rooms (LC 252)
   - Meeting Rooms II (LC 253)
   - Minimum Arrows to Burst Balloons (LC 452)

7. PATTERN: INTERVAL PROBLEMS:
   
   1. Sort by end time: Max non-overlapping
   2. Sort by start time: Merge intervals
   3. Two pointers: Intersection of intervals

8. COMMON MISTAKES:
   
   ❌ Sorting by start when end is better
   ❌ Using <= instead of < for overlap
   ❌ Counting removals wrong

9. TIME COMPLEXITY:
   
   Greedy: O(n log n) for sort
   DP: O(n²) - much slower!

10. practice TIP:
    
    "This is classic interval scheduling. I sort by end time
    because earliest-finishing interval leaves most room.
    
    For each interval, if it overlaps with previous kept one,
    I remove it (don't update prev_end). Otherwise I keep it.
    
    Touching intervals ([1,2], [2,3]) don't overlap!
    
    Time: O(n log n), dominated by sorting."
    
    Mention this is the Activity Selection Problem!

================================================================================
"""
