r"""
================================================================================
PROBLEM: Course Schedule I & II (LeetCode 207 & 210)
Difficulty: Medium | Pattern: Topological Sort
================================================================================

PROBLEM STATEMENT (LC 207 - Course Schedule):
There are numCourses courses labeled from 0 to numCourses - 1. You are given 
an array prerequisites where prerequisites[i] = [ai, bi] indicates that you 
must take course bi first if you want to take course ai.

Return true if you can finish all courses, otherwise return false.

PROBLEM STATEMENT (LC 210 - Course Schedule II):
Return the ordering of courses you should take to finish all courses.
If there are many valid answers, return any of them.
If it is impossible to finish all courses, return an empty array.

EXAMPLES:
    Input: numCourses = 2, prerequisites = [[1,0]]
    Output (LC 207): true
    Output (LC 210): [0,1]
    Explanation: Take course 0 first, then course 1.

    Input: numCourses = 2, prerequisites = [[1,0],[0,1]]
    Output (LC 207): false
    Output (LC 210): []
    Explanation: Cycle exists, can't complete all courses.

    Input: numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]
    Output (LC 207): true
    Output (LC 210): [0,1,2,3] or [0,2,1,3]
    
           0
          / \
         1   2
          \ /
           3

CONSTRAINTS:
- 1 <= numCourses <= 2000
- 0 <= prerequisites.length <= 5000
- prerequisites[i].length == 2
- 0 <= ai, bi < numCourses
- All pairs are unique

================================================================================
"""
from typing import List
from collections import deque, defaultdict


# ============================================================================
# SOLUTION 1: BFS (Kahn's Algorithm) - Recommended
# ============================================================================
def canFinish_bfs(numCourses: int, prerequisites: List[List[int]]) -> bool:
    """
    Kahn's Algorithm for topological sort using BFS.
    
    1. Calculate in-degree for each node
    2. Start with nodes having in-degree 0
    3. Process and reduce neighbors' in-degrees
    4. If all nodes processed, no cycle exists
    
    Time: O(V + E)
    Space: O(V + E)
    """
    # Build graph and in-degree array
    graph = defaultdict(list)
    in_degree = [0] * numCourses
    
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1
    
    # Start with courses having no prerequisites
    queue = deque([i for i in range(numCourses) if in_degree[i] == 0])
    completed = 0
    
    while queue:
        course = queue.popleft()
        completed += 1
        
        for next_course in graph[course]:
            in_degree[next_course] -= 1
            if in_degree[next_course] == 0:
                queue.append(next_course)
    
    return completed == numCourses


def findOrder_bfs(numCourses: int, prerequisites: List[List[int]]) -> List[int]:
    """
    Same Kahn's algorithm but return the ordering.
    
    Time: O(V + E)
    Space: O(V + E)
    """
    graph = defaultdict(list)
    in_degree = [0] * numCourses
    
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1
    
    queue = deque([i for i in range(numCourses) if in_degree[i] == 0])
    order = []
    
    while queue:
        course = queue.popleft()
        order.append(course)
        
        for next_course in graph[course]:
            in_degree[next_course] -= 1
            if in_degree[next_course] == 0:
                queue.append(next_course)
    
    return order if len(order) == numCourses else []


# ============================================================================
# SOLUTION 2: DFS with Cycle Detection
# ============================================================================
def canFinish_dfs(numCourses: int, prerequisites: List[List[int]]) -> bool:
    """
    DFS approach with three states:
    - 0: not visited
    - 1: visiting (in current DFS path)
    - 2: visited (completed)
    
    If we encounter state 1 during DFS, cycle exists!
    
    Time: O(V + E)
    Space: O(V + E)
    """
    graph = defaultdict(list)
    for course, prereq in prerequisites:
        graph[prereq].append(course)
    
    # 0: not visited, 1: visiting, 2: visited
    state = [0] * numCourses
    
    def has_cycle(course: int) -> bool:
        if state[course] == 1:
            return True  # Back edge = cycle
        if state[course] == 2:
            return False  # Already processed
        
        state[course] = 1  # Mark as visiting
        
        for next_course in graph[course]:
            if has_cycle(next_course):
                return True
        
        state[course] = 2  # Mark as visited
        return False
    
    for course in range(numCourses):
        if has_cycle(course):
            return False
    
    return True


def findOrder_dfs(numCourses: int, prerequisites: List[List[int]]) -> List[int]:
    """
    DFS approach returning order.
    Build order in reverse (post-order).
    
    Time: O(V + E)
    Space: O(V + E)
    """
    graph = defaultdict(list)
    for course, prereq in prerequisites:
        graph[prereq].append(course)
    
    state = [0] * numCourses
    order = []
    has_cycle = False
    
    def dfs(course: int) -> None:
        nonlocal has_cycle
        
        if state[course] == 1:
            has_cycle = True
            return
        if state[course] == 2:
            return
        
        state[course] = 1
        
        for next_course in graph[course]:
            dfs(next_course)
            if has_cycle:
                return
        
        state[course] = 2
        order.append(course)  # Add after processing all descendants
    
    for course in range(numCourses):
        if state[course] == 0:
            dfs(course)
            if has_cycle:
                return []
    
    return order[::-1]  # Reverse for correct order


# ============================================================================
# SOLUTION 3: DFS returning order directly (cleaner)
# ============================================================================
def findOrder_clean(numCourses: int, prerequisites: List[List[int]]) -> List[int]:
    """
    Cleaner DFS implementation.
    
    Time: O(V + E)
    Space: O(V + E)
    """
    graph = defaultdict(list)
    for course, prereq in prerequisites:
        graph[course].append(prereq)  # Reversed! course depends on prereq
    
    visited = set()
    path = set()  # Current DFS path for cycle detection
    result = []
    
    def dfs(course: int) -> bool:
        """Returns False if cycle detected"""
        if course in path:
            return False  # Cycle!
        if course in visited:
            return True  # Already processed
        
        path.add(course)
        
        for prereq in graph[course]:
            if not dfs(prereq):
                return False
        
        path.remove(course)
        visited.add(course)
        result.append(course)
        
        return True
    
    for course in range(numCourses):
        if not dfs(course):
            return []
    
    return result


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Simple dependency
    print("Test 1: numCourses=2, prerequisites=[[1,0]]")
    print(f"Can finish (BFS): {canFinish_bfs(2, [[1, 0]])}")  # True
    print(f"Order (BFS): {findOrder_bfs(2, [[1, 0]])}")  # [0, 1]
    print()
    
    # Test Case 2: Cycle exists
    print("Test 2: numCourses=2, prerequisites=[[1,0],[0,1]]")
    print(f"Can finish (DFS): {canFinish_dfs(2, [[1, 0], [0, 1]])}")  # False
    print(f"Order (DFS): {findOrder_dfs(2, [[1, 0], [0, 1]])}")  # []
    print()
    
    # Test Case 3: Diamond dependency
    print("Test 3: numCourses=4, prerequisites=[[1,0],[2,0],[3,1],[3,2]]")
    print(f"Can finish: {canFinish_bfs(4, [[1, 0], [2, 0], [3, 1], [3, 2]])}")  # True
    print(f"Order: {findOrder_bfs(4, [[1, 0], [2, 0], [3, 1], [3, 2]])}")  # [0,1,2,3] or [0,2,1,3]
    print()
    
    # Test Case 4: No prerequisites
    print("Test 4: numCourses=3, prerequisites=[]")
    print(f"Can finish: {canFinish_bfs(3, [])}")  # True
    print(f"Order: {findOrder_bfs(3, [])}")  # [0,1,2] or any order
    print()
    
    # Test Case 5: Complex case
    prereqs = [[1, 0], [2, 0], [3, 1], [3, 2], [4, 3], [5, 3]]
    print(f"Test 5: Complex dependency")
    print(f"Order (clean DFS): {findOrder_clean(6, prereqs)}")


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. THIS IS TOPOLOGICAL SORT:
   
   Topological sort = ordering where for every edge (u→v), u comes before v
   
   Only possible for DAG (Directed Acyclic Graph)
   Cycle = impossible to complete all courses

2. TWO APPROACHES - KAHN'S (BFS) VS DFS:
   
   Kahn's (BFS):
   - Use in-degree array
   - Start with in-degree 0 nodes
   - More intuitive for most
   
   DFS:
   - Use 3-state marking (not visited, visiting, visited)
   - Post-order gives reverse topological order
   - "Visiting" state detects back edges (cycles)

3. GRAPH DIRECTION MATTERS:
   
   [course, prereq] means prereq → course
   
   For Kahn's: Build prereq → course graph
   For DFS ordering: Can build course → prereq (reversed)

4. DETECTING CYCLES:
   
   Kahn's: completed count < numCourses → cycle exists
   DFS: Encounter "visiting" state → back edge → cycle

5. WHY 3 STATES IN DFS?
   
   - Not visited (0): Haven't seen this node
   - Visiting (1): In current DFS path - if seen again = CYCLE
   - Visited (2): Completely processed and done
   
   The "visiting" state is KEY for cycle detection!

6. POST-ORDER FOR TOPOLOGICAL SORT:
   
   In DFS, add to result AFTER processing all descendants:
   
   dfs(neighbors)
   result.append(node)  # Post-order
   
   Then reverse the result.

7. COMMON APPLICATIONS:
   
   - Build systems (dependency resolution)
   - Task scheduling
   - College course planning
   - Package installation

8. COMMON MISTAKES:
   
   ❌ Wrong graph direction
   ❌ DFS: Only using 2 states (can't detect all cycles)
   ❌ DFS: Not reversing the result

9. FOLLOW-UP: PARALLEL COURSES (LC 1136)
   
   "What's minimum semesters to finish all courses?"
   Use BFS, track levels. Answer = number of BFS levels.

10. HOW TO EXPLAIN IT:
    
    Start with Kahn's algorithm (more intuitive):
    
    "I'll use Kahn's algorithm - BFS-based topological sort.
    Start with courses having no prerequisites (in-degree 0),
    process them, reduce neighbors' in-degrees, repeat.
    If I process all courses, no cycle. Otherwise cycle exists."
    
    Know DFS approach too for follow-up questions!

================================================================================
"""
