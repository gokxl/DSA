"""
================================================================================
PROBLEM: Meeting Rooms II (LeetCode 253)
Difficulty: Medium | Pattern: Intervals + Heap/Sweep Line
================================================================================

PROBLEM STATEMENT:
Given an array of meeting time intervals intervals[i] = [start_i, end_i], 
find the minimum number of conference rooms required.

EXAMPLES:
    Input: intervals = [[0,30],[5,10],[15,20]]
    Output: 2
    Explanation: 
        Room 1: [0,30]
        Room 2: [5,10], then [15,20]
        At time 5, both meetings need a room.

    Input: intervals = [[7,10],[2,4]]
    Output: 1
    Explanation: No overlap, one room is enough.

    Input: intervals = [[1,5],[5,10]]
    Output: 1
    Explanation: [5,10] can use the room after [1,5] ends.

CONSTRAINTS:
- 1 <= intervals.length <= 10^4
- 0 <= start_i < end_i <= 10^6

================================================================================
"""

from typing import List
import heapq


# ============================================================================
# SOLUTION 1: Min Heap (Track ending times)
# ============================================================================
def minMeetingRooms_heap(intervals: List[List[int]]) -> int:
    """
    Sort meetings by start time.
    Use a min heap to track the end times of ongoing meetings.
    
    For each meeting:
    - If earliest ending meeting is done (end <= current start), reuse that room
    - Otherwise, need a new room
    
    The heap size at the end = number of rooms needed
    
    Time: O(n log n) - sorting and heap operations
    Space: O(n) - heap can have all meetings
    """
    if not intervals:
        return 0
    
    # Sort by start time
    intervals.sort(key=lambda x: x[0])
    
    # Min heap to track end times of ongoing meetings
    # Heap contains end times - smallest end time at top
    rooms = []
    heapq.heappush(rooms, intervals[0][1])  # First meeting's end time
    
    for start, end in intervals[1:]:
        # If earliest ending meeting is done, reuse that room
        if start >= rooms[0]:
            heapq.heappop(rooms)  # Remove the finished meeting
        
        # Add current meeting's end time (whether reusing or new room)
        heapq.heappush(rooms, end)
    
    return len(rooms)


# ============================================================================
# SOLUTION 2: Sweep Line / Chronological Ordering (Elegant!)
# ============================================================================
def minMeetingRooms(intervals: List[List[int]]) -> int:
    """
    Create events: +1 for start, -1 for end.
    Sort all events by time.
    Sweep through and track maximum concurrent meetings.
    
    Key insight: At any point in time, count of rooms = 
                 (meetings started) - (meetings ended)
    
    Time: O(n log n)
    Space: O(n)
    """
    if not intervals:
        return 0
    
    # Create events: (time, type)
    # type: +1 for start, -1 for end
    events = []
    for start, end in intervals:
        events.append((start, 1))   # Meeting starts
        events.append((end, -1))    # Meeting ends
    
    # Sort by time
    # If same time, end (-1) comes before start (+1)
    # This is because a room freed at time T can be used at time T
    events.sort(key=lambda x: (x[0], x[1]))
    
    max_rooms = 0
    current_rooms = 0
    
    for time, delta in events:
        current_rooms += delta
        max_rooms = max(max_rooms, current_rooms)
    
    return max_rooms


# ============================================================================
# SOLUTION 3: Two Sorted Arrays (Simple but clever)
# ============================================================================
def minMeetingRooms_two_arrays(intervals: List[List[int]]) -> int:
    """
    Sort start times and end times separately.
    Use two pointers to simulate the sweep line.
    
    Time: O(n log n)
    Space: O(n)
    """
    if not intervals:
        return 0
    
    starts = sorted([i[0] for i in intervals])
    ends = sorted([i[1] for i in intervals])
    
    rooms = 0
    end_ptr = 0
    
    for start in starts:
        if start < ends[end_ptr]:
            # Meeting started before any ended - need new room
            rooms += 1
        else:
            # A meeting ended, can reuse that room
            end_ptr += 1
    
    return rooms


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Overlapping meetings
    intervals1 = [[0, 30], [5, 10], [15, 20]]
    print(f"Input: {intervals1}")
    print(f"Output (Heap): {minMeetingRooms_heap(intervals1)}")
    print(f"Output (Sweep): {minMeetingRooms(intervals1)}")
    # Expected: 2
    print()
    
    # Test Case 2: No overlap
    intervals2 = [[7, 10], [2, 4]]
    print(f"Input: {intervals2}")
    print(f"Output (Heap): {minMeetingRooms_heap(intervals2)}")
    print(f"Output (Sweep): {minMeetingRooms(intervals2)}")
    # Expected: 1
    print()
    
    # Test Case 3: Back-to-back meetings
    intervals3 = [[1, 5], [5, 10]]
    print(f"Input: {intervals3}")
    print(f"Output (Heap): {minMeetingRooms_heap(intervals3)}")
    print(f"Output (Sweep): {minMeetingRooms(intervals3)}")
    # Expected: 1
    print()
    
    # Test Case 4: All overlap
    intervals4 = [[1, 5], [2, 6], [3, 7]]
    print(f"Input: {intervals4}")
    print(f"Output (Heap): {minMeetingRooms_heap(intervals4)}")
    print(f"Output (Sweep): {minMeetingRooms(intervals4)}")
    # Expected: 3
    print()
    
    # Test Case 5: Single meeting
    intervals5 = [[1, 5]]
    print(f"Input: {intervals5}")
    print(f"Output (Heap): {minMeetingRooms_heap(intervals5)}")
    print(f"Output (Sweep): {minMeetingRooms(intervals5)}")
    # Expected: 1


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. TWO MAIN APPROACHES (Know both!):

   a) MIN HEAP APPROACH:
      - Sort by start time
      - Heap tracks end times of ongoing meetings
      - If new meeting starts after earliest end → reuse room
      - Heap size = concurrent meetings = rooms needed
   
   b) SWEEP LINE APPROACH:
      - Create +1 events for starts, -1 events for ends
      - Sort all events by time
      - Track running count of rooms
      - Maximum count = answer

2. CRITICAL DETAIL: START = END TIME
   - If meeting A ends at 10 and B starts at 10, ONE room is enough
   - In sweep line: process end (-1) before start (+1) at same time
   - In heap: use >= not > when comparing

3. WHY HEAP APPROACH WORKS:
   - We only care about earliest ending meeting
   - If that meeting hasn't ended, we need a new room
   - Min heap gives O(log n) access to earliest end

4. WHY SWEEP LINE WORKS:
   - At any point: rooms = meetings_started - meetings_ended
   - Maximum of this value across all points = answer

5. WHICH TO USE IN practice?
   - Sweep line is more elegant and easier to explain
   - Heap is more intuitive ("simulate the process")
   - Know both! Interviewer might ask for alternative

6. VISUAL TIMELINE:

   Time:  0    5    10   15   20   25   30
          |----|----|----|----|----|----|
   [0,30] |================================|
   [5,10]      |=====|
   [15,20]               |=====|
   
   At t=5: 2 meetings concurrent → need 2 rooms

7. FOLLOW-UP QUESTIONS:
   Q: What if we need to return which meetings in which room?
   A: Modify heap to store (end_time, room_id), assign meetings to rooms

   Q: What if rooms have different capacities?
   A: Track room availability differently (more complex)

================================================================================
"""
