"""
================================================================================
PROBLEM: Find Median from Data Stream (LeetCode 295)
Difficulty: Hard | Pattern: Two Heaps
================================================================================

PROBLEM STATEMENT:
The median is the middle value in an ordered integer list. If the size of the 
list is even, there is no middle value, and the median is the mean of the two 
middle values.

Implement the MedianFinder class:
- MedianFinder() initializes the MedianFinder object.
- void addNum(int num) adds the integer num from the data stream to the data 
  structure.
- double findMedian() returns the median of all elements so far.

EXAMPLES:
    Input:
    ["MedianFinder", "addNum", "addNum", "findMedian", "addNum", "findMedian"]
    [[], [1], [2], [], [3], []]
    Output: [null, null, null, 1.5, null, 2.0]
    
    Explanation:
    MedianFinder mf = new MedianFinder();
    mf.addNum(1);    // [1]
    mf.addNum(2);    // [1, 2]
    mf.findMedian(); // return 1.5 (mean of 1 and 2)
    mf.addNum(3);    // [1, 2, 3]
    mf.findMedian(); // return 2.0

CONSTRAINTS:
- -10^5 <= num <= 10^5
- There will be at least one element in the data structure before calling 
  findMedian.
- At most 5 * 10^4 calls will be made to addNum and findMedian.

FOLLOW-UP:
1. If all integers are in range [0, 100], optimize
2. If 99% of integers are in range [0, 100], optimize

================================================================================
"""
import heapq
from sortedcontainers import SortedList  # pip install sortedcontainers


# ============================================================================
# SOLUTION 1: Two Heaps (Optimal)
# ============================================================================
class MedianFinder:
    """
    Use two heaps to maintain balance:
    - Max-heap for smaller half (left)
    - Min-heap for larger half (right)
    
    Invariants:
    1. All elements in max_heap <= all elements in min_heap
    2. Size difference is at most 1
    
    Time: O(log n) for addNum, O(1) for findMedian
    Space: O(n)
    """
    
    def __init__(self):
        # Max-heap (smaller half) - use negatives
        self.small = []  # Max-heap (negate values)
        # Min-heap (larger half)
        self.large = []  # Min-heap
    
    def addNum(self, num: int) -> None:
        # Add to max-heap (smaller half)
        heapq.heappush(self.small, -num)
        
        # Ensure all elements in small <= all elements in large
        if self.small and self.large and -self.small[0] > self.large[0]:
            heapq.heappush(self.large, -heapq.heappop(self.small))
        
        # Balance sizes: small can have at most 1 more element
        if len(self.small) > len(self.large) + 1:
            heapq.heappush(self.large, -heapq.heappop(self.small))
        
        if len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))
    
    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2.0


# ============================================================================
# SOLUTION 2: Simplified Two Heaps
# ============================================================================
class MedianFinder_Simplified:
    """
    Slightly different add logic - always add to small first, then balance.
    """
    
    def __init__(self):
        self.small = []  # Max-heap (negate values)
        self.large = []  # Min-heap
    
    def addNum(self, num: int) -> None:
        # Always add to small first, then move to large
        heapq.heappush(self.small, -num)
        heapq.heappush(self.large, -heapq.heappop(self.small))
        
        # Keep small >= large in size
        if len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))
    
    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2.0


# ============================================================================
# SOLUTION 3: Using SortedList (For reference)
# ============================================================================
class MedianFinder_SortedList:
    """
    Using SortedList for simpler implementation.
    Note: Not built-in Python, requires sortedcontainers package.
    
    Time: O(log n) for addNum, O(1) for findMedian
    Space: O(n)
    """
    
    def __init__(self):
        self.nums = SortedList()
    
    def addNum(self, num: int) -> None:
        self.nums.add(num)
    
    def findMedian(self) -> float:
        n = len(self.nums)
        if n % 2 == 1:
            return self.nums[n // 2]
        return (self.nums[n // 2 - 1] + self.nums[n // 2]) / 2.0


# ============================================================================
# SOLUTION 4: Counting Sort for Follow-up
# ============================================================================
class MedianFinder_Counting:
    """
    For follow-up: If all integers are in [0, 100].
    
    Time: O(1) for addNum, O(100) = O(1) for findMedian
    Space: O(100) = O(1)
    """
    
    def __init__(self):
        self.count = [0] * 101  # Count for 0-100
        self.total = 0
    
    def addNum(self, num: int) -> None:
        self.count[num] += 1
        self.total += 1
    
    def findMedian(self) -> float:
        # Find median position(s)
        if self.total % 2 == 1:
            target = self.total // 2 + 1
            cumsum = 0
            for i in range(101):
                cumsum += self.count[i]
                if cumsum >= target:
                    return i
        else:
            target1 = self.total // 2
            target2 = target1 + 1
            cumsum = 0
            first = second = 0
            found_first = False
            for i in range(101):
                cumsum += self.count[i]
                if not found_first and cumsum >= target1:
                    first = i
                    found_first = True
                if cumsum >= target2:
                    second = i
                    break
            return (first + second) / 2.0


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Standard usage
    mf = MedianFinder()
    mf.addNum(1)
    mf.addNum(2)
    print(f"After [1,2]: {mf.findMedian()}")  # Expected: 1.5
    mf.addNum(3)
    print(f"After [1,2,3]: {mf.findMedian()}")  # Expected: 2.0
    print()
    
    # Test Case 2: Simplified version
    mf2 = MedianFinder_Simplified()
    for num in [5, 3, 8, 1, 9]:
        mf2.addNum(num)
        print(f"After adding {num}: median = {mf2.findMedian()}")
    # After [5,3,8,1,9] sorted = [1,3,5,8,9], median = 5
    print()
    
    # Test Case 3: Negative numbers
    mf3 = MedianFinder()
    mf3.addNum(-1)
    mf3.addNum(-2)
    mf3.addNum(-3)
    print(f"Negative nums [-1,-2,-3]: {mf3.findMedian()}")  # Expected: -2.0
    print()
    
    # Test Case 4: Counting sort (for numbers in [0,100])
    mf4 = MedianFinder_Counting()
    for num in [10, 20, 30, 40, 50]:
        mf4.addNum(num)
    print(f"Counting sort median: {mf4.findMedian()}")  # Expected: 30


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. THE TWO-HEAP INSIGHT:
   
   Median divides data into two halves.
   - Max-heap: Smaller half (top is largest of smaller)
   - Min-heap: Larger half (top is smallest of larger)
   
   Median is at the boundary between heaps!

2. HEAP REPRESENTATION:
   
   Python heapq is MIN-heap only.
   For MAX-heap, negate values:
   
   heappush(small, -num)  # Add
   -heappop(small)        # Get max
   -small[0]              # Peek max

3. INVARIANTS TO MAINTAIN:
   
   1. All in small <= all in large
   2. |len(small) - len(large)| <= 1
   3. len(small) >= len(large) (for odd count, median in small)

4. ADD LOGIC FLOW:
   
   1. Add to small (max-heap)
   2. If small's max > large's min, move to large
   3. Rebalance sizes

5. FIND MEDIAN:
   
   Odd count: top of small (larger heap)
   Even count: average of both tops

6. TIME COMPLEXITY:
   
   addNum: O(log n) for heap operations
   findMedian: O(1)
   
   Much better than sorting: O(n log n) for each findMedian!

7. FOLLOW-UP: BOUNDED RANGE [0, 100]:
   
   Use counting sort!
   - count[i] = frequency of i
   - Find median by cumulative sum
   
   O(1) time for both operations!

8. FOLLOW-UP: 99% IN [0, 100]:
   
   Use counting for [0, 100], two heaps for outliers.
   Most queries are O(1), rare outliers need heap.

9. RELATED PROBLEMS:
   
   - Sliding Window Median (LC 480) - harder!
   - Kth Largest Element in Stream (LC 703)

10. practice TIP:
    
    "I'll use two heaps - a max-heap for the smaller half
    and a min-heap for the larger half.
    
    The median is always at the boundary:
    - Odd count: top of larger heap
    - Even count: average of both tops
    
    This gives O(log n) add and O(1) find median."
    
    Be ready to explain the rebalancing logic clearly!

================================================================================
"""
