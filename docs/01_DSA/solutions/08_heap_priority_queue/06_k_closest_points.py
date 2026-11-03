"""
================================================================================
PROBLEM: K Closest Points to Origin (LeetCode 973)
Difficulty: Medium | Pattern: Heap / Quick Select
================================================================================

PROBLEM STATEMENT:
Given an array of points where points[i] = [xi, yi] represents a point on the 
X-Y plane and an integer k, return the k closest points to the origin (0, 0).

The distance between two points on the X-Y plane is the Euclidean distance:
√(x1 - x2)² + (y1 - y2)²

You may return the answer in any order. The answer is guaranteed to be unique 
(except for the order).

EXAMPLES:
    Input: points = [[1,3],[-2,2]], k = 1
    Output: [[-2,2]]
    Explanation:
    Distance of (1,3) = √(1² + 3²) = √10
    Distance of (-2,2) = √(4 + 4) = √8
    √8 < √10, so (-2,2) is closer

    Input: points = [[3,3],[5,-1],[-2,4]], k = 2
    Output: [[3,3],[-2,4]] (or [[-2,4],[3,3]])
    Distances: √18, √26, √20
    Two closest: √18 and √20

CONSTRAINTS:
- 1 <= k <= points.length <= 10^4
- -10^4 <= xi, yi <= 10^4

================================================================================
"""
from typing import List
import heapq
import random


# ============================================================================
# SOLUTION 1: Max-Heap of Size K
# ============================================================================
def kClosest_maxheap(points: List[List[int]], k: int) -> List[List[int]]:
    """
    Use max-heap of size k to track k closest points.
    
    Time: O(n log k)
    Space: O(k)
    """
    # Max-heap: negate distances
    max_heap = []
    
    for x, y in points:
        dist = -(x * x + y * y)  # Negate for max-heap
        
        if len(max_heap) < k:
            heapq.heappush(max_heap, (dist, [x, y]))
        elif dist > max_heap[0][0]:  # Closer point found
            heapq.heapreplace(max_heap, (dist, [x, y]))
    
    return [point for _, point in max_heap]


# ============================================================================
# SOLUTION 2: Min-Heap (Simpler but more space)
# ============================================================================
def kClosest_minheap(points: List[List[int]], k: int) -> List[List[int]]:
    """
    Push all points with distances, pop k times.
    
    Time: O(n + k log n)
    Space: O(n)
    """
    min_heap = [(x * x + y * y, x, y) for x, y in points]
    heapq.heapify(min_heap)  # O(n)
    
    result = []
    for _ in range(k):
        _, x, y = heapq.heappop(min_heap)
        result.append([x, y])
    
    return result


# ============================================================================
# SOLUTION 3: Quick Select
# ============================================================================
def kClosest_quickselect(points: List[List[int]], k: int) -> List[List[int]]:
    """
    Quick Select to find k closest without full sort.
    
    Time: O(n) average, O(n²) worst
    Space: O(1) extra
    """
    def distance(point):
        return point[0] ** 2 + point[1] ** 2
    
    def partition(left: int, right: int) -> int:
        # Random pivot for better average case
        pivot_idx = random.randint(left, right)
        points[pivot_idx], points[right] = points[right], points[pivot_idx]
        
        pivot_dist = distance(points[right])
        i = left
        
        for j in range(left, right):
            if distance(points[j]) <= pivot_dist:
                points[i], points[j] = points[j], points[i]
                i += 1
        
        points[i], points[right] = points[right], points[i]
        return i
    
    left, right = 0, len(points) - 1
    
    while left <= right:
        pivot_idx = partition(left, right)
        
        if pivot_idx == k:
            break
        elif pivot_idx < k:
            left = pivot_idx + 1
        else:
            right = pivot_idx - 1
    
    return points[:k]


# ============================================================================
# SOLUTION 4: Using heapq.nsmallest
# ============================================================================
def kClosest_nsmallest(points: List[List[int]], k: int) -> List[List[int]]:
    """
    Use Python's built-in nsmallest with custom key.
    
    Time: O(n log k)
    Space: O(k)
    """
    return heapq.nsmallest(k, points, key=lambda p: p[0] ** 2 + p[1] ** 2)


# ============================================================================
# SOLUTION 5: Sorting (Simple but not optimal)
# ============================================================================
def kClosest_sort(points: List[List[int]], k: int) -> List[List[int]]:
    """
    Sort all points by distance, return first k.
    
    Time: O(n log n)
    Space: O(n) for sorting
    """
    points.sort(key=lambda p: p[0] ** 2 + p[1] ** 2)
    return points[:k]


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Standard case
    points1, k1 = [[1, 3], [-2, 2]], 1
    print(f"Points: {points1}, k={k1}")
    print(f"Max-Heap: {kClosest_maxheap(points1.copy(), k1)}")
    print(f"Quick Select: {kClosest_quickselect(points1.copy(), k1)}")
    # Expected: [[-2, 2]]
    print()
    
    # Test Case 2: Multiple points
    points2, k2 = [[3, 3], [5, -1], [-2, 4]], 2
    print(f"Points: {points2}, k={k2}")
    print(f"nsmallest: {kClosest_nsmallest(points2.copy(), k2)}")
    # Expected: [[3,3], [-2,4]] or [[-2,4], [3,3]]
    print()
    
    # Test Case 3: Origin in points
    points3, k3 = [[0, 0], [1, 1], [2, 2]], 2
    print(f"Points: {points3}, k={k3}")
    print(f"Result: {kClosest_minheap(points3.copy(), k3)}")
    # Expected: [[0,0], [1,1]]
    print()
    
    # Test Case 4: All points equidistant
    points4, k4 = [[1, 0], [0, 1], [-1, 0], [0, -1]], 2
    print(f"Points: {points4}, k={k4}")
    print(f"Result: {kClosest_sort(points4.copy(), k4)}")
    # Expected: Any 2 points (all equidistant)
    print()
    
    # Test Case 5: Negative coordinates
    points5, k5 = [[-5, -5], [5, 5], [-1, -1], [1, 1]], 2
    print(f"Points: {points5}, k={k5}")
    print(f"Result: {kClosest_maxheap(points5.copy(), k5)}")
    # Expected: [[-1,-1], [1,1]] or [[1,1], [-1,-1]]


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. NO SQUARE ROOT NEEDED:
   
   Since √a < √b ⟺ a < b (for non-negative),
   we can compare x² + y² directly.
   
   Avoids floating point issues!

2. MAX-HEAP FOR K SMALLEST:
   
   Counterintuitive: Use MAX-heap of size k
   
   - Keep k smallest by removing LARGEST
   - Final heap has k smallest points
   
   Time: O(n log k) - better when k << n

3. QUICK SELECT APPROACH:
   
   Same as Kth Largest Element problem.
   
   After partition:
   - Elements at indices 0..pivot-1 are smaller
   - Element at pivot is in correct position
   
   Partition until pivot_idx == k

4. HEAP VS QUICK SELECT:
   
   Max-Heap:
   - Time: O(n log k)
   - Deterministic
   - Good for streaming
   
   Quick Select:
   - Time: O(n) average
   - Randomized (or deterministic with median-of-medians)
   - Modifies input array

5. PYTHON'S heapq.nsmallest:
   
   heapq.nsmallest(k, iterable, key=func)
   
   Uses max-heap internally.
   Very clean to write and explain.

6. EUCLIDEAN DISTANCE FORMULA:
   
   d(p, origin) = √(x² + y²)
   
   But for comparison: x² + y² is enough

7. COMMON MISTAKES:
   
   ❌ Using sqrt (unnecessary, float issues)
   ❌ Forgetting negative coordinates
   ❌ Using min-heap of all elements (O(n) space)

8. FOLLOW-UP VARIATIONS:
   
   - K closest to a given point (not origin)
   - Find closest pair of points
   - K closest in 3D space

9. RELATED PROBLEMS:
   
   - Kth Largest Element (LC 215)
   - Top K Frequent Elements (LC 347)
   - Closest Points on a plane (not LC)

10. HOW TO EXPLAIN IT:
    
    "I'll use a max-heap of size k. For each point, I calculate
    the squared distance (no sqrt needed for comparison).
    
    I keep the k smallest by removing the largest when the heap
    exceeds size k.
    
    This gives O(n log k) time and O(k) space.
    
    Alternative: Quick Select for O(n) average time."
    
    Mention the no-sqrt optimization - shows attention to detail!

================================================================================
"""
