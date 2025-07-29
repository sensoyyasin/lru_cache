# lru_cache
lru cache in python. It uses a hashmap and a doubly linked list to make sure get and put operations are fast (constant time). When the cache is full, it removes the least recently used items automatically. There are unit tests included, and it can handle 100,000 operations in less than 2 seconds.
