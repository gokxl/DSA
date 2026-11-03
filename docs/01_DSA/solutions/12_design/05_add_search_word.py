"""
================================================================================
PROBLEM: Design Add and Search Words Data Structure (LeetCode 211)
Difficulty: Medium | Pattern: Design (Trie with Wildcards)
================================================================================

PROBLEM STATEMENT:
Design a data structure that supports adding new words and finding if a string 
matches any previously added string.

Implement the WordDictionary class:
- WordDictionary(): Initializes the object.
- void addWord(word): Adds word to the data structure, it can be matched later.
- bool search(word): Returns true if there is any string in the data structure 
  that matches word or false otherwise. word may contain dots '.' where dots 
  can be matched with any letter.

EXAMPLES:
    Input: ["WordDictionary","addWord","addWord","addWord","search","search","search","search"]
           [[],["bad"],["dad"],["mad"],["pad"],["bad"],[".ad"],["b.."]]
    Output: [null,null,null,null,false,true,true,true]

    Explanation:
    WordDictionary wordDictionary = new WordDictionary();
    wordDictionary.addWord("bad");
    wordDictionary.addWord("dad");
    wordDictionary.addWord("mad");
    wordDictionary.search("pad"); // return False
    wordDictionary.search("bad"); // return True
    wordDictionary.search(".ad"); // return True
    wordDictionary.search("b.."); // return True

CONSTRAINTS:
- 1 <= word.length <= 25
- word in addWord consists of lowercase English letters
- word in search consist of '.' or lowercase English letters
- There will be at most 2 dots in word for search queries
- At most 10^4 calls will be made to addWord and search

================================================================================
"""


# ============================================================================
# SOLUTION 1: Trie with DFS for Wildcards
# ============================================================================
class TrieNode:
    def __init__(self):
        self.children = {}  # char -> TrieNode
        self.is_word = False


class WordDictionary:
    """
    Trie for word storage.
    DFS with backtracking for '.' wildcards.
    
    addWord: O(m) where m = word length
    search: O(26^d × m) where d = number of dots
    Space: O(total characters)
    """
    
    def __init__(self):
        self.root = TrieNode()
    
    def addWord(self, word: str) -> None:
        """Add word to trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_word = True
    
    def search(self, word: str) -> bool:
        """Search with '.' as wildcard."""
        return self._dfs(word, 0, self.root)
    
    def _dfs(self, word: str, index: int, node: TrieNode) -> bool:
        """DFS search handling wildcards."""
        if index == len(word):
            return node.is_word
        
        char = word[index]
        
        if char == '.':
            # Try all children
            for child in node.children.values():
                if self._dfs(word, index + 1, child):
                    return True
            return False
        else:
            if char not in node.children:
                return False
            return self._dfs(word, index + 1, node.children[char])


# ============================================================================
# SOLUTION 2: Iterative with Stack
# ============================================================================
class WordDictionary_Iterative:
    """
    Iterative approach using stack for wildcards.
    """
    
    def __init__(self):
        self.root = TrieNode()
    
    def addWord(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_word = True
    
    def search(self, word: str) -> bool:
        # Stack: (node, index)
        stack = [(self.root, 0)]
        
        while stack:
            node, i = stack.pop()
            
            if i == len(word):
                if node.is_word:
                    return True
                continue
            
            char = word[i]
            
            if char == '.':
                for child in node.children.values():
                    stack.append((child, i + 1))
            elif char in node.children:
                stack.append((node.children[char], i + 1))
        
        return False


# ============================================================================
# SOLUTION 3: Trie with Length-Based Optimization
# ============================================================================
class WordDictionary_Optimized:
    """
    Store words by length for quick filtering.
    Useful when most searches have dots.
    """
    
    def __init__(self):
        self.root = TrieNode()
        self.words_by_length = {}  # length -> set of words
    
    def addWord(self, word: str) -> None:
        # Add to trie
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_word = True
        
        # Add to length map
        n = len(word)
        if n not in self.words_by_length:
            self.words_by_length[n] = set()
        self.words_by_length[n].add(word)
    
    def search(self, word: str) -> bool:
        n = len(word)
        
        # Quick check: any words of this length?
        if n not in self.words_by_length:
            return False
        
        # If no dots, simple lookup
        if '.' not in word:
            return word in self.words_by_length[n]
        
        # Use trie with DFS
        return self._dfs(word, 0, self.root)
    
    def _dfs(self, word: str, i: int, node: TrieNode) -> bool:
        if i == len(word):
            return node.is_word
        
        char = word[i]
        
        if char == '.':
            for child in node.children.values():
                if self._dfs(word, i + 1, child):
                    return True
            return False
        
        if char not in node.children:
            return False
        
        return self._dfs(word, i + 1, node.children[char])


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Basic operations
    print("=== Test 1: Basic Operations ===")
    wd = WordDictionary()
    wd.addWord("bad")
    wd.addWord("dad")
    wd.addWord("mad")
    
    print(f"search('pad'): {wd.search('pad')}")  # False
    print(f"search('bad'): {wd.search('bad')}")  # True
    print(f"search('.ad'): {wd.search('.ad')}")  # True
    print(f"search('b..'): {wd.search('b..')}")  # True
    print()
    
    # Test Case 2: Multiple dots
    print("=== Test 2: Multiple Dots ===")
    wd2 = WordDictionary()
    wd2.addWord("hello")
    wd2.addWord("world")
    
    print(f"search('h.ll.'): {wd2.search('h.ll.')}")  # True
    print(f"search('.....'): {wd2.search('.....')}")  # True
    print(f"search('h....'): {wd2.search('h....')}")  # True
    print(f"search('w....'): {wd2.search('w....')}")  # False (wrong length)
    print()
    
    # Test Case 3: Iterative version
    print("=== Test 3: Iterative ===")
    wd3 = WordDictionary_Iterative()
    wd3.addWord("apple")
    wd3.addWord("apply")
    
    print(f"search('appl.'): {wd3.search('appl.')}")  # True
    print(f"search('app..'): {wd3.search('app..')}")  # True
    print()
    
    # Test Case 4: Edge cases
    print("=== Test 4: Edge Cases ===")
    wd4 = WordDictionary()
    wd4.addWord("a")
    print(f"search('.'): {wd4.search('.')}")  # True
    print(f"search('..'): {wd4.search('..')}")  # False


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. TRIE + DFS FOR WILDCARDS:
   
   Regular characters: Follow trie path
   '.': Branch out to ALL children
   
   DFS handles backtracking naturally.

2. TIME COMPLEXITY:
   
   addWord: O(m) - just trie insertion
   search: O(26^d × m) worst case
   where d = number of dots, m = word length
   
   With constraint "at most 2 dots": O(26² × m) = O(m)

3. WHY DFS NOT BFS?
   
   DFS is more natural for trie traversal.
   Both work, but DFS is simpler to implement.
   
   Stack space is O(m) for word length.

4. EARLY TERMINATION:
   
   For '.', if any child path succeeds, return True.
   No need to explore all paths.

5. ALTERNATIVE: REGEX
   
   Could store words and use regex matching.
   But O(n × m) per search where n = word count.
   
   Trie is more efficient!

6. LENGTH-BASED OPTIMIZATION:
   
   Store words by length.
   Quickly eliminate impossible matches.
   
   Useful when dictionary is large.

7. COMMON MISTAKES:
   
   ❌ Not handling is_word check at end
   ❌ Returning True early without checking is_word
   ❌ Not exploring all children for '.'

8. ITERATIVE VS RECURSIVE:
   
   Recursive: Cleaner, natural for trie
   Iterative: Avoids stack overflow for long words
   
   Either is fine for practice.

9. RELATED PROBLEMS:
   
   - Implement Trie (LC 208)
   - Word Search II (LC 212)
   - Design Search Autocomplete (LC 642)

10. practice TIP:
    
    "I'll use a Trie for O(m) word insertion.
    For search with '.', I use DFS:
    
    - Regular char: Follow that child
    - '.': Try ALL children recursively
    
    Return True if we reach end of word at a node with is_word = True.
    
    Time: O(26^d × m) where d = number of dots.
    With the constraint of 2 dots max, this is effectively O(m)."

================================================================================
"""
