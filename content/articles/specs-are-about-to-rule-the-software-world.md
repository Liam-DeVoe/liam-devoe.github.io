---
title: Property-based testing is about to rule the (software) world
date: 2026-02-11
slug: specs
---

*And what can we do to prepare?*

Many people have strong opinions about the next few years of AI progress. Regardless of yours, I claim that (1) the models will continue to improve for at least another 6 months; and (2) even if that stopped *today*, Opus 4.6-tier models are already powerful enough to dramatically change how many developers write software.

I characterize this change as "AI code is treated as a black box". AI-pilled programmers care only about the observable outcome of code, not the implementation. In other words: the only thing that matters anymore *is the guarantees on the box*. When I ask the black-box z3 solver for a satisfying assignment, I don't care how it got there, only that the result is a valid SAT formula.

If we are to embrace AI code as an industry, we will and must adopt better ways to place guarantees on these black boxes. And I think property-based testing will quickly emerge as the forerunner.[^2][^3]

# Property-based testing

I have always been surprised at how under-adopted property-based testing is. Do companies not care about testing? Is it not mentioned enough in university curriculums? (Yes, but I digress). Has PBT just not permeated the cultural zeitgeist?

It doesn't really matter. AI is about to provide the forcing function for PBT to become a developer household name. Or, to put it another way: *PBT is about to get a lot more users*.

And yet, the PBT ecosystem is underprepared for this influx. In Python, I maintain [Hypothesis](https://github.com/hypothesisWorks/hypothesis), which I have no qualms in claiming as the most successful PBT library of all time.[^1] Python might well weather this storm.

But as much as I love Python, it comprises a small percentage of production code. What about other languages? Most do have a PBT library. And, to be clear, many years of development effort have gone into them. But I think even their maintainers will acknowledge most other libraries don't match the breadth and depth of Hypothesis:

* [Internal shrinking](https://drmaciver.github.io/papers/reduction-via-generation-preview.pdf), which is [consistently world-class](https://github.com/jlink/shrinking-challenge)
* [Pluggable backends](https://hypothesis.readthedocs.io/en/latest/extensions.html#alternative-backends), including [z3 integration](https://github.com/pschanely/hypothesis-crosshair)
* [Observability](https://hypothesis.readthedocs.io/en/latest/reference/integrations.html#observability)
* [Coverage-guided fuzzing integration](https://hypofuzz.com/)
* [A powerful internal test case representation](https://github.com/HypothesisWorks/hypothesis/issues/3921)
* [Stateful testing](https://hypothesis.readthedocs.io/en/latest/stateful.html)
* [Test case database](https://hypothesis.readthedocs.io/en/latest/tutorial/replaying-failures.html), for regressions
* Test case deduplication

My point is not to glorify Hypothesis. Even after 11 years of development, there is always more to improve. Rather, the demand for PBT is about to explode, and I don't think any language is prepared for it—maybe not even Python.

My concrete call to action: as a PBT ecosystem, we need to figure out how to share improvements among all libraries, to consolidate and amplify the best of our development effort. I am not the first to say this, but it has never been more true than today. The open [PBT observability spec](https://hypothesis.readthedocs.io/en/latest/reference/integrations.html#observability) is designed for any language and is a step in this direction.

What else can we standardize? Shrinking? The database? The choice sequence? How can we take the best parts of *every* library and combine them into one, in preparation for the PBT renaissance?

If you maintain a PBT library and want to collaborate with Hypothesis on this, [reach out](mailto:orionldevoe@gmail.com).

[^2]: At least until we can autonomously formally verify code according to the theorem statement "this code has no bugs". I expect this to be many years away even at current model progress rates.
[^3]: Or fuzzing, if you prefer that framing. I largely see fuzzing and PBT as two views on the identical problem, and think it's unfortunate we don't have more communication between these two worlds.
[^1]: See [https://hypothesis.readthedocs.io/en/latest/usage.html](https://hypothesis.readthedocs.io/en/latest/usage.html). For example, [4% of 2024 PSF survey respondents report using Hypothesis](https://lp.jetbrains.com/python-developers-survey-2024/).
