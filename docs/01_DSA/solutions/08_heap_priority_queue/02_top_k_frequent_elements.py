"""
================================================================================
PROBLEM: Top K Frequent Elements (LeetCode 347)
Difficulty: Medium | Pattern: Heap / Bucket Sort
================================================================================

PROBLEM STATEMENT:
Given an integer array nums and an integer k, return the k most frequent elements.
You may return the answer in any order.

EXAMPLES:
    Input: nums = [1,1,1,2,2,3], k = 2
    Output: [1,2]
    Explanation: 1 appears 3 times, 2 appears 2 times

    Input: nums = [1], k = 1
    Output: [1]

CONSTRAINTS:
- 1 <= nums.length <= 10^5
- -10^4 <= nums[i] <= 10^4
- k is in the range [1, the number of unique elements in the array]
- It is guaranteed that the answer is unique

FOLLOW-UP: Your algorithm's time complexity must be better than O(n log n)

================================================================================
"""
from typing import List
from collections import Counter
import heapq


# ============================================================================
# SOLUTION 1: Min-Heap of Size K (Optimal for large n)
# ============================================================================
def topKFrequent_heap(nums: List[int], k: int) -> List[int]:
    """
    Use min-heap of size k to find top k frequent elements.
    
    1. Count frequencies
    2. Use min-heap to keep top k elements
    3. Pop all from heap
    
    Time: O(n) for counting + O(n log k) for heap = O(n log k)
    Space: O(n) for counter + O(k) for heap
    """
    # Count frequencies
    count = Counter(nums)
    
    # Use min-heap of size k
    # We want top k, so we keep the k largest by removing smallest
    min_heap = []
    
    for num, freq in count.items():
        heapq.heappush(min_heap, (freq, num))
        if len(min_heap) > k:
            heapq.heappop(min_heap)  # Remove smallest frequency
    
    return [num for freq, num in min_heap]


# ============================================================================
# SOLUTION 2: Bucket Sort (O(n) time!)
# ============================================================================
def topKFrequent_bucket(nums: List[int], k: int) -> List[int]:
    """
    Use bucket sort where index = frequency.
    
    1. Count frequencies
    2. Create buckets where bucket[i] = elements with frequency i
    3. Collect k elements from highest frequency buckets
    
    Time: O(n)
    Space: O(n)
    """
    count = Counter(nums)
    
    # Buckets: bucket[freq] = list of numbers with that frequency
    # Max frequency is len(nums)
    buckets = [[] for _ in range(len(nums) + 1)]
    
    for num, freq in count.items():
        buckets[freq].append(num)
    
    # Collect k elements from highest frequency buckets
    result = []
    for freq in range(len(nums), 0, -1):
        for num in buckets[freq]:
            result.append(num)
            if len(result) == k:
                return result
    
    return result


# ============================================================================
# SOLUTION 3: Quick Select (O(n) average)
# ============================================================================
def topKFrequent_quickselect(nums: List[int], k: int) -> List[int]:
    """
    Quick select to find kth largest frequency.
    
    Time: O(n) average, O(n²) worst case
    Space: O(n)
    """
    import random
    
    count = Counter(nums)
    unique = list(count.keys())
    n = len(unique)
    
    def partition(left: int, right: int, pivot_idx: int) -> int:
        pivot_freq = count[unique[pivot_idx]]
        
        # Move pivot to end
        unique[pivot_idx], unique[right] = unique[right], unique[pivot_idx]
        
        store_idx = left
        for i in range(left, right):
            if count[unique[i]] < pivot_freq:
                unique[store_idx], unique[i] = unique[i], unique[store_idx]
                store_idx += 1
        
        # Move pivot to final place
        unique[store_idx], unique[right] = unique[right], unique[store_idx]
        return store_idx
    
    def quickselect(left: int, right: int, k_smallest: int) -> None:
        if left == right:
            return
        
        pivot_idx = random.randint(left, right)
        pivot_idx = partition(left, right, pivot_idx)
        
        if k_smallest == pivot_idx:
            return
        elif k_smallest < pivot_idx:
            quickselect(left, pivot_idx - 1, k_smallest)
        else:
            quickselect(pivot_idx + 1, right, k_smallest)
    
    # Find (n-k)th smallest = kth largest
    quickselect(0, n - 1, n - k)
    
    return unique[n - k:]


# ============================================================================
# SOLUTION 4: Using Python's nlargest (Clean and efficient)
# ============================================================================
def topKFrequent_nlargest(nums: List[int], k: int) -> List[int]:
    """
    Use heapq.nlargest with custom key.
    
    Time: O(n log k) when k << n
    Space: O(n)
    """
    count = Counter(nums)
    # nlargest internally uses a min-heap of size k
    return heapq.nlargest(k, count.keys(), key=count.get)


# ============================================================================
# SOLUTION 5: Sorting (Simple but doesn't meet follow-up)
# ============================================================================
def topKFrequent_sort(nums: List[int], k: int) -> List[int]:
    """
    Sort by frequency.
    
    Time: O(n log n) - doesn't meet follow-up requirement
    Space: O(n)
    """
    count = Counter(nums)
    sorted_nums = sorted(count.keys(), key=lambda x: count[x], reverse=True)
    return sorted_nums[:k]


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Standard case
    nums1, k1 = [1, 1, 1, 2, 2, 3], 2
    print(f"nums={nums1}, k={k1}")
    print(f"Heap: {topKFrequent_heap(nums1, k1)}")
    print(f"Bucket: {topKFrequent_bucket(nums1, k1)}")
    print(f"nlargest: {topKFrequent_nlargest(nums1, k1)}")
    # Expected: [1, 2] (order may vary)
    print()
    
    # Test Case 2: Single element
    nums2, k2 = [1], 1
    print(f"nums={nums2}, k={k2}")
    print(f"Result: {topKFrequent_heap(nums2, k2)}")
    # Expected: [1]
    print()
    
    # Test Case 3: All same frequency
    nums3, k3 = [1, 2, 3, 4], 2
    print(f"nums={nums3}, k={k3}")
    print(f"Result: {topKFrequent_bucket(nums3, k3)}")
    # Expected: Any 2 elements
    print()
    
    # Test Case 4: k equals unique count
    nums4, k4 = [1, 1, 2, 2, 3], 3
    print(f"nums={nums4}, k={k4}")
    print(f"Result: {topKFrequent_heap(nums4, k4)}")
    # Expected: [1, 2, 3]
    print()
    
    # Test Case 5: Negative numbers
    nums5, k5 = [-1, -1, -1, 2, 2, 0], 2
    print(f"nums={nums5}, k={k5}")
    print(f"Result: {topKFrequent_quickselect(nums5, k5)}")
    # Expected: [-1, 2]


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. THREE MAIN APPROACHES:
   
   a) Heap (O(n log k)): Best when k << n
   b) Bucket Sort (O(n)): Best overall time complexity
   c) Quick Select (O(n) avg): Good alternative
   
   Know at least heap and bucket sort!

2. BUCKET SORT INSIGHT:
   
   Frequency can only be 1 to n (array length).
   Create n+1 buckets, put elements by frequency.
   Iterate from highest bucket → collect k elements.
   
   This is TRUE O(n) time!

3. MIN-HEAP FOR TOP K:
   
   Counterintuitive: Use MIN-heap, not max-heap!
   
   Keep heap size = k
   When adding element with larger freq, pop smallest
   Result: k largest frequencies remain
   
   This is O(n log k), better than O(n log n) sort.

4. PYTHON'S heapq.nlargest:
   
   heapq.nlargest(k, iterable, key=...)
   
   Internally uses min-heap of size k.
   Very clean solution for practice sessions.

5. QUICK SELECT FOR TOP K:
   
   Partition around kth largest.
   Average O(n), worst O(n²).
   
   Good to mention as alternative.

6. WHY NOT MAX-HEAP?
   
   Max-heap: Push all n elements → O(n log n)
   Min-heap of size k: Each op is O(log k) → O(n log k)
   
   When k << n, big difference!

7. RELATED PROBLEMS:
   
   - Top K Frequent Words (LC 692)
   - Kth Largest Element in Array (LC 215)
   - Sort Characters By Frequency (LC 451)

8. COMMON MISTAKES:
   
   ❌ Using max-heap (worse complexity)
   ❌ Forgetting bucket sort (best time)
   ❌ Not handling ties correctly

9. TIME COMPLEXITY COMPARISON:
   
   Sorting: O(n log n)
   Heap: O(n log k)
   Bucket Sort: O(n)
   Quick Select: O(n) average
   
   Bucket sort is optimal!

10. practice TIP:
    
    "I'll use bucket sort for O(n) time.
    
    The key insight is that frequency ranges from 1 to n.
    I create n buckets, place each number in bucket[frequency].
    Then iterate from highest bucket and collect k elements.
    
    Alternative: min-heap of size k gives O(n log k)."
    
    Show you know multiple approaches!

================================================================================
"""
