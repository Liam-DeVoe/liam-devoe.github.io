---
title: "a quirk in super()"
layout: post
---

Quiz time! Consider the following piece of code:

```python
class A:
    def f(self):
        print("A.f called")
        super().f()

class B:
    def f(self):
        print("B.f called")

class C(A, B):
    pass

C().f()
```

Will this code crash when run? Obviously `A` doesn't inherit from anything, so that `super().f()` call is suspect. But at runtime a "super" of sorts does exist in `C` - namely, `B`. Place your bets now..

The answer, to my surprise, is that this code runs fine. My intuition of `super()` was a sort of static implementation, where if a class doesn't inherit from anything then any `super` call will fail (well, get forwaded to `object`, which obviously doesn't implement `f`).

But in reality, `super()` looks at the mro at runtime and chooses the next matching function to call. That mro is dependent on the class the function belongs to (`C`), not the class the function was originally defined in (`A`). If we dynamically modify the mro of `C` to take `B` out of the picture, the call to `f` fails:

```python
class A:
    def f(self):
        print("A.f called")
        super().f()

class B:
    def f(self):
        print("B.f called")

class ChangeMROMeta(type):
    def mro(cls):
        return (cls, A, object)

class C(A, B, metaclass=ChangeMROMeta):
    pass

c = C()
print(C.__mro__)
c.f()
```

This means you can have a method in a class which always fails but runs fine when you subclass it in a very particular way. I can't think of a black magic use case for this, but maybe someone else can!
