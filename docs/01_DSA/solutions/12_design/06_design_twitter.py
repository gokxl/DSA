"""
================================================================================
PROBLEM: Design Twitter (LeetCode 355)
Difficulty: Medium | Pattern: Design (OOP + Heap)
================================================================================

PROBLEM STATEMENT:
Design a simplified version of Twitter where users can post tweets, 
follow/unfollow another user, and is able to see the 10 most recent tweets 
in the user's news feed.

Implement the Twitter class:
- Twitter(): Initializes your twitter object.
- void postTweet(int userId, int tweetId): Composes a new tweet with ID tweetId 
  by the user userId. Each call to this function will be made with a unique tweetId.
- List<Integer> getNewsFeed(int userId): Retrieves the 10 most recent tweet IDs 
  in the user's news feed. Each item in the news feed must be posted by users 
  who the user followed or by the user themself. Tweets must be ordered from 
  most recent to least recent.
- void follow(int followerId, int followeeId): The user with ID followerId 
  started following the user with ID followeeId.
- void unfollow(int followerId, int followeeId): The user with ID followerId 
  stopped following the user with ID followeeId.

EXAMPLES:
    Input: ["Twitter", "postTweet", "getNewsFeed", "follow", "getNewsFeed", "unfollow", "getNewsFeed"]
           [[], [1, 5], [1], [1, 2], [1], [1, 2], [1]]
    Output: [null, null, [5], null, [5, 6], null, [5]]

CONSTRAINTS:
- 1 <= userId, followerId, followeeId <= 500
- 0 <= tweetId <= 10^4
- All the tweets have unique IDs
- At most 3 * 10^4 calls will be made to postTweet, getNewsFeed, follow, unfollow

================================================================================
"""
from typing import List
from collections import defaultdict
import heapq


# ============================================================================
# SOLUTION 1: HashMap + Heap (Standard)
# ============================================================================
class Twitter:
    """
    Design using:
    - HashMap for user -> tweets
    - HashMap for user -> followees
    - Heap for merging news feed
    
    postTweet: O(1)
    getNewsFeed: O(k log n) where k = 10, n = followees
    follow/unfollow: O(1)
    """
    
    def __init__(self):
        self.timestamp = 0
        self.user_tweets = defaultdict(list)  # userId -> [(timestamp, tweetId), ...]
        self.followees = defaultdict(set)     # userId -> set of followeeIds
    
    def postTweet(self, userId: int, tweetId: int) -> None:
        """Post a new tweet."""
        self.user_tweets[userId].append((self.timestamp, tweetId))
        self.timestamp += 1
    
    def getNewsFeed(self, userId: int) -> List[int]:
        """Get 10 most recent tweets from user and followees."""
        # Get all users to fetch tweets from (self + followees)
        users = self.followees[userId] | {userId}
        
        # Use max heap to get most recent
        # Store (-timestamp, tweetId, userId, index)
        heap = []
        
        for uid in users:
            tweets = self.user_tweets[uid]
            if tweets:
                idx = len(tweets) - 1  # Start from most recent
                ts, tid = tweets[idx]
                heapq.heappush(heap, (-ts, tid, uid, idx))
        
        result = []
        
        while heap and len(result) < 10:
            neg_ts, tweet_id, uid, idx = heapq.heappop(heap)
            result.append(tweet_id)
            
            # Add next tweet from same user
            if idx > 0:
                idx -= 1
                ts, tid = self.user_tweets[uid][idx]
                heapq.heappush(heap, (-ts, tid, uid, idx))
        
        return result
    
    def follow(self, followerId: int, followeeId: int) -> None:
        """User followerId follows followeeId."""
        if followerId != followeeId:  # Can't follow yourself
            self.followees[followerId].add(followeeId)
    
    def unfollow(self, followerId: int, followeeId: int) -> None:
        """User followerId unfollows followeeId."""
        self.followees[followerId].discard(followeeId)


# ============================================================================
# SOLUTION 2: Simple approach (collect all, sort)
# ============================================================================
class Twitter_Simple:
    """
    Simpler but less efficient: collect all tweets, sort.
    
    getNewsFeed: O(t log t) where t = total tweets from followees
    """
    
    def __init__(self):
        self.timestamp = 0
        self.user_tweets = defaultdict(list)
        self.followees = defaultdict(set)
    
    def postTweet(self, userId: int, tweetId: int) -> None:
        self.user_tweets[userId].append((self.timestamp, tweetId))
        self.timestamp += 1
    
    def getNewsFeed(self, userId: int) -> List[int]:
        users = self.followees[userId] | {userId}
        
        # Collect all tweets
        all_tweets = []
        for uid in users:
            all_tweets.extend(self.user_tweets[uid])
        
        # Sort by timestamp descending, take top 10
        all_tweets.sort(reverse=True, key=lambda x: x[0])
        
        return [tid for _, tid in all_tweets[:10]]
    
    def follow(self, followerId: int, followeeId: int) -> None:
        if followerId != followeeId:
            self.followees[followerId].add(followeeId)
    
    def unfollow(self, followerId: int, followeeId: int) -> None:
        self.followees[followerId].discard(followeeId)


# ============================================================================
# SOLUTION 3: OOP with Tweet and User classes
# ============================================================================
class Tweet:
    def __init__(self, tweet_id: int, timestamp: int):
        self.id = tweet_id
        self.timestamp = timestamp
        self.next = None  # For linked list of tweets


class User:
    def __init__(self, user_id: int):
        self.id = user_id
        self.followees = set()
        self.tweet_head = None  # Most recent tweet
    
    def follow(self, followee_id: int):
        if followee_id != self.id:
            self.followees.add(followee_id)
    
    def unfollow(self, followee_id: int):
        self.followees.discard(followee_id)
    
    def post(self, tweet_id: int, timestamp: int):
        tweet = Tweet(tweet_id, timestamp)
        tweet.next = self.tweet_head
        self.tweet_head = tweet


class Twitter_OOP:
    """
    Object-oriented design with Tweet and User classes.
    Uses linked list for user tweets.
    """
    
    def __init__(self):
        self.timestamp = 0
        self.users = {}  # userId -> User
    
    def _get_user(self, user_id: int) -> User:
        if user_id not in self.users:
            self.users[user_id] = User(user_id)
        return self.users[user_id]
    
    def postTweet(self, userId: int, tweetId: int) -> None:
        user = self._get_user(userId)
        user.post(tweetId, self.timestamp)
        self.timestamp += 1
    
    def getNewsFeed(self, userId: int) -> List[int]:
        user = self._get_user(userId)
        
        # Get all users to fetch from
        user_ids = user.followees | {userId}
        
        # Max heap with (-timestamp, tweet_id, tweet_node)
        heap = []
        for uid in user_ids:
            if uid in self.users:
                u = self.users[uid]
                if u.tweet_head:
                    t = u.tweet_head
                    heapq.heappush(heap, (-t.timestamp, t.id, t))
        
        result = []
        while heap and len(result) < 10:
            _, tweet_id, tweet = heapq.heappop(heap)
            result.append(tweet_id)
            
            if tweet.next:
                t = tweet.next
                heapq.heappush(heap, (-t.timestamp, t.id, t))
        
        return result
    
    def follow(self, followerId: int, followeeId: int) -> None:
        self._get_user(followerId).follow(followeeId)
    
    def unfollow(self, followerId: int, followeeId: int) -> None:
        self._get_user(followerId).unfollow(followeeId)


# ============================================================================
# TEST CASES
# ============================================================================
if __name__ == "__main__":
    # Test Case 1: Basic operations
    print("=== Test 1: Basic Operations ===")
    twitter = Twitter()
    twitter.postTweet(1, 5)
    print(f"getNewsFeed(1): {twitter.getNewsFeed(1)}")  # [5]
    
    twitter.follow(1, 2)
    twitter.postTweet(2, 6)
    print(f"getNewsFeed(1): {twitter.getNewsFeed(1)}")  # [6, 5]
    
    twitter.unfollow(1, 2)
    print(f"getNewsFeed(1): {twitter.getNewsFeed(1)}")  # [5]
    print()
    
    # Test Case 2: Multiple users
    print("=== Test 2: Multiple Users ===")
    twitter2 = Twitter()
    for i in range(1, 4):
        for j in range(3):
            twitter2.postTweet(i, i * 10 + j)
    
    twitter2.follow(1, 2)
    twitter2.follow(1, 3)
    print(f"getNewsFeed(1): {twitter2.getNewsFeed(1)}")  # Recent from users 1, 2, 3
    print()
    
    # Test Case 3: OOP version
    print("=== Test 3: OOP Version ===")
    twitter3 = Twitter_OOP()
    twitter3.postTweet(1, 1)
    twitter3.postTweet(1, 2)
    twitter3.postTweet(2, 3)
    twitter3.follow(1, 2)
    print(f"getNewsFeed(1): {twitter3.getNewsFeed(1)}")  # [3, 2, 1]


"""
================================================================================
KEY INSIGHTS FOR ALGORITHM STUDY:
================================================================================

1. DATA STRUCTURE CHOICES:
   
   - user_tweets: HashMap of userId -> list of (timestamp, tweetId)
   - followees: HashMap of userId -> set of followeeIds
   - Global timestamp for ordering

2. NEWS FEED ALGORITHM:
   
   Like merging k sorted lists!
   
   Use min/max heap:
   - Start with most recent tweet from each user
   - Pop smallest/largest, add next from that user
   - Stop after 10 tweets

3. WHY HEAP FOR NEWS FEED?
   
   Need top 10 from potentially many users.
   Heap avoids sorting all tweets.
   
   O(k log n) where k = 10, n = followees
   vs O(t log t) for sorting all tweets.

4. TIMESTAMP MANAGEMENT:
   
   Global incrementing counter.
   Each tweet gets unique timestamp.
   
   No need for actual time - just ordering.

5. SELF-FOLLOW HANDLING:
   
   User sees own tweets in feed.
   Don't allow following yourself (redundant).

6. OOP DESIGN:
   
   Tweet class: id, timestamp, next pointer
   User class: id, followees set, tweet list
   
   Shows good design skills in practice!

7. EDGE CASES:
   
   - User with no tweets
   - User follows no one
   - User not in system
   - Unfollow someone not followed

8. SCALABILITY:
   
   Real Twitter challenges:
   - Fanout on write vs read
   - Caching
   - Sharding by user
   
   Mention these for bonus points!

9. RELATED PROBLEMS:
   
   - Merge K Sorted Lists (LC 23)
   - Design Tic-Tac-Toe (LC 348)
   - Design Hit Counter (LC 362)

10. practice TIP:
    
    "I'll use HashMaps for user data and followees.
    
    For getNewsFeed, it's like merging k sorted lists:
    - Use a max heap
    - Start with most recent tweet from each relevant user
    - Pop and add next from that user
    - Stop after 10 tweets
    
    This gives O(10 log n) instead of sorting all tweets.
    
    I'll use a global timestamp for ordering - simpler than
    real timestamps for this problem."

================================================================================
"""
