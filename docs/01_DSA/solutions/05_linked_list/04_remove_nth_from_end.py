"""
================================================================================
PROBLEM: Remove Nth Node From End of List (LeetCode 19)
Difficulty: Medium | Pattern: Two Pointers + Linked List
================================================================================

PROBLEM STATEMENT:
Given the head of a linked list, remove the nth node from the end of the list 
and return its head.

EXAMPLES:
    Input: head = [1,2,3,4,5], n = 2
    Output: [1,2,3,5]
    Explanation: Remove 4 (2nd from end)

    Input: head = [1], n = 1
    Output: []
    Explanation: Remove only node

    Input: head = [1,2], n = 1
    Output: [1]
    Explanation: Remove 2 (1st from end)

CONSTRAINTS:
- The number of nodes in the list is sz
- 1 <= sz <= 30
- 0 <= Node.val <= 100
- 1 <= n <= sz

FOLLOW-UP: 
Could you do this in one pass?

================================================================================
"""
from typing import Optional


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# ============================================================================
# SOLUTION 1: Two Pointers - One Pass (Optimal)
# ============================================================================
def removeNthFromEnd(head: Optional[ListNode], n: int) -> Optional[ListNode]:
    """
    Use two pointers with n-node gap.
    When fast reaches end, slow is at node before target.
    
    Time: O(L) where L is list length
    Space: O(1)
    """
    # Dummy node handles edge case of removing head
    dummy = ListNode(0, head)
    slow = dummy
    fast = dummy
    
    # Move fast n+1 steps ahead
    # (so slow lands at node BEFORE the one to remove)
    for _ in range(n + 1):
        fast = fast.next
    
    # Move both until fast reaches end
    while fast:
        slow = slow.next
        fast = fast.next
    
    # Remove the nth node from end
    slow.next = slow.next.next
    
    return dummy.next


# ============================================================================
# SOLUTION 2: Two Passes (Simpler to understand)
# ============================================================================
def removeNthFromEnd_two_pass(head: Optional[ListNode], n: int) -> Optional[ListNode]:
    """
    First pass: Count total nodes
    Second pass: Remove (length - n)th node
    
    Time: O(L)
    Space: O(1)
    """
    # First pass: count nodes
    length = 0
    curr = head
    while curr:
        length += 1
        curr = curr.next
    
    # Handle removing head
    if n == length:
        return head.next
    
    # Second pass: find node before target
    target_idx = length - n - 1  # Index of node BEFORE target
    curr = head
    for _ in range(target_idx):
        curr = curr.next
    
    # Remove target
    curr.next = curr.next.next
    
    return head


# ============================================================================
# SOLUTION 3: Using Recursion (Different approach)
# ============================================================================
def removeNthFromEnd_recursive(head: Optional[ListNode], n: int) -> Optional[ListNode]:
    """
    Use recursion to count from end.
    
    Time: O(L)
    Space: O(L) for recursion stack
    """
    def helper(node: ListNode) -> int:
        """Returns position from end (1-indexed)"""
        if not node:
            return 0
        
        position = helper(node.next) + 1
        
        if position == n + 1:
            # node is right before the target
            node.next = node.next.next
        
        return position
    
    dummy = ListNode(0, head)
    helper(dummy)
    return dummy.next


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
    # Test Case 1: Middle node
    head1 = create_linked_list([1, 2, 3, 4, 5])
    print(f"Input: {linked_list_to_list(head1)}, n = 2")
    result1 = removeNthFromEnd(head1, 2)
    print(f"Output (One-pass): {linked_list_to_list(result1)}")
    # Expected: [1, 2, 3, 5]
    print()
    
    # Test Case 2: Remove only node
    head2 = create_linked_list([1])
    print(f"Input: {linked_list_to_list(head2)}, n = 1")
    result2 = removeNthFromEnd(head2, 1)
    print(f"Output: {linked_list_to_list(result2)}")
    # Expected: []
    print()
    
    # Test Case 3: Remove last node
    head3 = create_linked_list([1, 2])
    print(f"Input: {linked_list_to_list(head3)}, n = 1")
    result3 = removeNthFromEnd_two_pass(head3, 1)
    print(f"Output (Two-pass): {linked_list_to_list(result3)}")
    # Expected: [1]
    print()
    
    # Test Case 4: Remove first node (head)
    head4 = create_linked_list([1, 2])
    print(f"Input: {linked_list_to_list(head4)}, n = 2")
    result4 = removeNthFromEnd(head4, 2)
    print(f"Output: {linked_list_to_list(result4)}")
    # Expected: [2]
    print()
    
    # Test Case 5: Recursive approach
    head5 = create_linked_list([1, 2, 3, 4, 5])
    print(f"Input: {linked_list_to_list(head5)}, n = 3")
    result5 = removeNthFromEnd_recursive(head5, 3)
    print(f"Output (Recursive): {linked_list_to_list(result5)}")
    # Expected: [1, 2, 4, 5]


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. THE TWO-POINTER TRICK:
   
   Create n-node gap between fast and slow.
   When fast is at end, slow is at position we need.
   
   Visual for [1,2,3,4,5], n=2:
   
   After advancing fast by n+1:
   D → 1 → 2 → 3 → 4 → 5 → None
   s           f
   
   After moving together:
   D → 1 → 2 → 3 → 4 → 5 → None
               s           f
   
   slow.next = slow.next.next removes 4

2. WHY n+1 STEPS FOR FAST?
   
   We need slow to be at the node BEFORE the one to remove.
   (Because in singly linked list, we can only delete next node)
   
   Gap of n+1 means when fast = None, slow is 1 before target.

3. WHY DUMMY NODE?
   
   What if we remove the head?
   - Without dummy: special case handling
   - With dummy: uniform logic
   
   Example [1,2], n=2 (remove head):
   D → 1 → 2 → None
   s       f
   slow.next = slow.next.next = 2

4. TWO-PASS VS ONE-PASS:
   
   Two-pass:
   - Count nodes first
   - Find (length - n)th node
   - Easier to understand
   
   One-pass:
   - Two pointers with gap
   - More elegant
   - Follow-up asks for this!

5. COMMON MISTAKES:
   
   ❌ Moving fast by n instead of n+1
   ❌ Forgetting dummy node (fails when removing head)
   ❌ Off-by-one errors in counting

6. EDGE CASES:
   
   - Remove head (n = length)
   - Remove tail (n = 1)
   - Single node list (n = 1)
   - Two-node list

7. VERIFICATION TECHNIQUE:
   
   For [1,2,3,4,5], n=2:
   - 5 is 1st from end
   - 4 is 2nd from end ← remove this
   - Should get [1,2,3,5]
   
   Walk through pointer positions on whiteboard!

8. SOLVING FLOW:
   
   1. Clarify: "nth from END, not beginning?"
   2. Start with two-pass (simpler)
   3. Then optimize to one-pass
   4. Mention dummy node benefit

9. TIME/SPACE TRADE-OFF:
   
   Could store all nodes in array:
   - Time: O(n)
   - Space: O(n)
   
   Two-pointer approach:
   - Time: O(n)  
   - Space: O(1) ← Better!

10. RELATED PROBLEMS:
    
    - Middle of Linked List (LC 876)
    - Rotate List (LC 61)
    - Swap Nodes in Pairs (LC 24)
    
    All use similar two-pointer techniques!

================================================================================
"""
