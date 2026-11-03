"""
================================================================================
PROBLEM: Min Stack (LeetCode 155)
Difficulty: Medium | Pattern: Stack Design
================================================================================

PROBLEM STATEMENT:
Design a stack that supports push, pop, top, and retrieving the minimum element 
in constant time.

Implement the MinStack class:
- MinStack() initializes the stack object.
- void push(int val) pushes the element val onto the stack.
- void pop() removes the element on the top of the stack.
- int top() gets the top element of the stack.
- int getMin() retrieves the minimum element in the stack.

You must implement a solution with O(1) time complexity for each function.

EXAMPLES:
    Input:
    ["MinStack","push","push","push","getMin","pop","top","getMin"]
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
- Methods pop, top and getMin operations will always be called on non-empty stacks
- At most 3 * 10^4 calls will be made to push, pop, top, and getMin

================================================================================
"""


# ============================================================================
# SOLUTION 1: Two Stacks (Most Common)
# ============================================================================
class MinStack:
    """
    Use two stacks:
    - Main stack: stores all values
    - Min stack: stores minimum at each level
    
    Time: O(1) for all operations
    Space: O(n) for both stacks
    """
    
    def __init__(self):
        self.stack = []
        self.min_stack = []
    
    def push(self, val: int) -> None:
        self.stack.append(val)
        # Push minimum of (current value, current min)
        if self.min_stack:
            self.min_stack.append(min(val, self.min_stack[-1]))
        else:
            self.min_stack.append(val)
    
    def pop(self) -> None:
        self.stack.pop()
        self.min_stack.pop()
    
    def top(self) -> int:
        return self.stack[-1]
    
    def getMin(self) -> int:
        return self.min_stack[-1]


# ============================================================================
# SOLUTION 2: Single Stack with Tuple
# ============================================================================
class MinStack2:
    """
    Single stack storing tuples of (value, current_min).
    
    Time: O(1) for all operations
    Space: O(n) but slightly more memory per element
    """
    
    def __init__(self):
        self.stack = []  # Each element is (value, min_so_far)
    
    def push(self, val: int) -> None:
        if self.stack:
            current_min = min(val, self.stack[-1][1])
        else:
            current_min = val
        self.stack.append((val, current_min))
    
    def pop(self) -> None:
        self.stack.pop()
    
    def top(self) -> int:
        return self.stack[-1][0]
    
    def getMin(self) -> int:
        return self.stack[-1][1]


# ============================================================================
# SOLUTION 3: Optimized Min Stack (Store only when min changes)
# ============================================================================
class MinStack3:
    """
    Optimize space: only push to min_stack when value <= current min.
    
    Time: O(1) for all operations
    Space: O(n) but min_stack can be smaller
    """
    
    def __init__(self):
        self.stack = []
        self.min_stack = []
    
    def push(self, val: int) -> None:
        self.stack.append(val)
        # Only push to min_stack if val is new minimum (or equal)
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)
    
    def pop(self) -> None:
        val = self.stack.pop()
        # Only pop from min_stack if we're removing the minimum
        if val == self.min_stack[-1]:
            self.min_stack.pop()
    
    def top(self) -> int:
        return self.stack[-1]
    
    def getMin(self) -> int:
        return self.min_stack[-1]


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Basic operations
    print("Testing MinStack (Two Stacks):")
    minStack = MinStack()
    minStack.push(-2)
    minStack.push(0)
    minStack.push(-3)
    print(f"getMin(): {minStack.getMin()}")  # -3
    minStack.pop()
    print(f"top(): {minStack.top()}")        # 0
    print(f"getMin(): {minStack.getMin()}")  # -2
    print()
    
    # Test Case 2: Single element
    print("Testing MinStack2 (Tuple):")
    minStack2 = MinStack2()
    minStack2.push(5)
    print(f"top(): {minStack2.top()}")       # 5
    print(f"getMin(): {minStack2.getMin()}") # 5
    print()
    
    # Test Case 3: Increasing values
    print("Testing MinStack3 (Optimized):")
    minStack3 = MinStack3()
    minStack3.push(1)
    minStack3.push(2)
    minStack3.push(3)
    print(f"getMin(): {minStack3.getMin()}")  # 1
    minStack3.pop()
    minStack3.pop()
    print(f"getMin(): {minStack3.getMin()}")  # 1
    print()
    
    # Test Case 4: Duplicate minimums
    print("Testing duplicate minimums:")
    ms = MinStack()
    ms.push(0)
    ms.push(1)
    ms.push(0)
    print(f"getMin(): {ms.getMin()}")  # 0
    ms.pop()
    print(f"getMin(): {ms.getMin()}")  # 0 (still has another 0)


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. THE CHALLENGE:
   
   Regular stack: O(1) push, pop, top
   Finding minimum: O(n) if we scan
   
   How to get O(1) getMin()? Track minimum at each state!

2. KEY INSIGHT - SNAPSHOT OF MIN:
   
   When we push, snapshot what the minimum was at that moment.
   When we pop, we restore to the previous snapshot.
   
   Stack state:  [5, 3, 7, 2]
   Min at each:  [5, 3, 3, 2]
   
   Pop 2: min becomes 3 (previous snapshot)

3. THREE APPROACHES:
   
   a) Two separate stacks:
      - Cleaner code
      - Easy to understand
      - Slightly more memory operations
   
   b) Single stack with tuples:
      - One data structure
      - Each element slightly larger
   
   c) Optimized min stack:
      - Only store new minimums
      - Handles duplicates carefully (use <=, not <)

4. THE DUPLICATE TRAP:
   
   If min_stack only stores strict minimums:
   push(0), push(0), pop() → min_stack loses both 0s!
   
   Solution: Use <= when comparing, so duplicates are stored.

5. VISUAL EXAMPLE:
   
   Operations: push(-2), push(0), push(-3), pop()
   
   Stack:      [-2]     [-2,0]    [-2,0,-3]   [-2,0]
   Min Stack:  [-2]     [-2,-2]   [-2,-2,-3]  [-2,-2]
   
   getMin() always returns min_stack[-1]

6. FOLLOW-UP: MAX STACK (LC 716)
   
   Same approach but track maximum.
   Harder variant: Support popMax() - need different structure.

7. RELATED DESIGN PROBLEMS:
   - Max Stack (LC 716)
   - Design Stack with Increment (LC 1381)
   - Online Stock Span (LC 901)
   - Design Browser History (LC 1472)

8. COMPLEXITY:
   
   Time: O(1) for all operations
   Space: O(n) for storing elements + mins

9. HOW TO EXPLAIN IT:
   
   Start by asking: "Can I use extra space?"
   If yes, the two-stack solution is cleanest.
   If challenged on space, mention the optimized version.

10. COMMON MISTAKES:
    - Using < instead of <= for optimized version
    - Forgetting to handle empty stack edge cases
    - Not keeping min_stack in sync with main stack

================================================================================
"""
