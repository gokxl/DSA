"""
================================================================================
PROBLEM: Merge Two Sorted Lists (LeetCode 21)
Difficulty: Easy | Pattern: Linked List + Two Pointers
================================================================================

PROBLEM STATEMENT:
You are given the heads of two sorted linked lists list1 and list2.

Merge the two lists into one sorted list. The list should be made by splicing 
together the nodes of the first two lists.

Return the head of the merged linked list.

EXAMPLES:
    Input: list1 = [1,2,4], list2 = [1,3,4]
    Output: [1,1,2,3,4,4]

    Input: list1 = [], list2 = []
    Output: []

    Input: list1 = [], list2 = [0]
    Output: [0]

CONSTRAINTS:
- The number of nodes in both lists is in range [0, 50]
- -100 <= Node.val <= 100
- Both list1 and list2 are sorted in non-decreasing order

================================================================================
"""
from typing import Optional


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# ============================================================================
# SOLUTION 1: Iterative with Dummy Node (Optimal)
# ============================================================================
def mergeTwoLists(list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
    """
    Use dummy node to simplify edge cases.
    Compare and pick smaller value at each step.
    
    Time: O(n + m) where n, m are lengths of lists
    Space: O(1) - we're reusing existing nodes
    """
    dummy = ListNode(0)  # Dummy head
    curr = dummy
    
    while list1 and list2:
        if list1.val <= list2.val:
            curr.next = list1
            list1 = list1.next
        else:
            curr.next = list2
            list2 = list2.next
        curr = curr.next
    
    # Attach remaining nodes (one list might not be exhausted)
    curr.next = list1 if list1 else list2
    
    return dummy.next


# ============================================================================
# SOLUTION 2: Recursive
# ============================================================================
def mergeTwoLists_recursive(list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
    """
    Recursively merge by picking smaller head.
    
    Time: O(n + m)
    Space: O(n + m) for recursion stack
    """
    # Base cases
    if not list1:
        return list2
    if not list2:
        return list1
    
    # Pick smaller and recurse
    if list1.val <= list2.val:
        list1.next = mergeTwoLists_recursive(list1.next, list2)
        return list1
    else:
        list2.next = mergeTwoLists_recursive(list1, list2.next)
        return list2


# ============================================================================
# SOLUTION 3: Without Dummy Node (Handle edge cases manually)
# ============================================================================
def mergeTwoLists_no_dummy(list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
    """
    Same logic but without dummy node.
    Need to handle head separately.
    
    Time: O(n + m)
    Space: O(1)
    """
    # Edge cases
    if not list1:
        return list2
    if not list2:
        return list1
    
    # Determine head
    if list1.val <= list2.val:
        head = list1
        list1 = list1.next
    else:
        head = list2
        list2 = list2.next
    
    curr = head
    
    # Merge rest
    while list1 and list2:
        if list1.val <= list2.val:
            curr.next = list1
            list1 = list1.next
        else:
            curr.next = list2
            list2 = list2.next
        curr = curr.next
    
    curr.next = list1 if list1 else list2
    
    return head


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
    # Test Case 1: Normal case
    list1 = create_linked_list([1, 2, 4])
    list2 = create_linked_list([1, 3, 4])
    print(f"List1: {linked_list_to_list(list1)}")
    print(f"List2: {linked_list_to_list(list2)}")
    result = mergeTwoLists(list1, list2)
    print(f"Merged (Iterative): {linked_list_to_list(result)}")
    # Expected: [1, 1, 2, 3, 4, 4]
    print()
    
    # Test Case 2: Both empty
    list1 = create_linked_list([])
    list2 = create_linked_list([])
    result = mergeTwoLists(list1, list2)
    print(f"Empty + Empty: {linked_list_to_list(result)}")
    # Expected: []
    print()
    
    # Test Case 3: One empty
    list1 = create_linked_list([])
    list2 = create_linked_list([0])
    result = mergeTwoLists(list1, list2)
    print(f"Empty + [0]: {linked_list_to_list(result)}")
    # Expected: [0]
    print()
    
    # Test Case 4: Recursive
    list1 = create_linked_list([1, 3, 5])
    list2 = create_linked_list([2, 4, 6])
    result = mergeTwoLists_recursive(list1, list2)
    print(f"Merged (Recursive): {linked_list_to_list(result)}")
    # Expected: [1, 2, 3, 4, 5, 6]
    print()
    
    # Test Case 5: Different lengths
    list1 = create_linked_list([1])
    list2 = create_linked_list([2, 3, 4, 5])
    result = mergeTwoLists(list1, list2)
    print(f"Merged (Diff lengths): {linked_list_to_list(result)}")
    # Expected: [1, 2, 3, 4, 5]


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. DUMMY NODE TECHNIQUE:
   
   Creating a dummy head simplifies code:
   - No need to handle "first node" specially
   - Just return dummy.next at the end
   
   This is a VERY common linked list pattern!

2. TWO-POINTER MERGE:
   
   Same concept as merging two sorted arrays:
   - Compare heads, pick smaller
   - Advance that pointer
   - Repeat until one exhausted
   - Attach remaining

3. WHY DUMMY NODE HELPS:
   
   Without dummy:
   - Need to determine head first
   - Then merge rest
   - More code, more edge cases
   
   With dummy:
   - Head is just dummy.next
   - Uniform logic throughout

4. ITERATIVE VS RECURSIVE:
   
   Iterative:
   - O(1) space
   - More explicit
   - Preferred for practice sessions
   
   Recursive:
   - O(n+m) space (call stack)
   - Elegant but risky for large lists
   - Good to mention as alternative

5. BUILDING BLOCK FOR HARDER PROBLEMS:
   
   This is used in:
   - Merge K Sorted Lists (LC 23) - Google favorite!
   - Sort List (LC 148) - Merge sort for lists
   - Merge Sorted Array (LC 88)

6. FOLLOW-UP: MERGE K SORTED LISTS
   
   Two approaches:
   
   a) Divide and Conquer (optimal):
      - Pair up lists and merge
      - O(N log k) where N = total nodes
   
   b) Min-Heap:
      - Push first node of each list
      - Pop min, push its next
      - O(N log k)

7. EDGE CASES:
   
   - Both lists empty
   - One list empty
   - Lists of different lengths
   - Duplicate values
   - Single element lists

8. STABILITY:
   
   This merge is stable:
   - Equal elements maintain relative order
   - list1.val <= list2.val (not <)

9. COMMON MISTAKES:
   
   ❌ Forgetting to advance curr
   ❌ Not attaching remaining list
   ❌ Returning dummy instead of dummy.next

10. practice TIP:
    
    Always clarify:
    - "Can I modify the input lists?"
    - "Should I create new nodes or reuse existing?"
    
    For this problem, we reuse nodes (O(1) space).

================================================================================
"""
