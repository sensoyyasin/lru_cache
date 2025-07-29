# Design a data structure that follows the constraints of a Least Recently Used(LRU) Cache.

# implement the LRUCache class:
# LRUCache(int capacity) initialize the LRU cache with positive size capacity.
# int get(int key) return the value of the key if the key exists, otherwise return -1
# void put(int key, int value) Update the value of the key if the key exists. Otherwise, add the key-value pair to the cache. If the number of keys exceeds the capacity from this operation, evict the least recently used key.

# 0(1) time complexity.

# Left Least Recent
# Right Most Recent

import unittest
import time

class Node:
    def __init__(self, key, value):
        self.key = key
        self.val = value
        self.prev = None
        self.next = None

class LRUCache:

    def __init__(self, capacity):
        self.cap = capacity
        self.cache = {} # key -> Node

        # Left = LRU, right = Most recently Used
        self.left, self.right = Node(0, 0), Node(0,0)
        # left <-> right
        self.left.next, self.right.prev = self.right, self.left

    # remove node from list
    def remove(self, node):
        # node = mid
        # prev -> middle -> nxt
        # prev -> nxt
        prev = node.prev
        nxt = node.next
        prev.next = nxt
        nxt.prev = prev

    # insert node at right
    def insert(self, node):
        # node = mid
        # we're gonna insert the node in mid.
        prev = self.right.prev
        nxt = self.right
        prev.next =  node
        nxt.prev = node
        node.prev = prev
        node.next = nxt


    def get(self, key):
        if key in self.cache:
            # TODO: Update the most recent
            node = self.cache[key]
            self.remove(node)
            self.insert(node)
            return node.val
        return -1

    def put(self, key, value):
        if key in self.cache:
            self.remove(self.cache[key])
        self.cache[key] = Node(key, value)
        self.insert(self.cache[key])

        if len(self.cache) > self.cap:
            # remove from the List and delete the LRU
            lru = self.left.next
            self.remove(lru)
            del self.cache[lru.key]

    def debug(self):
        curr = self.left.next
        state = []
        while curr != self.right:
            state.append(f"{curr.key}:{curr.val}")
            curr = curr.next
        print("Cache State:", " <-> ".join(state))


class TestLRUCache(unittest.TestCase):
    def test_basic(self):
        cache = LRUCache(2)

        cache.put(1, 10)
        cache.debug()
        cache.put(2, 20)
        cache.debug()
        self.assertEqual(cache.get(1), 10)
        cache.debug()
        cache.put(3, 30)
        cache.debug()
        self.assertEqual(cache.get(2), -1)
        cache.debug()
        cache.put(4, 40)
        cache.debug()
        self.assertEqual(cache.get(1), -1)
        self.assertEqual(cache.get(3), 30)
        self.assertEqual(cache.get(4), 40)

    def test_update_value(self):
        cache = LRUCache(2)
        cache.put(1, 100)
        cache.put(1, 200)
        self.assertEqual(cache.get(1), 200)

    def test_capacity_one(self):
        cache = LRUCache(1)
        cache.put(1, 10)
        cache.put(2, 20)
        self.assertEqual(cache.get(1), -1)
        self.assertEqual(cache.get(2), 20)

    def test_benchmark(self):
        cache = LRUCache(1000)
        start = time.time()
        for i in range(100000):
            cache.put(i, i)
            cache.get(i)
        elapsed = time.time() - start
        print("Elapsed:", elapsed)
        self.assertTrue(elapsed < 2)

if __name__ == "__main__":
    unittest.main()
