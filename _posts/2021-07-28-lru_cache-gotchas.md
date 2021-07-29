---
title: "@lru_cache gotchas"
layout: post
---

I was adding some caching to a django application via `@lru_cache`, and much to my confusion, it wasn't working. I could even see the cache missess ticking up as I was calling it with identical (read: no) arguments. Here's what it looked like:

```python
import random
from functools import lru_cache
from django.views import View
from django.http import JsonResponse

class Course(View):

    def get(self):
        print("page loaded")
        data = self.expensive()
        print(f"data: {data}")
        return JsonResponse({"data": data})

    @lru_cache
    def expensive(self):
        return random.randint(1, 100)
```

And upon refreshing the page three times:

```python
page loaded
data: 72
page loaded
data: 5
page loaded
data: 25
```

What's going on here? Why aren't you caching the computation? It was at this point I began to seriously question my understanding of `lru_cache` and its usage. Perhaps I've missed something obvious in the docs. Does it need to be `@lru_cache()` instead of `@lru_cache`? No, either form works. Is this function actually the one getting called, or is some other proxy being called somehow? No, I can see the cache misses incrementing:

```python
    @lru_cache
    def expensive(self):
        print(self.expensive.cache_info())
        return random.randint(1, 100)
```

```python
CacheInfo(hits=0, misses=1, maxsize=128, currsize=0)
CacheInfo(hits=0, misses=2, maxsize=128, currsize=1)
CacheInfo(hits=0, misses=3, maxsize=128, currsize=2)
```

Well, to make a long story short, it turns out `lru_cache` uses every single argument to a function to generate the key for that entry. *Including* `self`. This isn't surprising in hindsight - `self` is, after all, just an argument like any other - but it took me longer than I care to admit to realize this was the issue.

To be explicit, here's a simple example of what's going on:

```python
import random
from functools import lru_cache

class RandomHash:
    @lru_cache
    def expensive(self):
        return random.randint(1, 100)

    def __hash__(self):
        return random.randint(1, 100)

r = RandomHash()
print(r.expensive())
print(r.expensive())
print(r.expensive())
```

```python
21
10
72
```

As you can see, the function calls aren't actually being cached.

This wouldn't normally be a big deal, except django is doing some magic behind the scenes that causes a `View`'s hash to every time you load its page. This explains why every single call was a miss; the hash of the parameters was indeed changing on every call.

Is there an easy solution to my original problem? In this case, yes. My computation didn't rely on any instance attributes, so it could be trivially converted to a static method, avoiding the issue altogether by simply taking `self` out of the equation:

```python
    @staticmethod
    @lru_cache
    def expensive():
        return random.randint(1, 100)
```

```python
92
92
92
```

But what if I did need `self` to access some attribute or call some method? I don't see an easy way out there. I think I would have to write my own wrapper around `lru_cache` which ignores the first parameter (ie `self`) when computing the hashed key. I actually started doing this and it quickly became messy, so I'm glad I haven't had to. Yet.

(to preempt any "why not just use `@cached_property`?" comments, the actual computation taking place did take parameters to the function, so a true `lru_cache` was necessary. I've just simplified for this post)
