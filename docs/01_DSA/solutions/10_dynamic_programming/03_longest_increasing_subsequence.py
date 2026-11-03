"""
================================================================================
PROBLEM: Longest Increasing Subsequence (LeetCode 300)
Difficulty: Medium | Pattern: DP + Binary Search
================================================================================

PROBLEM STATEMENT:
Given an integer array nums, return the length of the longest strictly 
increasing subsequence.

A subsequence is an array that can be derived from another array by deleting 
some or no elements without changing the order of the remaining elements.

EXAMPLES:
    Input: nums = [10,9,2,5,3,7,101,18]
    Output: 4
    Explanation: The longest increasing subsequence is [2,3,7,101], length = 4

    Input: nums = [0,1,0,3,2,3]
    Output: 4
    Explanation: [0,1,2,3]

    Input: nums = [7,7,7,7,7,7,7]
    Output: 1

CONSTRAINTS:
- 1 <= nums.length <= 2500
- -10^4 <= nums[i] <= 10^4

FOLLOW UP: Can you come up with an algorithm that runs in O(n log n)?

================================================================================
"""
from typing import List
import bisect


# ============================================================================
# SOLUTION 1: O(n²) DP
# ============================================================================
def lengthOfLIS_dp(nums: List[int]) -> int:
    """
    dp[i] = length of LIS ending at index i
    
    For each i, check all j < i:
    If nums[j] < nums[i], dp[i] = max(dp[i], dp[j] + 1)
    
    Time: O(n²)
    Space: O(n)
    """
    n = len(nums)
    dp = [1] * n  # Minimum LIS length is 1 (element itself)
    
    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)


# ============================================================================
# SOLUTION 2: O(n log n) with Binary Search
# ============================================================================
def lengthOfLIS(nums: List[int]) -> int:
    """
    Maintain array of smallest tail for each LIS length.
    
    tails[i] = smallest tail of all LIS with length i+1
    
    For each number, binary search to find its position.
    
    Time: O(n log n)
    Space: O(n)
    """
    tails = []  # tails[i] = smallest tail for LIS of length i+1
    
    for num in nums:
        # Binary search for position
        pos = bisect.bisect_left(tails, num)
        
        if pos == len(tails):
            tails.append(num)  # Extend LIS
        else:
            tails[pos] = num  # Replace with smaller tail
    
    return len(tails)


# ============================================================================
# SOLUTION 3: O(n log n) with manual binary search
# ============================================================================
def lengthOfLIS_manual(nums: List[int]) -> int:
    """
    Same approach with manual binary search.
    
    Time: O(n log n)
    Space: O(n)
    """
    tails = []
    
    def binary_search(target: int) -> int:
        """Find leftmost position where tails[pos] >= target"""
        left, right = 0, len(tails)
        
        while left < right:
            mid = (left + right) // 2
            if tails[mid] < target:
                left = mid + 1
            else:
                right = mid
        
        return left
    
    for num in nums:
        pos = binary_search(num)
        
        if pos == len(tails):
            tails.append(num)
        else:
            tails[pos] = num
    
    return len(tails)


# ============================================================================
# SOLUTION 4: Get actual LIS (not just length)
# ============================================================================
def lengthOfLIS_with_sequence(nums: List[int]) -> tuple:
    """
    Return both length and actual LIS.
    
    Track parent pointers to reconstruct.
    
    Time: O(n log n)
    Space: O(n)
    """
    n = len(nums)
    if n == 0:
        return 0, []
    
    # tails_idx[i] = index of smallest tail for LIS of length i+1
    tails_idx = []
    # parent[i] = previous index in LIS ending at i
    parent = [-1] * n
    
    for i, num in enumerate(nums):
        pos = bisect.bisect_left([nums[j] for j in tails_idx], num)
        
        if pos == len(tails_idx):
            tails_idx.append(i)
        else:
            tails_idx[pos] = i
        
        if pos > 0:
            parent[i] = tails_idx[pos - 1]
    
    # Reconstruct LIS
    lis = []
    idx = tails_idx[-1]
    while idx != -1:
        lis.append(nums[idx])
        idx = parent[idx]
    
    return len(lis), lis[::-1]


# ============================================================================
# SOLUTION 5: Segment Tree (for range queries)
# ============================================================================
def lengthOfLIS_segment_tree(nums: List[int]) -> int:
    """
    Use segment tree for O(n log n) solution.
    
    Coordinate compression + range max query.
    Good for when need to handle online queries.
    
    Time: O(n log n)
    Space: O(n)
    """
    # Coordinate compression
    sorted_nums = sorted(set(nums))
    rank = {v: i for i, v in enumerate(sorted_nums)}
    
    n = len(sorted_nums)
    tree = [0] * (2 * n)
    
    def update(pos: int, val: int) -> None:
        pos += n
        tree[pos] = max(tree[pos], val)
        while pos > 1:
            pos //= 2
            tree[pos] = max(tree[2 * pos], tree[2 * pos + 1])
    
    def query(left: int, right: int) -> int:
        """Max in range [left, right)"""
        result = 0
        left += n
        right += n
        while left < right:
            if left & 1:
                result = max(result, tree[left])
                left += 1
            if right & 1:
                right -= 1
                result = max(result, tree[right])
            left //= 2
            right //= 2
        return result
    
    ans = 0
    for num in nums:
        r = rank[num]
        # LIS ending at num = 1 + max LIS ending at smaller values
        length = query(0, r) + 1
        ans = max(ans, length)
        update(r, length)
    
    return ans


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Standard case
    nums1 = [10, 9, 2, 5, 3, 7, 101, 18]
    print(f"nums = {nums1}")
    print(f"O(n²) DP: {lengthOfLIS_dp(nums1)}")
    print(f"O(n log n): {lengthOfLIS(nums1)}")
    length, seq = lengthOfLIS_with_sequence(nums1)
    print(f"With sequence: length={length}, LIS={seq}")
    # Expected: 4 ([2,3,7,101] or [2,5,7,101])
    print()
    
    # Test Case 2: Another case
    nums2 = [0, 1, 0, 3, 2, 3]
    print(f"nums = {nums2}")
    print(f"Result: {lengthOfLIS(nums2)}")
    # Expected: 4
    print()
    
    # Test Case 3: All same
    nums3 = [7, 7, 7, 7, 7]
    print(f"nums = {nums3}")
    print(f"Result: {lengthOfLIS(nums3)}")
    # Expected: 1
    print()
    
    # Test Case 4: Decreasing
    nums4 = [5, 4, 3, 2, 1]
    print(f"nums = {nums4}")
    print(f"Result: {lengthOfLIS(nums4)}")
    # Expected: 1
    print()
    
    # Test Case 5: Increasing
    nums5 = [1, 2, 3, 4, 5]
    print(f"nums = {nums5}")
    print(f"Result: {lengthOfLIS(nums5)}")
    # Expected: 5


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. THE O(n log n) INSIGHT:
   
   Maintain array tails where:
   tails[i] = smallest ending element of all LIS of length i+1
   
   Key properties:
   - tails is always sorted (!)
   - Can use binary search to find position

2. WHY TAILS IS SORTED:
   
   If LIS of length i ends at x, and LIS of length i+1 ends at y,
   then y > x (since we extended x by adding larger element).
   
   So: tails[0] < tails[1] < ... < tails[k-1]

3. TWO CASES FOR NEW NUMBER:
   
   num = new element, pos = bisect_left(tails, num)
   
   Case 1: pos == len(tails)
   → num is larger than all, extends longest LIS
   → tails.append(num)
   
   Case 2: pos < len(tails)
   → num can improve some LIS (smaller tail)
   → tails[pos] = num

4. EXAMPLE WALKTHROUGH:
   
   nums = [10, 9, 2, 5, 3, 7]
   
   10: tails = [10]
   9:  tails = [9]      (replace 10)
   2:  tails = [2]      (replace 9)
   5:  tails = [2, 5]   (extend)
   3:  tails = [2, 3]   (replace 5)
   7:  tails = [2, 3, 7] (extend)
   
   LIS length = 3

5. TAILS ≠ ACTUAL LIS:
   
   tails is NOT the actual LIS!
   It just has the right length.
   
   For actual LIS, need to track parent pointers.

6. COMMON VARIATIONS:
   
   - Number of LIS (LC 673)
   - Longest Non-Decreasing Subsequence (use bisect_right)
   - Russian Doll Envelopes (LC 354) - 2D LIS

7. BINARY SEARCH CHOICE:
   
   bisect_left: For STRICTLY increasing (no equal)
   bisect_right: For NON-DECREASING (equal allowed)

8. TIME COMPLEXITY:
   
   O(n²): Try all pairs
   O(n log n): Binary search for each element

9. RELATED PROBLEMS:
   
   - Russian Doll Envelopes (LC 354)
   - Maximum Length of Pair Chain (LC 646)
   - Increasing Triplet Subsequence (LC 334)

10. HOW TO EXPLAIN IT:
    
    "The O(n²) solution uses dp[i] = LIS ending at i.
    For O(n log n), I maintain tails[i] = smallest ending
    element of any LIS of length i+1.
    
    Since tails is sorted, I can binary search to find
    where each new element belongs. If it's larger than
    all, it extends the LIS; otherwise, it improves
    some shorter LIS.
    
    Key insight: tails is always sorted because longer
    LIS must end at larger values."

================================================================================
"""
