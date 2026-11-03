# Common Mistakes to Avoid

Learn from others' failures. Don't repeat these in your practice.

---

## Top 10 practice Killers

### 1. Starting to Code Too Fast

**Mistake:** Jump into coding without clarifying requirements  
**Result:** Solve wrong problem, waste time, look unprepared

**Fix:**
- "Before I start coding, let me make sure I understand..."
- "What should I return if the input is empty?"
- "Can there be negative numbers?"
- Spend 3-5 minutes clarifying BEFORE touching keyboard

---

### 2. Not Explaining Your Approach First

**Mistake:** Start coding silently without explaining the algorithm  
**Result:** Interviewer can't help if you're going wrong direction

**Fix:**
- "My approach will be..."
- "I'll use [pattern] because [reason]"
- "Does this approach make sense before I code?"
- Always get verbal approval before coding

---

### 3. Off-By-One Errors

**Mistake:** Wrong loop bounds, wrong index calculations  
**Result:** Code fails on edge cases, debugging wastes time

**Common situations:**
```python
# WRONG
for i in range(n):       # Does this include n?
while left <= right:     # When to use < vs <=?
arr[n]                   # Index out of bounds!

# FIX: Trace through with small example
# n=3: indices are 0, 1, 2 (not 3!)
```

---

### 4. Forgetting Edge Cases

**Mistake:** Code works for normal cases, fails on edges  
**Result:** Shows lack of thoroughness

**Always check:**
- Empty input ([], "", None)
- Single element
- Two elements
- All same elements
- Negative numbers
- Zero
- Already sorted / reverse sorted
- Duplicates

---

### 5. Not Testing Your Code

**Mistake:** Say "I think this works" without tracing through  
**Result:** Bugs you could have caught

**Fix:** After coding, always:
1. Trace through with given example
2. Trace through with edge case
3. Check loop bounds

---

### 6. Silence

**Mistake:** Code silently for 5+ minutes  
**Result:** Interviewer can't assess your thinking or help

**Fix:**
- "I'm thinking about how to handle..."
- "The tricky part here is..."
- "I'm stuck on [X], could I get a hint?"
- Never be silent for more than 30 seconds

---

### 7. Getting Stuck and Panicking

**Mistake:** Freeze when approach doesn't work  
**Result:** Wasted time, poor impression

**Recovery strategy:**
1. "Let me reconsider the approach"
2. "What if the input was just 2 elements?"
3. "What pattern might this be?"
4. "Could I get a small hint on direction?"

Asking for hints is OK. Giving up is not.

---

### 8. Overcomplicating the Solution

**Mistake:** Use complex algorithm when simple one works  
**Result:** More bugs, harder to debug

**Signs you're overcomplicating:**
- Using recursion when iteration is simpler
- Using DP when greedy works
- Adding unnecessary data structures
- Handling edge cases with complex logic

Always start with brute force, then optimize.

---

### 9. Not Knowing Time/Space Complexity

**Mistake:** Can't explain complexity when asked  
**Result:** Shows lack of CS fundamentals

**Fix:** After coding, immediately say:
- "The time complexity is O(n) because we iterate once through the array."
- "The space complexity is O(n) for the HashMap in the worst case."

---

### 10. Poor Code Quality

**Mistake:** Messy variable names, no structure  
**Result:** Harder to debug, shows lack of experience

**Bad:**
```python
def f(a, t):
    d = {}
    for i, x in enumerate(a):
        if t - x in d:
            return [d[t-x], i]
        d[x] = i
```

**Good:**
```python
def twoSum(nums, target):
    seen = {}  # value -> index
    
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    
    return []
```

---

## Pattern-Specific Mistakes

| Pattern | Mistake | Fix |
|---------|---------|-----|
| Two Pointers | Not skipping duplicates | `while left < right and nums[left] == nums[left-1]` |
| Sliding Window | Not shrinking window | `while invalid: left += 1` |
| Binary Search | Infinite loop | Use `left = mid + 1` or `right = mid - 1` |
| Trees | No base case | Always check `if not node: return` |
| Graphs | No visited check | `if node in visited: continue` |
| DP | Wrong base case | Think: smallest subproblem? |
| Backtracking | Not making a copy | `result.append(path[:])` |

---

## Checklists

### Before Coding

- [ ] Did I clarify the input format?
- [ ] Did I clarify the output format?
- [ ] Did I ask about edge cases?
- [ ] Did I explain my approach?
- [ ] Did I get verbal approval?

### After Coding

- [ ] Did I trace through with the given example?
- [ ] Did I test with an edge case?
- [ ] Did I check loop bounds?
- [ ] Did I state time and space complexity?

---

## Useful Phrases

**When starting:**
- "Before I start, let me clarify a few things..."
- "I'll first describe my approach, then code it."

**When stuck:**
- "Let me take a step back and think about this differently."
- "I'm not seeing the optimal solution yet. Could I get a hint on the pattern?"

**When debugging:**
- "Let me trace through with a small example..."
- "Oh, I see the issue - [explain]. Let me fix that."

**When finished:**
- "The time complexity is O(n) because..."
- "The space complexity is O(n) because..."

---

Read this before every practice session. Read this before practice sessions.
