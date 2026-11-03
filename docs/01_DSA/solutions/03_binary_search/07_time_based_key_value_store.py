"""
================================================================================
PROBLEM: Time Based Key-Value Store (LeetCode 981)
Difficulty: Medium | Pattern: Binary Search + HashMap
================================================================================

PROBLEM STATEMENT:
Design a time-based key-value data structure that can store multiple values 
for the same key at different time stamps and retrieve the key's value at a 
certain timestamp.

Implement the TimeMap class:
- TimeMap() Initializes the object.
- void set(String key, String value, int timestamp) Stores the key with 
  the value at the given time timestamp.
- String get(String key, int timestamp) Returns a value such that set was 
  called previously, with timestamp_prev <= timestamp. If there are multiple 
  such values, it returns the value associated with the largest timestamp_prev. 
  If there are no values, it returns "".

EXAMPLES:
    Input:
    ["TimeMap", "set", "get", "get", "set", "get", "get"]
    [[], ["foo", "bar", 1], ["foo", 1], ["foo", 3], ["foo", "bar2", 4], ["foo", 4], ["foo", 5]]
    
    Output: [null, null, "bar", "bar", null, "bar2", "bar2"]
    
    Explanation:
    TimeMap timeMap = new TimeMap();
    timeMap.set("foo", "bar", 1);  // store "foo":"bar" at timestamp 1
    timeMap.get("foo", 1);         // return "bar"
    timeMap.get("foo", 3);         // return "bar" (largest timestamp <= 3 is 1)
    timeMap.set("foo", "bar2", 4); // store "foo":"bar2" at timestamp 4
    timeMap.get("foo", 4);         // return "bar2"
    timeMap.get("foo", 5);         // return "bar2"

CONSTRAINTS:
- 1 <= key.length, value.length <= 100
- key and value consist of lowercase English letters and digits
- 1 <= timestamp <= 10^7
- All timestamps of set are strictly increasing for the same key
- At most 2 * 10^5 calls to set and get

================================================================================
"""

import bisect
from collections import defaultdict
from typing import List


# ============================================================================
# SOLUTION 1: HashMap + Binary Search (Using bisect)
# ============================================================================
class TimeMap:
    """
    Store values with timestamps in a list.
    Use binary search to find the latest timestamp <= query timestamp.
    
    Since timestamps are strictly increasing for each key, the list is 
    always sorted, so we can use binary search.
    
    Time: set O(1), get O(log n)
    Space: O(n) for all stored values
    """
    
    def __init__(self):
        # key -> list of (timestamp, value) pairs
        self.store = defaultdict(list)
    
    def set(self, key: str, value: str, timestamp: int) -> None:
        # Timestamps are strictly increasing, so just append
        self.store[key].append((timestamp, value))
    
    def get(self, key: str, timestamp: int) -> str:
        if key not in self.store:
            return ""
        
        values = self.store[key]
        
        # Binary search for largest timestamp <= given timestamp
        # bisect_right gives us the insertion point for timestamp
        # We want the element just before that
        idx = bisect.bisect_right(values, (timestamp, chr(127)))
        
        if idx == 0:
            return ""  # All timestamps are larger
        
        return values[idx - 1][1]


# ============================================================================
# SOLUTION 2: Manual Binary Search
# ============================================================================
class TimeMap2:
    """
    Same approach but with manual binary search implementation.
    
    Time: set O(1), get O(log n)
    Space: O(n)
    """
    
    def __init__(self):
        self.store = defaultdict(list)
    
    def set(self, key: str, value: str, timestamp: int) -> None:
        self.store[key].append((timestamp, value))
    
    def get(self, key: str, timestamp: int) -> str:
        if key not in self.store:
            return ""
        
        values = self.store[key]
        
        # Binary search: find largest timestamp <= given timestamp
        left, right = 0, len(values) - 1
        result = ""
        
        while left <= right:
            mid = left + (right - left) // 2
            
            if values[mid][0] <= timestamp:
                # This timestamp is valid, store and look for larger
                result = values[mid][1]
                left = mid + 1
            else:
                # This timestamp is too large
                right = mid - 1
        
        return result


# ============================================================================
# SOLUTION 3: Separate Lists for Timestamps and Values
# ============================================================================
class TimeMap3:
    """
    Store timestamps and values in separate lists.
    Slightly more memory efficient for bisect.
    
    Time: set O(1), get O(log n)
    Space: O(n)
    """
    
    def __init__(self):
        # key -> {'times': [...], 'values': [...]}
        self.store = defaultdict(lambda: {'times': [], 'values': []})
    
    def set(self, key: str, value: str, timestamp: int) -> None:
        self.store[key]['times'].append(timestamp)
        self.store[key]['values'].append(value)
    
    def get(self, key: str, timestamp: int) -> str:
        if key not in self.store:
            return ""
        
        times = self.store[key]['times']
        values = self.store[key]['values']
        
        # bisect_right finds where timestamp would be inserted
        idx = bisect.bisect_right(times, timestamp)
        
        if idx == 0:
            return ""
        
        return values[idx - 1]


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Basic operations
    print("Testing TimeMap (bisect):")
    timeMap = TimeMap()
    timeMap.set("foo", "bar", 1)
    print(f"get('foo', 1) = '{timeMap.get('foo', 1)}'")   # "bar"
    print(f"get('foo', 3) = '{timeMap.get('foo', 3)}'")   # "bar"
    timeMap.set("foo", "bar2", 4)
    print(f"get('foo', 4) = '{timeMap.get('foo', 4)}'")   # "bar2"
    print(f"get('foo', 5) = '{timeMap.get('foo', 5)}'")   # "bar2"
    print()
    
    # Test Case 2: Timestamp before first set
    print("Testing edge case - timestamp before first:")
    timeMap2 = TimeMap2()
    timeMap2.set("key", "value", 10)
    print(f"get('key', 5) = '{timeMap2.get('key', 5)}'")   # ""
    print(f"get('key', 10) = '{timeMap2.get('key', 10)}'")  # "value"
    print(f"get('key', 15) = '{timeMap2.get('key', 15)}'")  # "value"
    print()
    
    # Test Case 3: Key doesn't exist
    print("Testing non-existent key:")
    print(f"get('nonexistent', 1) = '{timeMap.get('nonexistent', 1)}'")  # ""
    print()
    
    # Test Case 4: Multiple values for same key
    print("Testing multiple timestamps:")
    timeMap3 = TimeMap3()
    timeMap3.set("x", "a", 1)
    timeMap3.set("x", "b", 5)
    timeMap3.set("x", "c", 10)
    print(f"get('x', 0) = '{timeMap3.get('x', 0)}'")    # ""
    print(f"get('x', 1) = '{timeMap3.get('x', 1)}'")    # "a"
    print(f"get('x', 3) = '{timeMap3.get('x', 3)}'")    # "a"
    print(f"get('x', 5) = '{timeMap3.get('x', 5)}'")    # "b"
    print(f"get('x', 7) = '{timeMap3.get('x', 7)}'")    # "b"
    print(f"get('x', 10) = '{timeMap3.get('x', 10)}'")  # "c"
    print(f"get('x', 100) = '{timeMap3.get('x', 100)}'")  # "c"


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. KEY OBSERVATION:
   
   "All timestamps of set are strictly increasing for the same key"
   
   This means we don't need to sort! Just append.
   The list is always sorted by timestamp.

2. THE SEARCH PROBLEM:
   
   "Find largest timestamp_prev <= timestamp"
   
   This is a classic UPPER BOUND - 1 or "floor" operation.
   Binary search to find the rightmost element <= target.

3. USING BISECT:
   
   bisect_right(arr, x) → First position where element > x
   
   For timestamps:
   idx = bisect_right(times, timestamp)
   if idx > 0:
       return values[idx - 1]
   
   For (timestamp, value) pairs:
   # Use chr(127) as max character to ensure we find correct position
   idx = bisect_right(pairs, (timestamp, chr(127)))

4. DATA STRUCTURE CHOICE:
   
   HashMap + List is perfect because:
   - O(1) key lookup
   - O(1) append (timestamps increasing)
   - O(log n) binary search

5. VISUAL EXAMPLE:
   
   set("foo", "bar", 1)
   set("foo", "bar2", 4)
   set("foo", "bar3", 7)
   
   store["foo"] = [(1, "bar"), (4, "bar2"), (7, "bar3")]
   
   get("foo", 5):
   - Binary search for largest timestamp <= 5
   - (4, "bar2") is the answer

6. COMMON MISTAKES:
   
   - Forgetting the chr(127) trick with bisect on tuples
   - Off-by-one after bisect_right
   - Not handling empty/missing key

7. FOLLOW-UP QUESTIONS:
   
   Q: What if timestamps are NOT strictly increasing?
   A: Need to maintain sorted order:
      - Binary search for insertion point
      - Insert at correct position O(n)
      - Or use a balanced BST for O(log n) insert
   
   Q: What about deleting values?
   A: Mark as deleted or use a more complex structure

8. TIME COMPLEXITY:
   
   - set: O(1) amortized (list append)
   - get: O(log n) where n = number of timestamps for key
   - Space: O(total number of set calls)

9. REAL-WORLD APPLICATIONS:
   
   - Version control systems
   - Database temporal queries
   - Cache with TTL
   - Event sourcing

10. ALTERNATIVE DATA STRUCTURES:
    
    - TreeMap (Java): O(log n) for both operations
    - SortedDict (Python): Same as TreeMap
    - Skip List: O(log n) average
    
    For strictly increasing timestamps, HashMap + List is optimal.

================================================================================
"""
