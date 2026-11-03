"""
================================================================================
PROBLEM: Reverse Linked List (LeetCode 206)
Difficulty: Easy | Pattern: Linked List Basics
================================================================================

PROBLEM STATEMENT:
Given the head of a singly linked list, reverse the list, and return the 
reversed list.

EXAMPLES:
    Input: head = [1,2,3,4,5]
    Output: [5,4,3,2,1]

    Input: head = [1,2]
    Output: [2,1]

    Input: head = []
    Output: []

CONSTRAINTS:
- The number of nodes in the list is in range [0, 5000]
- -5000 <= Node.val <= 5000

FOLLOW-UP: 
A linked list can be reversed either iteratively or recursively. 
Can you implement both?

================================================================================
"""
from typing import Optional


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# ============================================================================
# SOLUTION 1: Iterative (Optimal)
# ============================================================================
def reverseList(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Iteratively reverse by changing next pointers.
    
    prev → curr → next  becomes  prev ← curr  next
    
    Time: O(n)
    Space: O(1)
    """
    prev = None
    curr = head
    
    while curr:
        next_temp = curr.next  # Save next node
        curr.next = prev       # Reverse the link
        prev = curr            # Move prev forward
        curr = next_temp       # Move curr forward
    
    return prev


# ============================================================================
# SOLUTION 2: Recursive
# ============================================================================
def reverseList_recursive(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Recursively reverse the list.
    
    Base case: empty or single node
    Recursive case: reverse rest, then attach head to end
    
    Time: O(n)
    Space: O(n) for recursion stack
    """
    # Base case
    if not head or not head.next:
        return head
    
    # Recursively reverse the rest
    new_head = reverseList_recursive(head.next)
    
    # head.next is now the last node of reversed sublist
    # Make it point back to head
    head.next.next = head
    head.next = None  # Head becomes tail, so next = None
    
    return new_head


# ============================================================================
# SOLUTION 3: Using Stack (Educational)
# ============================================================================
def reverseList_stack(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Use stack to reverse order.
    
    Time: O(n)
    Space: O(n)
    """
    if not head:
        return None
    
    # Push all nodes to stack
    stack = []
    curr = head
    while curr:
        stack.append(curr)
        curr = curr.next
    
    # Pop and link
    new_head = stack.pop()
    curr = new_head
    while stack:
        curr.next = stack.pop()
        curr = curr.next
    curr.next = None  # Last node points to None
    
    return new_head


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
    while curr:
        result.append(curr.val)
        curr = curr.next
    return result


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Normal list
    head1 = create_linked_list([1, 2, 3, 4, 5])
    print(f"Input: {linked_list_to_list(head1)}")
    result1 = reverseList(head1)
    print(f"Output (Iterative): {linked_list_to_list(result1)}")
    # Expected: [5, 4, 3, 2, 1]
    print()
    
    # Test Case 2: Two nodes
    head2 = create_linked_list([1, 2])
    print(f"Input: {linked_list_to_list(head2)}")
    result2 = reverseList_recursive(head2)
    print(f"Output (Recursive): {linked_list_to_list(result2)}")
    # Expected: [2, 1]
    print()
    
    # Test Case 3: Empty list
    head3 = create_linked_list([])
    print(f"Input: {linked_list_to_list(head3)}")
    result3 = reverseList(head3)
    print(f"Output: {linked_list_to_list(result3)}")
    # Expected: []
    print()
    
    # Test Case 4: Single node
    head4 = create_linked_list([1])
    print(f"Input: {linked_list_to_list(head4)}")
    result4 = reverseList(head4)
    print(f"Output: {linked_list_to_list(result4)}")
    # Expected: [1]
    print()
    
    # Test Case 5: Stack method
    head5 = create_linked_list([1, 2, 3])
    print(f"Input: {linked_list_to_list(head5)}")
    result5 = reverseList_stack(head5)
    print(f"Output (Stack): {linked_list_to_list(result5)}")
    # Expected: [3, 2, 1]


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. THE THREE-POINTER PATTERN (Iterative):
   
   prev = None    (will become new tail)
   curr = head    (node we're processing)
   next_temp      (saved to not lose connection)
   
   At each step:
   1. Save next (next_temp = curr.next)
   2. Reverse link (curr.next = prev)
   3. Move prev forward (prev = curr)
   4. Move curr forward (curr = next_temp)

2. VISUAL WALKTHROUGH:
   
   Initial: None   1 → 2 → 3 → None
            prev  curr
   
   Step 1:  None ← 1   2 → 3 → None
                  prev curr
   
   Step 2:  None ← 1 ← 2   3 → None
                      prev curr
   
   Step 3:  None ← 1 ← 2 ← 3   None
                          prev curr
   
   Return prev (which is 3)

3. RECURSIVE INTUITION:
   
   reverseList([1,2,3,4,5])
   = reverseList([2,3,4,5]) + [1]
   = [5,4,3,2] + [1]
   = [5,4,3,2,1]
   
   Key: head.next.next = head makes 2→1
        head.next = None makes 1→None

4. WHY ITERATIVE IS PREFERRED:
   
   - O(1) space vs O(n) for recursive
   - No stack overflow risk
   - Often what interviewers want to see first

5. COMMON MISTAKES:
   
   ❌ Forgetting to save next before reversing
   ❌ Not setting head.next = None in recursive
   ❌ Returning head instead of prev/new_head

6. EDGE CASES:
   
   - Empty list: Return None
   - Single node: Return as is
   - Two nodes: Test boundary

7. VARIATIONS TO KNOW:
   
   - Reverse between positions m and n (LC 92)
   - Reverse in k-groups (LC 25) - Google favorite!
   - Reverse alternate k nodes

8. FOLLOW-UP: REVERSE IN K-GROUPS
   
   Google asks this often! The approach:
   - Check if k nodes exist
   - Reverse k nodes (same technique)
   - Recursively handle rest
   - Connect the reversed group

9. practice TIP:
   
   Start with iterative solution (cleaner).
   Then mention: "I can also solve this recursively"
   
   If asked about space: "Iterative is O(1) space,
   recursive is O(n) due to call stack"

10. CODE CLARITY:
    
    Use descriptive names:
    - prev, curr, next_temp (not p, c, n)
    - Makes your thought process clear
    - Easier to debug on whiteboard

================================================================================
"""
