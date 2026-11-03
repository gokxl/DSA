"""
================================================================================
PROBLEM: Task Scheduler (LeetCode 621)
Difficulty: Medium | Pattern: Greedy/Math
================================================================================

PROBLEM STATEMENT:
Given a characters array tasks, representing the tasks a CPU needs to do, 
where each letter represents a different task. Tasks could be done in any order. 
Each task is done in one unit of time. For each unit of time, the CPU could 
complete either one task or just be idle.

However, there is a non-negative integer n that represents the cooldown period 
between two same tasks (the same letter in the array), that is that there must 
be at least n units of time between any two same tasks.

Return the least number of units of times that the CPU will take to finish 
all the given tasks.

EXAMPLES:
    Input: tasks = ["A","A","A","B","B","B"], n = 2
    Output: 8
    Explanation: A -> B -> idle -> A -> B -> idle -> A -> B

    Input: tasks = ["A","A","A","B","B","B"], n = 0
    Output: 6
    Explanation: No cooldown needed, any order works.

    Input: tasks = ["A","A","A","A","A","A","B","C","D","E","F","G"], n = 2
    Output: 16
    Explanation: A -> B -> C -> A -> D -> E -> A -> F -> G -> A -> idle -> idle -> A -> idle -> idle -> A

CONSTRAINTS:
- 1 <= tasks.length <= 10^4
- tasks[i] is an uppercase English letter
- n is in the range [0, 100]

================================================================================
"""
from typing import List
from collections import Counter
import heapq


# ============================================================================
# SOLUTION 1: Math Formula (Optimal)
# ============================================================================
def leastInterval(tasks: List[str], n: int) -> int:
    """
    Key insight: Most frequent task determines minimum time.
    
    If max_freq task appears f times, need at least (f-1) * (n+1) + count_max slots.
    
    Time: O(n) where n = number of tasks
    Space: O(1) - at most 26 letters
    """
    freq = Counter(tasks)
    max_freq = max(freq.values())
    
    # Count how many tasks have max frequency
    count_max = sum(1 for f in freq.values() if f == max_freq)
    
    # Calculate using formula
    # (max_freq - 1) cycles of (n + 1) slots, plus count_max at the end
    result = (max_freq - 1) * (n + 1) + count_max
    
    # Can't be less than total number of tasks
    return max(result, len(tasks))


# ============================================================================
# SOLUTION 2: Greedy with Max Heap
# ============================================================================
def leastInterval_heap(tasks: List[str], n: int) -> int:
    """
    Greedy: Always pick the task with highest remaining frequency.
    Use max heap + queue for cooldown.
    
    Time: O(total_time)
    Space: O(26) = O(1)
    """
    from collections import deque
    
    freq = Counter(tasks)
    max_heap = [-f for f in freq.values()]  # Max heap (negate for min heap)
    heapq.heapify(max_heap)
    
    time = 0
    queue = deque()  # (available_time, remaining_count)
    
    while max_heap or queue:
        time += 1
        
        if max_heap:
            count = heapq.heappop(max_heap) + 1  # Decrement (add 1 since negative)
            if count != 0:  # Still has remaining tasks
                queue.append((time + n, count))
        
        # Move cooled-down tasks back to heap
        if queue and queue[0][0] == time:
            heapq.heappush(max_heap, queue.popleft()[1])
    
    return time


# ============================================================================
# SOLUTION 3: Round Robin Simulation
# ============================================================================
def leastInterval_round_robin(tasks: List[str], n: int) -> int:
    """
    Simulate round-robin scheduling.
    
    Time: O(total_time)
    Space: O(26)
    """
    freq = Counter(tasks)
    counts = sorted(freq.values(), reverse=True)
    
    time = 0
    while counts[0] > 0:
        # Try to schedule n+1 tasks
        scheduled = 0
        for i in range(len(counts)):
            if scheduled > n:
                break
            if counts[i] > 0:
                counts[i] -= 1
                scheduled += 1
                time += 1
        
        # Re-sort after scheduling
        counts.sort(reverse=True)
        
        # Add idle time if needed (but not for last cycle)
        if counts[0] > 0 and scheduled <= n:
            time += (n + 1 - scheduled)
    
    return time


# ============================================================================
# SOLUTION 4: Frame-based approach
# ============================================================================
def leastInterval_frames(tasks: List[str], n: int) -> int:
    """
    Think in terms of frames of size (n+1).
    
    Most frequent task needs (max_freq - 1) frames + last row.
    
    Time: O(n)
    Space: O(1)
    """
    freq = Counter(tasks)
    max_freq = max(freq.values())
    count_max = list(freq.values()).count(max_freq)
    
    # Visualize as grid:
    # Frame 1: [A, _, _, _]  (n+1 slots)
    # Frame 2: [A, _, _, _]
    # ...
    # Last row: [A, B, ...]  (count_max tasks)
    
    frame_count = max_freq - 1
    frame_size = n + 1
    last_row = count_max
    
    min_time = frame_count * frame_size + last_row
    
    # Total tasks might exceed this if we have many different tasks
    return max(min_time, len(tasks))


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Standard case
    tasks1 = ["A", "A", "A", "B", "B", "B"]
    n1 = 2
    print(f"tasks = {tasks1}, n = {n1}")
    print(f"Math: {leastInterval(tasks1, n1)}")
    print(f"Heap: {leastInterval_heap(tasks1, n1)}")
    # Expected: 8 (A -> B -> idle -> A -> B -> idle -> A -> B)
    print()
    
    # Test Case 2: No cooldown
    tasks2 = ["A", "A", "A", "B", "B", "B"]
    n2 = 0
    print(f"tasks = {tasks2}, n = {n2}")
    print(f"Result: {leastInterval(tasks2, n2)}")
    # Expected: 6
    print()
    
    # Test Case 3: Many different tasks
    tasks3 = ["A", "A", "A", "A", "A", "A", "B", "C", "D", "E", "F", "G"]
    n3 = 2
    print(f"tasks = {tasks3}, n = {n3}")
    print(f"Result: {leastInterval(tasks3, n3)}")
    # Expected: 16
    print()
    
    # Test Case 4: Single task type
    tasks4 = ["A", "A", "A", "A"]
    n4 = 3
    print(f"tasks = {tasks4}, n = {n4}")
    print(f"Result: {leastInterval(tasks4, n4)}")
    # Expected: 13 (A -> idle -> idle -> idle -> A -> ...)
    print()
    
    # Test Case 5: Many tasks, more than idle needed
    tasks5 = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]
    n5 = 2
    print(f"tasks = {tasks5}, n = {n5}")
    print(f"Result: {leastInterval_frames(tasks5, n5)}")
    # Expected: 12 (no idle needed)


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. THE MATH FORMULA:
   
   result = (max_freq - 1) * (n + 1) + count_max
   
   Visualize as a grid:
   [A][B][C][ ]    <- n+1 slots per row
   [A][B][C][ ]
   [A][B]          <- last row: count_max elements
   
   Total = (max_freq - 1) rows × (n+1) slots + count_max

2. WHY max(result, len(tasks))?
   
   If we have many different tasks, they might fill all idle slots.
   Then answer is just total number of tasks.
   
   Example: tasks = [A,B,C,D,E,F], n = 1
   A-B-C-D-E-F (no idle needed)

3. GREEDY WITH HEAP:
   
   Always schedule the most frequent remaining task.
   This minimizes idle time.
   
   Use max heap + cooldown queue.

4. COOLDOWN MANAGEMENT:
   
   After task A, it can't be scheduled for n time units.
   Track "available time" for each task type.

5. FRAME-BASED THINKING:
   
   Each frame is (n+1) slots.
   Most frequent task defines number of frames.
   Other tasks fill the gaps.

6. EDGE CASES:
   
   - n = 0: Answer is len(tasks)
   - Single task type: (freq - 1) * (n + 1) + 1
   - Many task types: Answer is len(tasks) (no idle)

7. TIME COMPLEXITY:
   
   Math formula: O(n) - just count frequencies
   Heap: O(total_time) which could be larger

8. COMMON MISTAKES:
   
   ❌ Forgetting max(result, len(tasks))
   ❌ Wrong frame size (n+1, not n)
   ❌ Off-by-one in last row count

9. RELATED PROBLEMS:
   
   - Reorganize String (LC 767)
   - Rearrange String k Distance Apart (LC 358)

10. practice TIP:
    
    "The key insight is that the most frequent task determines
    the minimum time. I visualize it as a grid:
    
    - (max_freq - 1) rows of (n+1) slots each
    - Last row has count_max tasks (those with max frequency)
    
    Formula: (max_freq - 1) * (n + 1) + count_max
    
    But if we have many different tasks, they fill all idle slots,
    so answer is max of formula and len(tasks).
    
    Time: O(n), Space: O(1)."
    
    Draw the grid visualization!

================================================================================
"""
