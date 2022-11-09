---
title: tracking all subclasses of a class
layout: post
tags: python
---

Let's say you have a class `A` and you want to create a list of all subclasses of `A`. I've reached for this exact structure on 3 separate occasions now, and so just recently sat down and abstracted it out to a reusable metaclass.

First, let's be concrete about the problem. We have the following classes:

```python
class A:
    pass
class B(A):
    pass
class C(B):
    pass
```

...and we would like to end with a list containing `[<class '__main__.B'>, <class '__main__.C'>]`.

There are a few naive ways to do this:

```python
# manually aggregate
classes = [B, C]

# "register" each class
classes = []
def register(class_):
    classes.append(class_)
    return class_

class A:
    pass
@register
class B(A):
    pass
@register
class C(B):
    pass

print(classes)
# [<class '__main__.B'>, <class '__main__.C'>]
```

But these approaches require manual interaction for each new subclass. So, we turn to metaclasses:

```python
classes = []
class TrackSubclassesMeta(type):
    def __init__(cls, name, bases, attrs):
        classes.append(cls)
        return super().__init__(name, bases, attrs)

class A(metaclass=TrackSubclassesMeta):
    pass
class B(A):
    pass
class C(B):
    pass

print(classes)
# [<class '__main__.A'>, <class '__main__.B'>, <class '__main__.C'>]
```

Actually, there's one small problem here, in that `A` will be added to `classes` as well. Depending on your use case this might be fine, but I almost always want the strict subclasses of a class, disincluding the class itself. So let's filter it out based on name:

```python
class TrackSubclassesMeta(type):
    def __init__(cls, name, bases, attrs):
        if name != "A":
            classes.append(cls)
        return super().__init__(name, bases, attrs)
```

Great. This is perfectly functional and what I call "v1" of the desired abstraction.

One problem - what if we wanted to track the subclasses of two classes, in separate lists `classes1` and `classes2`? Reusing the same `TrackSubclassesMeta` metaclass doesn't work, because they would get added to the same list.

With a bit of work, this is resolvable for the case of two distinct class hierarchies, or three, or four (just traverse up `cls.__mro__` until you hit one of the desired base classes, then add the class to the list corresponding to that base class). But it would require manual interaction each time we want to track the hierarchy of a new class, which is exactly what we were trying to avoid.

The biggest point of contention here is where to store the lists of subclasses, and by extension how to determine which list to add a subclass to. Ideally we're not creating them manually as we have been in the above examples, so we need somewhere we can store it programmatically. A perfect place for this is as a class attribute of the base class we're annotating with `TrackSubclassesMeta`. This attribute also doubles as a way to tell the metaclass that this class in particular is at the base of a hierarchy, and any subclasses should be added to its attribute.

Here's the code for that

```python
class TrackSubclassesMeta(type):
    def __init__(cls, name, bases, attrs):
        base = None
        # filter out current class; in particular, this prevents `A` from being
        # added as a subclass of itself
        mro = [b for b in cls.__mro__ if b != cls]
        # traverse up inheritance hierarchy, looking for a base class
        for class_ in mro:
            if hasattr(class_, "_meta_tracked_classes"):
                base = class_
        # if we found one, add this class to the base class' list
        if base:
            base._meta_tracked_classes.append(cls)
        super().__init__(name, bases, attrs)

class A(metaclass=TrackSubclassesMeta):
    _meta_tracked_classes = []
class B(A):
    pass
class C(B):
    pass

print(A._meta_tracked_classes)
# [<class '__main__.B'>, <class '__main__.C'>]
```

I've chosen to prefix the attribute with `_meta`  to make extra sure there are no name collisions, but you can choose whatever name for this attribute you want, as long as you also change it in the metaclass.

This is "v2" of the desired abstraction. With this, we can use the same metaclass to track arbitrarily many class hierarchies.

But, it's kind of dirty because we don't get to choose the name of the attribute. We can fix this by checking the *value* of an attribute to determine if it's the one we're looking for, rather than the name. To this end, let's use a custom class to denote the attribute we want to hold the base class' subclasses:

```python
# no actual new functionality, just a marker interface
class TrackedClasses(list):
    pass

class TrackSubclassesMeta(type):
    def __init__(cls, name, bases, attrs):
        base = None
        subclasses_attr = None
        # filter out current class
        mro = [b for b in cls.__mro__ if b != cls]
        # traverse up inheritance hierarchy, looking for a base class
        # (which here means a class with a TrackedClasses attribute)
        for class_ in mro:
            for name_, value in class_.__dict__.items():
                if isinstance(value, TrackedClasses):
                    subclasses_attr = name_
                    base = class_
        # add this class to the TrackedClasses attribute
        if base:
            subclasses = getattr(base, subclasses_attr)
            subclasses.append(cls)
        super().__init__(name, bases, attrs)

class A(metaclass=TrackSubclassesMeta):
    tracked_classes = TrackedClasses()

class B(A):
    pass
class C(B):
    pass

print(A.tracked_classes)
# [<class '__main__.B'>, <class '__main__.C'>]
```

(This is very similar to what libraries like [pydantic](https://github.com/samuelcolvin/pydantic) do with their custom `Field` class).

Note that we could have named `tracked_classes` whatever we wanted and it still would have worked.

This is "v3" of the desired abstraction and is, I think, quite clean. By switching to a custom `TrackedClasses` class, we're also able to specify configuration options for the metaclass, which wasn't possible before without adding another attribute to the class. For instance, just for fun let's add the ability to ignore certain subclasses by name:

```python
from collections import UserList
class TrackedClasses(UserList):
    def __init__(self, *, ignore_classes=[]):
        self.ignore_classes = ignore_classes
        super().__init__()

class TrackSubclassesMeta(type):
    def __init__(cls, name, bases, attrs):
        base = None
        subclasses_attr = None
        mro = [b for b in cls.__mro__ if b != cls]
        for class_ in mro:
            for name_, value in class_.__dict__.items():
                if isinstance(value, TrackedClasses):
                    subclasses_attr = name_
                    base = class_
        if base:
            subclasses = getattr(base, subclasses_attr)
            # check the TrackedClasses blacklist first
            if name not in subclasses.ignore_classes:
                subclasses.append(cls)
        super().__init__(name, bases, attrs)

class A(metaclass=TrackSubclassesMeta):
    tracked_classes = TrackedClasses(ignore_classes=["B"])

class B(A):
    pass
class C(B):
    pass

print(A.tracked_classes)
# [<class '__main__.C'>]
```

This is "v3.5", if you like, though it's not really any different in approach than v3.

A few final caveats. Obviously class attributes are inherited by subclasses, so `C.tracked_classes` returns the same list as `A.tracked_classes`. `A.tracked_classes` is the only one that really makes sense to access though, and you should probably avoid accessing `tracked_classes` through any subclasses of `A`.

Also, as written, the hierarchies have to be totally independent. That is, you can't use multiple `TrackSubclassesMeta` in a single hierarchy, say to track all the subclasses of `A` in `A.tracked_classes` and also track all the subclasses of `B` in `B.tracked_classes`. I think implementing this is feasible, but would take a fair bit of work.

And that's about it! I have yet to find a "metaclass utils" library, but if one exists, my guess is a metaclass similar to this one would be in it.
