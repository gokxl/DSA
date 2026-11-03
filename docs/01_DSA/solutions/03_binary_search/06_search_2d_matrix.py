"""
================================================================================
PROBLEM: Search a 2D Matrix (LeetCode 74)
Difficulty: Medium | Pattern: Binary Search + Matrix
================================================================================

PROBLEM STATEMENT:
You are given an m x n integer matrix with the following two properties:
- Each row is sorted in non-decreasing order.
- The first integer of each row is greater than the last integer of the previous row.

Given an integer target, return true if target is in matrix or false otherwise.

You must write a solution in O(log(m * n)) time complexity.

EXAMPLES:
    Input: matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3
    Output: true

    Input: matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 13
    Output: false

CONSTRAINTS:
- m == matrix.length
- n == matrix[i].length
- 1 <= m, n <= 100
- -10^4 <= matrix[i][j], target <= 10^4

================================================================================
"""

from typing import List


# ============================================================================
# SOLUTION 1: Single Binary Search (Treat as 1D array)
# ============================================================================
def searchMatrix(matrix: List[List[int]], target: int) -> bool:
    """
    Treat the 2D matrix as a flattened 1D sorted array.
    
    For index i in the virtual 1D array:
    - Row = i // n
    - Col = i % n
    
    Time: O(log(m * n))
    Space: O(1)
    """
    if not matrix or not matrix[0]:
        return False
    
    m, n = len(matrix), len(matrix[0])
    left, right = 0, m * n - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        # Convert 1D index to 2D coordinates
        row = mid // n
        col = mid % n
        value = matrix[row][col]
        
        if value == target:
            return True
        elif value < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return False


# ============================================================================
# SOLUTION 2: Two Binary Searches (Row first, then column)
# ============================================================================
def searchMatrix_two_searches(matrix: List[List[int]], target: int) -> bool:
    """
    Step 1: Binary search to find the row
    Step 2: Binary search within that row
    
    Time: O(log m + log n) = O(log(m * n))
    Space: O(1)
    """
    if not matrix or not matrix[0]:
        return False
    
    m, n = len(matrix), len(matrix[0])
    
    # Step 1: Find the row where target could be
    # Find the largest row where first element <= target
    top, bottom = 0, m - 1
    
    while top <= bottom:
        mid = top + (bottom - top) // 2
        
        if matrix[mid][0] <= target <= matrix[mid][n - 1]:
            # Target could be in this row
            row = mid
            break
        elif matrix[mid][0] > target:
            bottom = mid - 1
        else:  # matrix[mid][n-1] < target
            top = mid + 1
    else:
        # No suitable row found
        return False
    
    # Step 2: Binary search within the row
    left, right = 0, n - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if matrix[row][mid] == target:
            return True
        elif matrix[row][mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return False


# ============================================================================
# SOLUTION 3: Staircase Search (Alternative O(m + n))
# ============================================================================
def searchMatrix_staircase(matrix: List[List[int]], target: int) -> bool:
    """
    Start from top-right (or bottom-left).
    - If current > target: move left
    - If current < target: move down
    
    This works because of the sorted properties.
    
    Time: O(m + n) - not as efficient but still good
    Space: O(1)
    """
    if not matrix or not matrix[0]:
        return False
    
    m, n = len(matrix), len(matrix[0])
    row, col = 0, n - 1  # Start from top-right
    
    while row < m and col >= 0:
        if matrix[row][col] == target:
            return True
        elif matrix[row][col] > target:
            col -= 1  # Move left
        else:
            row += 1  # Move down
    
    return False


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Target exists
    matrix1 = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
    target1 = 3
    print(f"Matrix: {matrix1}")
    print(f"Target: {target1}")
    print(f"Output (1D): {searchMatrix(matrix1, target1)}")
    print(f"Output (2 searches): {searchMatrix_two_searches(matrix1, target1)}")
    print(f"Output (Staircase): {searchMatrix_staircase(matrix1, target1)}")
    # Expected: True
    print()
    
    # Test Case 2: Target doesn't exist
    matrix2 = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
    target2 = 13
    print(f"Matrix: {matrix2}")
    print(f"Target: {target2}")
    print(f"Output: {searchMatrix(matrix2, target2)}")
    # Expected: False
    print()
    
    # Test Case 3: Single element (found)
    matrix3 = [[1]]
    target3 = 1
    print(f"Matrix: {matrix3}, Target: {target3}")
    print(f"Output: {searchMatrix(matrix3, target3)}")
    # Expected: True
    print()
    
    # Test Case 4: Single element (not found)
    matrix4 = [[1]]
    target4 = 2
    print(f"Matrix: {matrix4}, Target: {target4}")
    print(f"Output: {searchMatrix(matrix4, target4)}")
    # Expected: False
    print()
    
    # Test Case 5: Target at boundaries
    matrix5 = [[1, 3, 5], [7, 9, 11], [13, 15, 17]]
    print(f"Matrix: {matrix5}")
    print(f"Target 1 (first): {searchMatrix(matrix5, 1)}")   # True
    print(f"Target 17 (last): {searchMatrix(matrix5, 17)}")  # True
    print(f"Target 0 (before): {searchMatrix(matrix5, 0)}")   # False
    print(f"Target 20 (after): {searchMatrix(matrix5, 20)}")  # False


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. KEY OBSERVATION:
   
   The matrix is essentially a flattened sorted array!
   
   [[1,  3,  5,  7],
    [10, 11, 16, 20],
    [23, 30, 34, 60]]
   
   Is equivalent to:
   [1, 3, 5, 7, 10, 11, 16, 20, 23, 30, 34, 60]

2. 1D INDEX TO 2D CONVERSION:
   
   For a matrix with n columns:
   
   Virtual 1D index i → 2D coordinates:
   - row = i // n
   - col = i % n
   
   Example: n=4, index 9
   - row = 9 // 4 = 2
   - col = 9 % 4 = 1
   - matrix[2][1] = 11 ✓

3. COMPARISON OF APPROACHES:
   
   | Approach      | Time Complexity | Notes                      |
   |---------------|-----------------|----------------------------|
   | Single BS     | O(log(m*n))     | Treat as 1D, most elegant  |
   | Two BS        | O(log m + log n)| Same as O(log(m*n))        |
   | Staircase     | O(m + n)        | Works for LC 240 too       |

4. VISUAL 1D MAPPING:
   
   Matrix (m=3, n=4):
   [[ 1,  3,  5,  7],    indices 0-3
    [10, 11, 16, 20],    indices 4-7
    [23, 30, 34, 60]]    indices 8-11
   
   Binary search range: [0, 11]
   mid = 5 → row=5//4=1, col=5%4=1 → matrix[1][1] = 11

5. WHEN TO USE WHICH:
   
   - LC 74 (this problem): Rows are connected → Single BS
   - LC 240 (Search Matrix II): Only row/col sorted → Staircase
   
   For LC 240, first element of next row is NOT > last element
   of current row, so 1D mapping doesn't work.

6. EDGE CASES:
   
   - Empty matrix
   - Single row
   - Single column
   - Target smaller than all elements
   - Target larger than all elements
   - Target between rows

7. WHY STAIRCASE WORKS (LC 240 approach):
   
   From top-right corner:
   - If current > target: nothing in this column can match
   - If current < target: nothing in this row can match
   
   Each step eliminates a row or column!

8. COMMON MISTAKES:
   
   - Using wrong index conversion formula
   - Forgetting the matrix might be empty
   - Off-by-one in boundary calculations

9. RELATED PROBLEMS:
   - Search a 2D Matrix II (LC 240) - Different constraint
   - Kth Smallest Element in Sorted Matrix (LC 378)
   - Count Negative Numbers in Sorted Matrix (LC 1351)

10. practice TIP:
    
    Start by clarifying the matrix properties:
    "So the entire matrix is globally sorted?"
    
    If yes (LC 74): Use single binary search
    If only rows/cols sorted (LC 240): Use staircase

================================================================================
"""
