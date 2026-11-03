"""
================================================================================
PROBLEM: Implement Trie (Prefix Tree) (LeetCode 208)
Difficulty: Medium | Pattern: Design (Trie)
================================================================================

PROBLEM STATEMENT:
A trie (pronounced as "try") or prefix tree is a tree data structure used to 
efficiently store and retrieve keys in a dataset of strings. There are various 
applications of this data structure, such as autocomplete and spellchecker.

Implement the Trie class:
- Trie(): Initializes the trie object.
- void insert(String word): Inserts the string word into the trie.
- boolean search(String word): Returns true if the string word is in the trie 
  (i.e., was inserted before), and false otherwise.
- boolean startsWith(String prefix): Returns true if there is a previously 
  inserted string word that has the prefix prefix, and false otherwise.

EXAMPLES:
    Input: ["Trie", "insert", "search", "search", "startsWith", "insert", "search"]
           [[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]]
    Output: [null, null, true, false, true, null, true]

CONSTRAINTS:
- 1 <= word.length, prefix.length <= 2000
- word and prefix consist only of lowercase English letters
- At most 3 * 10^4 calls will be made to insert, search, and startsWith

================================================================================
"""


# ============================================================================
# SOLUTION 1: Trie with Dictionary Children
# ============================================================================
class TrieNode:
    def __init__(self):
        self.children = {}  # char -> TrieNode
        self.is_end = False  # Marks end of word


class Trie:
    """
    Trie using dictionary for children.
    Flexible for any character set.
    
    Time: O(m) for insert, search, startsWith where m = word length
    Space: O(ALPHABET_SIZE × n × m) worst case
    """
    
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word: str) -> None:
        """Insert word into trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
    
    def search(self, word: str) -> bool:
        """Return True if word exists in trie."""
        node = self._find_node(word)
        return node is not None and node.is_end
    
    def startsWith(self, prefix: str) -> bool:
        """Return True if any word starts with prefix."""
        return self._find_node(prefix) is not None
    
    def _find_node(self, prefix: str) -> TrieNode:
        """Find node corresponding to prefix."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node


# ============================================================================
# SOLUTION 2: Trie with Array Children (26 letters)
# ============================================================================
class TrieNode_Array:
    def __init__(self):
        self.children = [None] * 26  # For a-z
        self.is_end = False


class Trie_Array:
    """
    Trie using fixed array for children.
    Slightly faster access but uses more memory.
    
    Time: O(m)
    Space: O(26 × n × m) worst case
    """
    
    def __init__(self):
        self.root = TrieNode_Array()
    
    def _char_to_index(self, char: str) -> int:
        return ord(char) - ord('a')
    
    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            idx = self._char_to_index(char)
            if node.children[idx] is None:
                node.children[idx] = TrieNode_Array()
            node = node.children[idx]
        node.is_end = True
    
    def search(self, word: str) -> bool:
        node = self._find_node(word)
        return node is not None and node.is_end
    
    def startsWith(self, prefix: str) -> bool:
        return self._find_node(prefix) is not None
    
    def _find_node(self, prefix: str):
        node = self.root
        for char in prefix:
            idx = self._char_to_index(char)
            if node.children[idx] is None:
                return None
            node = node.children[idx]
        return node


# ============================================================================
# SOLUTION 3: Trie with Additional Features
# ============================================================================
class Trie_Extended:
    """
    Extended Trie with additional useful methods:
    - delete
    - count words with prefix
    - get all words with prefix (autocomplete)
    """
    
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
    
    def search(self, word: str) -> bool:
        node = self._find_node(word)
        return node is not None and node.is_end
    
    def startsWith(self, prefix: str) -> bool:
        return self._find_node(prefix) is not None
    
    def _find_node(self, prefix: str) -> TrieNode:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node
    
    def delete(self, word: str) -> bool:
        """Delete word from trie. Returns True if word existed."""
        def _delete(node: TrieNode, word: str, depth: int) -> bool:
            if depth == len(word):
                if not node.is_end:
                    return False
                node.is_end = False
                return len(node.children) == 0
            
            char = word[depth]
            if char not in node.children:
                return False
            
            should_delete = _delete(node.children[char], word, depth + 1)
            
            if should_delete:
                del node.children[char]
                return len(node.children) == 0 and not node.is_end
            
            return False
        
        return _delete(self.root, word, 0)
    
    def get_words_with_prefix(self, prefix: str) -> list:
        """Get all words starting with prefix (autocomplete)."""
        results = []
        node = self._find_node(prefix)
        
        if node is None:
            return results
        
        def dfs(node: TrieNode, path: str):
            if node.is_end:
                results.append(path)
            for char, child in node.children.items():
                dfs(child, path + char)
        
        dfs(node, prefix)
        return results
    
    def count_words_with_prefix(self, prefix: str) -> int:
        """Count words starting with prefix."""
        node = self._find_node(prefix)
        
        if node is None:
            return 0
        
        def count(node: TrieNode) -> int:
            total = 1 if node.is_end else 0
            for child in node.children.values():
                total += count(child)
            return total
        
        return count(node)


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Basic operations
    print("=== Test 1: Basic Operations ===")
    trie = Trie()
    trie.insert("apple")
    print(f"search('apple'): {trie.search('apple')}")  # True
    print(f"search('app'): {trie.search('app')}")  # False
    print(f"startsWith('app'): {trie.startsWith('app')}")  # True
    trie.insert("app")
    print(f"search('app'): {trie.search('app')}")  # True
    print()
    
    # Test Case 2: Array-based Trie
    print("=== Test 2: Array-based ===")
    trie2 = Trie_Array()
    trie2.insert("hello")
    trie2.insert("help")
    print(f"search('hello'): {trie2.search('hello')}")  # True
    print(f"search('hel'): {trie2.search('hel')}")  # False
    print(f"startsWith('hel'): {trie2.startsWith('hel')}")  # True
    print()
    
    # Test Case 3: Extended Trie
    print("=== Test 3: Extended Trie ===")
    trie3 = Trie_Extended()
    words = ["apple", "app", "application", "apply", "banana"]
    for word in words:
        trie3.insert(word)
    
    print(f"Words with 'app': {trie3.get_words_with_prefix('app')}")
    print(f"Count with 'app': {trie3.count_words_with_prefix('app')}")
    
    trie3.delete("app")
    print(f"After deleting 'app': {trie3.get_words_with_prefix('app')}")


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. TRIE STRUCTURE:
   
   Each node has:
   - children: map from character to child node
   - is_end: marks if a word ends here
   
   Root represents empty string.

2. TIME COMPLEXITY:
   
   insert(word): O(m) where m = word length
   search(word): O(m)
   startsWith(prefix): O(m)
   
   All operations are proportional to string length.

3. SPACE COMPLEXITY:
   
   Worst case: O(ALPHABET_SIZE × N × M)
   where N = number of words, M = average length
   
   Best case: shared prefixes save space!

4. DICT VS ARRAY CHILDREN:
   
   Dictionary: Flexible, space-efficient for sparse data
   Array [26]: Faster access, fixed memory per node
   
   Use dict for practice unless told otherwise.

5. COMMON OPERATIONS:
   
   - Insert: Create nodes for each character
   - Search: Navigate nodes, check is_end
   - StartsWith: Navigate nodes, just check existence
   - Delete: Recursive removal, clean up empty nodes
   - Autocomplete: DFS from prefix node

6. USE CASES:
   
   - Autocomplete / Type-ahead
   - Spell checker
   - IP routing (longest prefix match)
   - Word games (Boggle, Scrabble)
   - Searching by prefix

7. TRIE VS HASHSET:
   
   HashSet: O(m) insert/search, no prefix queries
   Trie: O(m) insert/search, O(p + n) prefix queries
   
   Trie wins for prefix-based problems!

8. COMMON MISTAKES:
   
   ❌ Forgetting is_end flag
   ❌ Not returning False in search when path exists but is_end is False
   ❌ Confusing search vs startsWith

9. RELATED PROBLEMS:
   
   - Add and Search Word (LC 211) - with wildcards
   - Word Search II (LC 212) - Trie + backtracking
   - Replace Words (LC 648)
   - Design Search Autocomplete (LC 642)

10. practice TIP:
    
    "Trie is a tree where each node represents a character.
    The path from root to any node spells a prefix.
    
    Each node has:
    - children (dict of char → node)
    - is_end (marks complete words)
    
    Insert: Create path, set is_end at end.
    Search: Follow path, check is_end.
    StartsWith: Follow path, check existence.
    
    Time is O(m) for word of length m."
    
    Mention autocomplete use case!

================================================================================
"""
