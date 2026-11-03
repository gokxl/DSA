"""
================================================================================
PROBLEM: Min Stack (LeetCode 155)
Difficulty: Medium | Pattern: Design (Stack)
================================================================================

PROBLEM STATEMENT:
Design a stack that supports push, pop, top, and retrieving the minimum element 
in constant time.

Implement the MinStack class:
- MinStack(): Initializes the stack object.
- void push(int val): Pushes element val onto the stack.
- void pop(): Removes the element on the top of the stack.
- int top(): Gets the top element of the stack.
- int getMin(): Retrieves the minimum element in the stack.

You must implement a solution with O(1) time complexity for each function.

EXAMPLES:
    Input: ["MinStack","push","push","push","getMin","pop","top","getMin"]
           [[],[-2],[0],[-3],[],[],[],[]]
    Output: [null,null,null,null,-3,null,0,-2]

    Explanation:
    MinStack minStack = new MinStack();
    minStack.push(-2);
    minStack.push(0);
    minStack.push(-3);
    minStack.getMin(); // return -3
    minStack.pop();
    minStack.top();    // return 0
    minStack.getMin(); // return -2

CONSTRAINTS:
- -2^31 <= val <= 2^31 - 1
- Methods pop, top and getMin will always be called on non-empty stacks
- At most 3 * 10^4 calls will be made

================================================================================
"""


# ============================================================================
# SOLUTION 1: Two Stacks (Standard)
# ============================================================================
class MinStack:
    """
    Main stack for values, auxiliary stack for minimums.
    Min stack tracks minimum at each level.
    
    Time: O(1) for all operations
    Space: O(n)
    """
    
    def __init__(self):
        self.stack = []
        self.min_stack = []
    
    def push(self, val: int) -> None:
        self.stack.append(val)
        
        # Push to min stack if it's a new minimum (or equal)
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)
    
    def pop(self) -> None:
        if self.stack:
            val = self.stack.pop()
            
            # Pop from min stack if we're removing the current min
            if val == self.min_stack[-1]:
                self.min_stack.pop()
    
    def top(self) -> int:
        return self.stack[-1]
    
    def getMin(self) -> int:
        return self.min_stack[-1]


# ============================================================================
# SOLUTION 2: Store (value, min_so_far) pairs
# ============================================================================
class MinStack_Pairs:
    """
    Store (value, minimum_at_this_level) pairs.
    
    Time: O(1) for all operations
    Space: O(n)
    """
    
    def __init__(self):
        self.stack = []  # List of (value, min_so_far)
    
    def push(self, val: int) -> None:
        current_min = min(val, self.stack[-1][1]) if self.stack else val
        self.stack.append((val, current_min))
    
    def pop(self) -> None:
        self.stack.pop()
    
    def top(self) -> int:
        return self.stack[-1][0]
    
    def getMin(self) -> int:
        return self.stack[-1][1]


# ============================================================================
# SOLUTION 3: Single Stack with Encoding (Space Optimized)
# ============================================================================
class MinStack_Encoded:
    """
    Store difference from minimum. Recover values on access.
    
    When pushing value smaller than min:
    - Store (val - old_min) which is negative
    - Update min to val
    
    When popping and diff is negative:
    - Actual value was the current min
    - Restore old min as (current_min - diff)
    
    Time: O(1) for all operations
    Space: O(n) but more space efficient in practice
    """
    
    def __init__(self):
        self.stack = []
        self.min_val = float('inf')
    
    def push(self, val: int) -> None:
        if not self.stack:
            self.stack.append(0)
            self.min_val = val
        else:
            diff = val - self.min_val
            self.stack.append(diff)
            if diff < 0:
                self.min_val = val
    
    def pop(self) -> None:
        diff = self.stack.pop()
        
        if diff < 0:
            # We're popping the minimum, restore old min
            self.min_val = self.min_val - diff
        
        if not self.stack:
            self.min_val = float('inf')
    
    def top(self) -> int:
        diff = self.stack[-1]
        if diff < 0:
            return self.min_val
        else:
            return self.min_val + diff
    
    def getMin(self) -> int:
        return self.min_val


# ============================================================================
# SOLUTION 4: Node-based with min pointer
# ============================================================================
class StackNode:
    def __init__(self, val: int, min_val: int, next_node=None):
        self.val = val
        self.min_val = min_val
        self.next = next_node


class MinStack_LinkedList:
    """
    Linked list implementation with min stored in each node.
    
    Time: O(1) for all operations
    Space: O(n)
    """
    
    def __init__(self):
        self.head = None
    
    def push(self, val: int) -> None:
        if self.head is None:
            self.head = StackNode(val, val)
        else:
            self.head = StackNode(val, min(val, self.head.min_val), self.head)
    
    def pop(self) -> None:
        self.head = self.head.next
    
    def top(self) -> int:
        return self.head.val
    
    def getMin(self) -> int:
        return self.head.min_val


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Basic operations
    print("=== Test 1: Two Stacks ===")
    stack = MinStack()
    stack.push(-2)
    stack.push(0)
    stack.push(-3)
    print(f"getMin(): {stack.getMin()}")  # -3
    stack.pop()
    print(f"top(): {stack.top()}")  # 0
    print(f"getMin(): {stack.getMin()}")  # -2
    print()
    
    # Test Case 2: Pairs approach
    print("=== Test 2: Pairs ===")
    stack2 = MinStack_Pairs()
    stack2.push(1)
    stack2.push(2)
    stack2.push(-1)
    print(f"getMin(): {stack2.getMin()}")  # -1
    stack2.pop()
    print(f"getMin(): {stack2.getMin()}")  # 1
    print()
    
    # Test Case 3: Encoded approach
    print("=== Test 3: Encoded ===")
    stack3 = MinStack_Encoded()
    stack3.push(5)
    stack3.push(3)
    stack3.push(7)
    print(f"getMin(): {stack3.getMin()}")  # 3
    print(f"top(): {stack3.top()}")  # 7
    stack3.pop()
    stack3.pop()
    print(f"getMin(): {stack3.getMin()}")  # 5
    print()
    
    # Test Case 4: Duplicates
    print("=== Test 4: Duplicates ===")
    stack4 = MinStack()
    stack4.push(0)
    stack4.push(1)
    stack4.push(0)
    print(f"getMin(): {stack4.getMin()}")  # 0
    stack4.pop()
    print(f"getMin(): {stack4.getMin()}")  # 0


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. THE CHALLENGE:
   
   Stack operations are O(1), but finding min is O(n).
   How to make getMin() O(1)?
   
   Solution: Track minimum at each stack level.

2. TWO STACKS APPROACH:
   
   Main stack: [values...]
   Min stack: [min at each level...]
   
   Push to min stack when value <= current min.
   Pop from min stack when popping the minimum.
   
   Why <=? Handle duplicates!

3. PAIRS APPROACH:
   
   Store (value, min_so_far) at each level.
   
   More space but simpler logic.

4. ENCODED APPROACH:
   
   Store difference from minimum: (val - min)
   
   If diff < 0: this value became new min
   On pop with diff < 0: restore old_min = curr_min - diff
   
   Clever but tricky to explain!

5. WHY NOT JUST TRACK MIN?
   
   When we pop the minimum, what's the new min?
   We'd need to scan the whole stack!
   
   Solution: Track min history.

6. DUPLICATE HANDLING:
   
   When pushing value equal to min, still push to min stack!
   
   [1, 1] with min_stack [1]
   Pop → min_stack should still have [1]
   
   Use <= not < when pushing to min stack.

7. FOLLOW-UP: MaxStack
   
   Same idea but track maximum instead.
   
   Additional challenge: popMax() - remove max from middle.
   Need TreeMap/SortedDict + DLL for O(log n) popMax.

8. COMMON MISTAKES:
   
   ❌ Using < instead of <= for duplicates
   ❌ Forgetting to pop from min stack
   ❌ Not handling empty stack

9. RELATED PROBLEMS:
   
   - Max Stack (LC 716)
   - Implement Queue using Stacks (LC 232)
   - Daily Temperatures (LC 739)

10. HOW TO EXPLAIN IT:
    
    "The challenge is O(1) getMin. A single min variable won't
    work because when we pop the min, we don't know the next min.
    
    I'll use two stacks: main stack for values, min stack for
    the minimum at each level.
    
    On push: add to main; add to min if value <= current min.
    On pop: pop from main; pop from min if popping the minimum.
    
    getMin returns min_stack[-1]. All operations are O(1)."
    
    Mention the duplicate edge case!

================================================================================
"""
