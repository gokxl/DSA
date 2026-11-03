"""
================================================================================
PROBLEM: Task Scheduler (LeetCode 621)
Difficulty: Medium | Pattern: Heap + Greedy
================================================================================

PROBLEM STATEMENT:
Given a characters array tasks, representing the tasks a CPU needs to do, where 
each letter represents a different task. Tasks could be done in any order. Each 
task is done in one unit of time. For each unit of time, the CPU could complete 
either one task or just be idle.

However, there is a non-negative integer n that represents the cooldown period 
between two same tasks (same letter), meaning if you've just completed task 'A', 
you must wait n units before you can do another 'A'.

Return the least number of units of times that the CPU will take to finish all 
the given tasks.

EXAMPLES:
    Input: tasks = ["A","A","A","B","B","B"], n = 2
    Output: 8
    Explanation: A -> B -> idle -> A -> B -> idle -> A -> B
    
    Input: tasks = ["A","A","A","B","B","B"], n = 0
    Output: 6
    Explanation: No cooldown, just do all tasks: A B A B A B
    
    Input: tasks = ["A","A","A","A","A","A","B","C","D","E","F","G"], n = 2
    Output: 16
    Explanation: One possible solution:
    A -> B -> C -> A -> D -> E -> A -> F -> G -> A -> idle -> idle -> A -> idle -> idle -> A

CONSTRAINTS:
- 1 <= tasks.length <= 10^4
- tasks[i] is an uppercase English letter
- 0 <= n <= 100

================================================================================
"""
from typing import List
from collections import Counter
import heapq


# ============================================================================
# SOLUTION 1: Math/Greedy (Optimal)
# ============================================================================
def leastInterval_math(tasks: List[str], n: int) -> int:
    """
    Mathematical approach based on most frequent task.
    
    The key insight: The most frequent task determines minimum time.
    
    If max frequency task appears f times:
    - Need (f-1) gaps of length (n+1) between them
    - Plus 1 for the last occurrence
    - Minimum: (f-1) * (n+1) + count_of_max_freq_tasks
    
    Time: O(n)
    Space: O(1) - only 26 letters
    """
    count = Counter(tasks)
    max_freq = max(count.values())
    
    # Count tasks with max frequency
    max_count = sum(1 for freq in count.values() if freq == max_freq)
    
    # Formula: (max_freq - 1) * (n + 1) + max_count
    # But result can't be less than total tasks
    result = (max_freq - 1) * (n + 1) + max_count
    
    return max(result, len(tasks))


# ============================================================================
# SOLUTION 2: Max-Heap Simulation
# ============================================================================
def leastInterval_heap(tasks: List[str], n: int) -> int:
    """
    Simulate scheduling using max-heap.
    
    Greedy: Always pick task with highest remaining count.
    Use cooldown queue for tasks that can't be used yet.
    
    Time: O(total_time * log 26) = O(total_time)
    Space: O(26) = O(1)
    """
    count = Counter(tasks)
    
    # Max-heap (negate counts)
    max_heap = [-cnt for cnt in count.values()]
    heapq.heapify(max_heap)
    
    time = 0
    cooldown = []  # (available_time, remaining_count)
    
    while max_heap or cooldown:
        time += 1
        
        # Move tasks from cooldown to heap if ready
        while cooldown and cooldown[0][0] <= time:
            _, cnt = heapq.heappop(cooldown)
            heapq.heappush(max_heap, cnt)
        
        if max_heap:
            cnt = heapq.heappop(max_heap)
            cnt += 1  # Remember we negated, so +1 means decrement
            
            if cnt < 0:  # Still has remaining tasks
                # Use min-heap for cooldown (sorted by available_time)
                heapq.heappush(cooldown, (time + n + 1, cnt))
    
    return time


# ============================================================================
# SOLUTION 3: Heap with cleaner simulation
# ============================================================================
def leastInterval_heap_v2(tasks: List[str], n: int) -> int:
    """
    Cleaner heap simulation using time-based queue.
    
    Time: O(total_tasks * log 26)
    Space: O(26)
    """
    count = Counter(tasks)
    max_heap = [-cnt for cnt in count.values()]
    heapq.heapify(max_heap)
    
    time = 0
    queue = []  # (time_available, negative_count)
    
    while max_heap or queue:
        time += 1
        
        if max_heap:
            cnt = heapq.heappop(max_heap) + 1  # Execute task
            if cnt != 0:
                queue.append((time + n, cnt))  # Add to cooldown
        
        # Check if any task is ready
        if queue and queue[0][0] == time:
            heapq.heappush(max_heap, queue.pop(0)[1])
    
    return time


# ============================================================================
# SOLUTION 4: Round Robin Simulation
# ============================================================================
def leastInterval_round_robin(tasks: List[str], n: int) -> int:
    """
    Simulate round-robin scheduling.
    
    Fill each cycle of length n+1 with most frequent tasks.
    
    Time: O(total_time)
    Space: O(26)
    """
    count = Counter(tasks)
    counts = sorted(count.values(), reverse=True)
    
    time = 0
    while counts[0] > 0:
        # Fill one cycle of n+1 slots
        i = 0
        while i <= n:
            if counts[0] == 0:
                break  # All tasks done
            
            if i < len(counts) and counts[i] > 0:
                counts[i] -= 1  # Do task
            
            time += 1
            i += 1
        
        counts.sort(reverse=True)  # Re-sort for next cycle
    
    return time


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Standard case
    tasks1, n1 = ["A", "A", "A", "B", "B", "B"], 2
    print(f"Tasks: {tasks1}, n={n1}")
    print(f"Math: {leastInterval_math(tasks1, n1)}")
    print(f"Heap: {leastInterval_heap(tasks1, n1)}")
    # Expected: 8 (A -> B -> idle -> A -> B -> idle -> A -> B)
    print()
    
    # Test Case 2: No cooldown
    tasks2, n2 = ["A", "A", "A", "B", "B", "B"], 0
    print(f"Tasks: {tasks2}, n={n2}")
    print(f"Result: {leastInterval_math(tasks2, n2)}")
    # Expected: 6
    print()
    
    # Test Case 3: Many tasks, one dominant
    tasks3 = ["A", "A", "A", "A", "A", "A", "B", "C", "D", "E", "F", "G"]
    n3 = 2
    print(f"Tasks: {tasks3}, n={n3}")
    print(f"Result: {leastInterval_math(tasks3, n3)}")
    # Expected: 16
    print()
    
    # Test Case 4: All same task
    tasks4, n4 = ["A", "A", "A"], 2
    print(f"Tasks: {tasks4}, n={n4}")
    print(f"Result: {leastInterval_heap(tasks4, n4)}")
    # Expected: 7 (A -> idle -> idle -> A -> idle -> idle -> A)
    print()
    
    # Test Case 5: Enough variety, no idle needed
    tasks5, n5 = ["A", "B", "C", "D", "E"], 2
    print(f"Tasks: {tasks5}, n={n5}")
    print(f"Result: {leastInterval_math(tasks5, n5)}")
    # Expected: 5 (no idle needed)


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. THE MATH FORMULA:
   
   If max frequency = f, max_count = tasks with frequency f:
   
   Minimum time = max((f-1) * (n+1) + max_count, total_tasks)
   
   Visualization for n=2, f=3:
   
   A _ _ | A _ _ | A
   [slot][slot][slot]
   
   Each slot has n+1 positions.

2. WHY THE FORMULA WORKS:
   
   - Most frequent task creates (f-1) mandatory gaps
   - Each gap is n+1 slots (task + n cooldown)
   - Final group: just the tasks with max frequency
   
   If we have enough other tasks, no idle needed.

3. GREEDY HEAP APPROACH:
   
   Always schedule the task with most remaining occurrences.
   
   This minimizes idle time by spreading out frequent tasks.

4. COOLDOWN QUEUE:
   
   After executing a task:
   - Can't use it for n time units
   - Put in queue with (available_time, count)
   - Move back to heap when available

5. EDGE CASES:
   
   - n = 0: Just return len(tasks)
   - All same task: Maximum idle time
   - Many unique tasks: Might not need any idle

6. WHY MAX(result, len(tasks))?
   
   If we have enough unique tasks, no idle needed.
   Result can't be less than total tasks.
   
   Example: 100 different tasks, n=2
   → Just do all 100 tasks, no idle needed

7. COMMON MISTAKES:
   
   ❌ Forgetting to count all max-frequency tasks
   ❌ Not taking max with total tasks
   ❌ Off-by-one in slot calculation

8. RELATED PROBLEMS:
   
   - Reorganize String (LC 767)
   - Rearrange String k Distance Apart (LC 358)
   - Distant Barcodes (LC 1054)

9. TIME COMPLEXITY:
   
   Math approach: O(n) - just count frequencies
   Heap approach: O(total_time × log 26) ≈ O(total_time)
   
   Math is simpler and faster!

10. practice TIP:
    
    "The key insight is that the most frequent task determines
    the minimum time. If it appears f times, we need at least
    (f-1) gaps of cooldown.
    
    Formula: (max_freq - 1) * (n + 1) + count_of_max_freq_tasks
    
    But if we have enough variety, we might not need any idle time,
    so the answer is max(formula, total_tasks)."
    
    Walk through the visual representation!

================================================================================
"""
