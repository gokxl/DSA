"""
================================================================================
PROBLEM: Linked List Cycle (LeetCode 141) + Cycle II (LeetCode 142)
Difficulty: Easy/Medium | Pattern: Fast & Slow Pointers
================================================================================

PROBLEM STATEMENT (LC 141):
Given head, the head of a linked list, determine if the linked list has a cycle.

There is a cycle if there is some node that can be reached again by continuously 
following the next pointer.

Return true if there is a cycle, false otherwise.

PROBLEM STATEMENT (LC 142):
Given the head of a linked list, return the node where the cycle begins. 
If there is no cycle, return null.

EXAMPLES:
    Input: head = [3,2,0,-4], pos = 1 (tail connects to index 1)
    Output (LC 141): true
    Output (LC 142): node with value 2

    Input: head = [1,2], pos = 0 (tail connects to index 0)
    Output (LC 141): true
    Output (LC 142): node with value 1

    Input: head = [1], pos = -1 (no cycle)
    Output (LC 141): false
    Output (LC 142): null

CONSTRAINTS:
- The number of nodes in the list is in range [0, 10^4]
- -10^5 <= Node.val <= 10^5
- pos is -1 or a valid index in the linked-list

================================================================================
"""
from typing import Optional


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# ============================================================================
# SOLUTION 1: Floyd's Cycle Detection (Optimal)
# ============================================================================
def hasCycle(head: Optional[ListNode]) -> bool:
    """
    Floyd's Tortoise and Hare algorithm.
    
    If there's a cycle, fast will eventually meet slow.
    If no cycle, fast will reach end.
    
    Time: O(n)
    Space: O(1)
    """
    if not head or not head.next:
        return False
    
    slow = head
    fast = head
    
    while fast and fast.next:
        slow = slow.next        # Move 1 step
        fast = fast.next.next   # Move 2 steps
        
        if slow == fast:        # They meet = cycle exists
            return True
    
    return False


# ============================================================================
# SOLUTION 2: Find Cycle Start (LC 142)
# ============================================================================
def detectCycle(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Two-phase Floyd's algorithm:
    Phase 1: Detect if cycle exists (fast meets slow)
    Phase 2: Find cycle start (reset slow to head, move both by 1)
    
    Time: O(n)
    Space: O(1)
    """
    if not head or not head.next:
        return None
    
    # Phase 1: Detect cycle
    slow = head
    fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        
        if slow == fast:
            # Cycle detected! Move to phase 2
            break
    else:
        # No cycle (fast reached end)
        return None
    
    # Phase 2: Find cycle start
    # Reset slow to head, keep fast at meeting point
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next
    
    return slow  # This is the cycle start


# ============================================================================
# SOLUTION 3: Using HashSet (Simple but O(n) space)
# ============================================================================
def hasCycle_hashset(head: Optional[ListNode]) -> bool:
    """
    Store visited nodes in a set.
    If we see a node again, there's a cycle.
    
    Time: O(n)
    Space: O(n)
    """
    visited = set()
    curr = head
    
    while curr:
        if curr in visited:
            return True
        visited.add(curr)
        curr = curr.next
    
    return False


def detectCycle_hashset(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Return the first node we visit twice.
    
    Time: O(n)
    Space: O(n)
    """
    visited = set()
    curr = head
    
    while curr:
        if curr in visited:
            return curr
        visited.add(curr)
        curr = curr.next
    
    return None


# ============================================================================
# HELPER FUNCTIONS FOR TESTING
# ============================================================================
def create_linked_list_with_cycle(values, pos):
    """Create linked list with cycle at position pos (-1 for no cycle)"""
    if not values:
        return None
    
    head = ListNode(values[0])
    curr = head
    cycle_node = None
    
    for i, val in enumerate(values[1:], 1):
        curr.next = ListNode(val)
        curr = curr.next
        if i == pos:
            cycle_node = curr
    
    if pos == 0:
        curr.next = head
    elif cycle_node:
        curr.next = cycle_node
    
    return head


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Cycle at position 1
    head1 = create_linked_list_with_cycle([3, 2, 0, -4], 1)
    print(f"List: [3,2,0,-4] with cycle at pos 1")
    print(f"Has Cycle (Floyd): {hasCycle(head1)}")
    print(f"Has Cycle (HashSet): {hasCycle_hashset(head1)}")
    cycle_start = detectCycle(head1)
    print(f"Cycle starts at: {cycle_start.val if cycle_start else None}")
    # Expected: True, value 2
    print()
    
    # Test Case 2: Cycle at position 0 (tail → head)
    head2 = create_linked_list_with_cycle([1, 2], 0)
    print(f"List: [1,2] with cycle at pos 0")
    print(f"Has Cycle: {hasCycle(head2)}")
    cycle_start = detectCycle(head2)
    print(f"Cycle starts at: {cycle_start.val if cycle_start else None}")
    # Expected: True, value 1
    print()
    
    # Test Case 3: No cycle
    head3 = create_linked_list_with_cycle([1], -1)
    print(f"List: [1] with no cycle")
    print(f"Has Cycle: {hasCycle(head3)}")
    cycle_start = detectCycle(head3)
    print(f"Cycle starts at: {cycle_start.val if cycle_start else None}")
    # Expected: False, None
    print()
    
    # Test Case 4: Empty list
    head4 = None
    print(f"Empty list")
    print(f"Has Cycle: {hasCycle(head4)}")
    # Expected: False


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. FLOYD'S ALGORITHM - WHY IT WORKS:
   
   If there's a cycle:
   - Both pointers enter cycle eventually
   - Fast gains 1 step per iteration on slow
   - They MUST meet within cycle
   
   If no cycle:
   - Fast reaches end → no cycle

2. WHY FAST MOVES 2, SLOW MOVES 1:
   
   Relative speed = 2 - 1 = 1
   Fast gains 1 node per iteration.
   
   If cycle length = k, they meet in ≤ k iterations.
   
   Other speeds work too (3 and 1), but 2 and 1 is simplest.

3. FINDING CYCLE START - THE MATH:
   
   Let:
   - L = distance from head to cycle start
   - C = cycle length
   - K = distance from cycle start to meeting point
   
   When they meet:
   - Slow traveled: L + K
   - Fast traveled: L + K + nC (some complete cycles)
   
   Since fast = 2 × slow:
   2(L + K) = L + K + nC
   L + K = nC
   L = nC - K
   
   So: L = (n-1)C + (C - K)
   
   This means: Distance from HEAD to cycle start (L)
              = Distance from MEETING POINT to cycle start!
   
   That's why reset slow to head, move both by 1 until they meet!

4. HASHSET APPROACH:
   
   Simpler to understand:
   - Store each visited node
   - If we see it again → cycle, and that node is start
   
   Trade-off: O(n) space vs O(1)

5. EDGE CASES:
   
   - Empty list (head = None)
   - Single node without cycle
   - Single node with self-loop
   - Two nodes with cycle

6. COMMON MISTAKES:
   
   ❌ Using while fast.next (misses fast = None case)
   ✓ Use while fast and fast.next
   
   ❌ Comparing values instead of node references
   ✓ Compare slow == fast (object identity)

7. FOLLOW-UP QUESTIONS:
   
   Q: What if we need cycle length?
   A: After detecting cycle, keep moving slow and count:
      slow = slow.next
      count += 1
      until slow == fast again

8. RELATED PROBLEMS:
   
   - Happy Number (LC 202) - same Floyd's technique!
   - Find Duplicate Number (LC 287)
   - Linked List Cycle II (LC 142)

9. HAPPY NUMBER INSIGHT:
   
   Sequence: n → sum of squared digits
   Eventually cycles OR reaches 1.
   
   Treat it as linked list cycle detection!

10. practice TIP:
    
    If asked "how does it work?", explain the math:
    "When they meet, the distance from head to cycle start
    equals the distance from meeting point to cycle start
    (going around the cycle). So reset one pointer to head
    and move both by 1 until they meet at cycle start."

================================================================================
"""
