"""
================================================================================
PROBLEM: Reorder List (LeetCode 143)
Difficulty: Medium | Pattern: Linked List
================================================================================

PROBLEM STATEMENT:
You are given the head of a singly linked-list. The list can be represented as:
    L0 → L1 → … → Ln-1 → Ln

Reorder the list to be on the following form:
    L0 → Ln → L1 → Ln-1 → L2 → Ln-2 → …

You may not modify the values in the list's nodes. Only nodes themselves may 
be changed.

EXAMPLES:
    Input: head = [1,2,3,4]
    Output: [1,4,2,3]

    Input: head = [1,2,3,4,5]
    Output: [1,5,2,4,3]

CONSTRAINTS:
- The number of nodes in the list is in range [1, 5 * 10^4]
- 1 <= Node.val <= 1000

================================================================================
"""
from typing import Optional


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# ============================================================================
# SOLUTION 1: Three Steps - Find Middle, Reverse, Merge (Optimal)
# ============================================================================
def reorderList(head: Optional[ListNode]) -> None:
    """
    Three steps:
    1. Find middle of list (fast & slow pointers)
    2. Reverse second half
    3. Merge two halves alternately
    
    Time: O(n)
    Space: O(1)
    
    Do not return anything, modify head in-place instead.
    """
    if not head or not head.next:
        return
    
    # Step 1: Find middle (slow will be at middle)
    slow, fast = head, head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    
    # slow is at the end of first half
    # slow.next is the start of second half
    
    # Step 2: Reverse second half
    second = slow.next
    slow.next = None  # Cut the list
    
    prev = None
    while second:
        next_temp = second.next
        second.next = prev
        prev = second
        second = next_temp
    
    second = prev  # Head of reversed second half
    
    # Step 3: Merge two halves alternately
    first = head
    while second:
        # Save next pointers
        first_next = first.next
        second_next = second.next
        
        # Interleave
        first.next = second
        second.next = first_next
        
        # Move forward
        first = first_next
        second = second_next


# ============================================================================
# SOLUTION 2: Using Stack (O(n) space)
# ============================================================================
def reorderList_stack(head: Optional[ListNode]) -> None:
    """
    Use stack to reverse second half efficiently.
    
    Time: O(n)
    Space: O(n)
    """
    if not head or not head.next:
        return
    
    # Push all nodes to stack
    stack = []
    curr = head
    while curr:
        stack.append(curr)
        curr = curr.next
    
    # Merge first half with reversed second half
    n = len(stack)
    curr = head
    
    for _ in range(n // 2):
        back = stack.pop()
        
        # Insert back after curr
        back.next = curr.next
        curr.next = back
        
        # Move to next pair position
        curr = back.next
    
    # Terminate the list
    curr.next = None


# ============================================================================
# SOLUTION 3: Using Deque (Similar to stack approach)
# ============================================================================
from collections import deque

def reorderList_deque(head: Optional[ListNode]) -> None:
    """
    Use deque to pop from both ends.
    
    Time: O(n)
    Space: O(n)
    """
    if not head:
        return
    
    # Collect all nodes
    nodes = deque()
    curr = head
    while curr:
        nodes.append(curr)
        curr = curr.next
    
    # Alternate between front and back
    curr = nodes.popleft()
    toggle = True
    
    while nodes:
        if toggle:
            next_node = nodes.pop()
        else:
            next_node = nodes.popleft()
        
        curr.next = next_node
        curr = next_node
        toggle = not toggle
    
    curr.next = None


# ============================================================================
# HELPER FUNCTIONS FOR TESTING
# ============================================================================
def create_linked_list(values):
    """Create linked list from list of values"""
    if not values:
        return None
    head = ListNode(values[0])
    curr = head
    for val in values[1:]:
        curr.next = ListNode(val)
        curr = curr.next
    return head


def linked_list_to_list(head):
    """Convert linked list to Python list"""
    result = []
    curr = head
    count = 0
    while curr and count < 20:  # Prevent infinite loop
        result.append(curr.val)
        curr = curr.next
        count += 1
    return result


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Even number of nodes
    head1 = create_linked_list([1, 2, 3, 4])
    print(f"Input: {linked_list_to_list(head1)}")
    reorderList(head1)
    print(f"Output (Optimal): {linked_list_to_list(head1)}")
    # Expected: [1, 4, 2, 3]
    print()
    
    # Test Case 2: Odd number of nodes
    head2 = create_linked_list([1, 2, 3, 4, 5])
    print(f"Input: {linked_list_to_list(head2)}")
    reorderList(head2)
    print(f"Output: {linked_list_to_list(head2)}")
    # Expected: [1, 5, 2, 4, 3]
    print()
    
    # Test Case 3: Two nodes
    head3 = create_linked_list([1, 2])
    print(f"Input: {linked_list_to_list(head3)}")
    reorderList(head3)
    print(f"Output: {linked_list_to_list(head3)}")
    # Expected: [1, 2]
    print()
    
    # Test Case 4: Single node
    head4 = create_linked_list([1])
    print(f"Input: {linked_list_to_list(head4)}")
    reorderList(head4)
    print(f"Output: {linked_list_to_list(head4)}")
    # Expected: [1]
    print()
    
    # Test Case 5: Stack approach
    head5 = create_linked_list([1, 2, 3, 4, 5, 6])
    print(f"Input: {linked_list_to_list(head5)}")
    reorderList_stack(head5)
    print(f"Output (Stack): {linked_list_to_list(head5)}")
    # Expected: [1, 6, 2, 5, 3, 4]


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. THE THREE-STEP APPROACH:
   
   This problem combines THREE classic linked list operations:
   
   a) Find Middle (Fast & Slow pointers)
   b) Reverse Linked List
   c) Merge Two Lists (alternating)
   
   Each is a common practice question on its own!

2. FINDING THE MIDDLE:
   
   For [1,2,3,4]:
   - slow at 2, fast at 4
   - Second half starts at slow.next = 3
   
   For [1,2,3,4,5]:
   - slow at 3, fast at 5
   - Second half starts at slow.next = 4

3. WHY CUT THE LIST?
   
   slow.next = None
   
   This separates the two halves:
   - First half: 1 → 2 → None
   - Second half: 3 → 4 (or 3 → 4 → 5)
   
   Makes merging cleaner!

4. MERGING ALTERNATELY:
   
   First:  1 → 2 → None
   Second: 4 → 3 → None (reversed)
   
   Step 1: 1 → 4, save 2, save 3
   Step 2: 4 → 2 → 3 → None
   
   Result: 1 → 4 → 2 → 3

5. THE PATTERN FOR ODD LENGTH:
   
   [1,2,3,4,5]
   First half: [1,2,3]
   Second half: [4,5] → reversed: [5,4]
   
   Merge: 1→5→2→4→3
   
   Middle element (3) stays in first half.

6. COMMON MISTAKES:
   
   ❌ Not cutting the list (slow.next = None)
   ❌ Off-by-one in finding middle
   ❌ Not handling even vs odd length

7. WHY O(1) SPACE IS IMPORTANT:
   
   Stack approach uses O(n) space.
   Three-step approach uses O(1) space.
   
   Interviewer may ask: "Can you do better than O(n) space?"

8. VALIDATION TECHNIQUE:
   
   [1,2,3,4,5]:
   - L0=1, L4=5 → 1,5
   - L1=2, L3=4 → 1,5,2,4
   - L2=3 → 1,5,2,4,3
   
   Pattern: first from start, last from end, repeat

9. RELATED PROBLEMS:
   
   - Palindrome Linked List (LC 234) - Same first two steps!
   - Merge Two Lists (LC 21)
   - Reverse Linked List (LC 206)
   - Middle of Linked List (LC 876)

10. practice PRESENTATION:
    
    "This problem combines three classic operations:
    1. Find middle using fast & slow pointers
    2. Reverse the second half
    3. Merge alternately
    
    Each of these is O(n), so total is O(n).
    Space is O(1) since we only use pointers."
    
    This shows you understand the building blocks!

================================================================================
"""
