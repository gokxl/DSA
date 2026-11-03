"""
================================================================================
PROBLEM: Merge k Sorted Lists (LeetCode 23)
Difficulty: Hard | Pattern: Heap
================================================================================

PROBLEM STATEMENT:
You are given an array of k linked-lists lists, each linked-list is sorted in 
ascending order.

Merge all the linked-lists into one sorted linked-list and return it.

EXAMPLES:
    Input: lists = [[1,4,5],[1,3,4],[2,6]]
    Output: [1,1,2,3,4,4,5,6]
    
    Merging:
    1->4->5
    1->3->4
    2->6
    
    Result: 1->1->2->3->4->4->5->6

    Input: lists = []
    Output: []

    Input: lists = [[]]
    Output: []

CONSTRAINTS:
- k == lists.length
- 0 <= k <= 10^4
- 0 <= lists[i].length <= 500
- -10^4 <= lists[i][j] <= 10^4
- lists[i] is sorted in ascending order
- The sum of lists[i].length will not exceed 10^4

================================================================================
"""
from typing import List, Optional
import heapq


# Definition for singly-linked list
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# ============================================================================
# SOLUTION 1: Min-Heap (Optimal)
# ============================================================================
def mergeKLists(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    """
    Use min-heap to always get the smallest node among k lists.
    
    Time: O(N log k) where N = total nodes, k = number of lists
    Space: O(k) for the heap
    """
    # Min-heap: (value, index, node)
    # Index is used as tiebreaker since ListNode is not comparable
    min_heap = []
    
    # Initialize heap with first node from each list
    for i, head in enumerate(lists):
        if head:
            heapq.heappush(min_heap, (head.val, i, head))
    
    dummy = ListNode()
    current = dummy
    
    while min_heap:
        val, i, node = heapq.heappop(min_heap)
        
        # Add smallest node to result
        current.next = node
        current = current.next
        
        # Push next node from same list
        if node.next:
            heapq.heappush(min_heap, (node.next.val, i, node.next))
    
    return dummy.next


# ============================================================================
# SOLUTION 2: Divide and Conquer
# ============================================================================
def mergeKLists_divide_conquer(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    """
    Merge lists in pairs, reducing count by half each round.
    
    Time: O(N log k)
    Space: O(log k) for recursion
    """
    if not lists:
        return None
    
    def merge_two(l1: ListNode, l2: ListNode) -> ListNode:
        """Merge two sorted lists"""
        dummy = ListNode()
        current = dummy
        
        while l1 and l2:
            if l1.val <= l2.val:
                current.next = l1
                l1 = l1.next
            else:
                current.next = l2
                l2 = l2.next
            current = current.next
        
        current.next = l1 or l2
        return dummy.next
    
    # Keep merging pairs until one list remains
    while len(lists) > 1:
        merged = []
        for i in range(0, len(lists), 2):
            l1 = lists[i]
            l2 = lists[i + 1] if i + 1 < len(lists) else None
            merged.append(merge_two(l1, l2))
        lists = merged
    
    return lists[0]


# ============================================================================
# SOLUTION 3: Sequential Merge (Less optimal but intuitive)
# ============================================================================
def mergeKLists_sequential(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    """
    Merge lists one by one: merge 1&2, then result with 3, etc.
    
    Time: O(kN) - not optimal
    Space: O(1)
    """
    if not lists:
        return None
    
    def merge_two(l1: ListNode, l2: ListNode) -> ListNode:
        dummy = ListNode()
        current = dummy
        
        while l1 and l2:
            if l1.val <= l2.val:
                current.next = l1
                l1 = l1.next
            else:
                current.next = l2
                l2 = l2.next
            current = current.next
        
        current.next = l1 or l2
        return dummy.next
    
    result = lists[0]
    for i in range(1, len(lists)):
        result = merge_two(result, lists[i])
    
    return result


# ============================================================================
# SOLUTION 4: Using Python's heapq.merge (For reference)
# ============================================================================
def mergeKLists_pythonic(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    """
    Convert to arrays, use built-in merge, convert back.
    Not ideal for practice sessions but good to know.
    
    Time: O(N log k)
    Space: O(N)
    """
    def list_to_array(head):
        arr = []
        while head:
            arr.append(head.val)
            head = head.next
        return arr
    
    def array_to_list(arr):
        dummy = ListNode()
        current = dummy
        for val in arr:
            current.next = ListNode(val)
            current = current.next
        return dummy.next
    
    arrays = [list_to_array(head) for head in lists if head]
    merged = list(heapq.merge(*arrays))
    return array_to_list(merged)


# ============================================================================
# HELPER FUNCTIONS FOR TESTING
# ============================================================================
def create_linked_list(arr):
    """Create linked list from array"""
    dummy = ListNode()
    current = dummy
    for val in arr:
        current.next = ListNode(val)
        current = current.next
    return dummy.next


def linked_list_to_array(head):
    """Convert linked list to array"""
    arr = []
    while head:
        arr.append(head.val)
        head = head.next
    return arr


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Standard case
    lists1 = [
        create_linked_list([1, 4, 5]),
        create_linked_list([1, 3, 4]),
        create_linked_list([2, 6])
    ]
    result1 = mergeKLists(lists1)
    print(f"Heap: {linked_list_to_array(result1)}")
    # Expected: [1, 1, 2, 3, 4, 4, 5, 6]
    
    # Test Case 2: Divide and conquer
    lists2 = [
        create_linked_list([1, 4, 5]),
        create_linked_list([1, 3, 4]),
        create_linked_list([2, 6])
    ]
    result2 = mergeKLists_divide_conquer(lists2)
    print(f"D&C:  {linked_list_to_array(result2)}")
    # Expected: [1, 1, 2, 3, 4, 4, 5, 6]
    
    # Test Case 3: Empty input
    print(f"Empty: {mergeKLists([])}")
    # Expected: None
    
    # Test Case 4: Single list
    lists4 = [create_linked_list([1, 2, 3])]
    result4 = mergeKLists(lists4)
    print(f"Single: {linked_list_to_array(result4)}")
    # Expected: [1, 2, 3]
    
    # Test Case 5: Lists with empty lists
    lists5 = [None, create_linked_list([1]), None]
    result5 = mergeKLists(lists5)
    print(f"With nulls: {linked_list_to_array(result5)}")
    # Expected: [1]


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. THE KEY INSIGHT:
   
   At any time, the next node in result is the MINIMUM among
   the current heads of all k lists.
   
   Min-heap gives us this in O(log k) time!

2. HEAP APPROACH:
   
   1. Push first node of each list to heap
   2. Pop minimum, add to result
   3. Push next node from same list
   4. Repeat until heap empty
   
   Why O(N log k)? Each node pushed/popped once, each op is O(log k)

3. THE TIEBREAKER ISSUE:
   
   heapq compares tuples element by element.
   If values equal, it compares ListNode objects → Error!
   
   Solution: Add unique index as second element:
   (value, index, node)

4. DIVIDE AND CONQUER:
   
   Round 1: Merge pairs → k/2 lists
   Round 2: Merge pairs → k/4 lists
   ...
   Round log(k): → 1 list
   
   Each round processes N nodes → O(N log k)

5. WHY NOT SEQUENTIAL MERGE?
   
   Merge 1 with 2: n₁ + n₂
   Merge result with 3: n₁ + n₂ + n₃
   ...
   
   Total: O(kN) where N is total nodes
   Much worse than O(N log k)!

6. SPACE COMPLEXITY:
   
   Heap: O(k) - only k nodes in heap
   D&C: O(log k) for recursion stack
   Sequential: O(1) if done iteratively

7. COMMON MISTAKES:
   
   ❌ Forgetting to check for empty lists/heads
   ❌ Not handling heap tiebreaker for equal values
   ❌ Modifying original lists unexpectedly

8. FOLLOW-UP: MERGE K SORTED ARRAYS:
   
   Same approach works! Just use indices instead of node pointers:
   heap = [(arr[0], i, 0) for i, arr in enumerate(arrays) if arr]

9. RELATED PROBLEMS:
   
   - Merge Two Sorted Lists (LC 21)
   - Ugly Number II (LC 264)
   - Find K Pairs with Smallest Sums (LC 373)

10. practice TIP:
    
    "I'll use a min-heap of size k. I push the first node from
    each list, then repeatedly pop the minimum and push the
    next node from that list.
    
    This gives O(N log k) time and O(k) space.
    
    Alternative: Divide and conquer - merge pairs of lists,
    reducing count by half each round. Same time complexity."

================================================================================
"""
