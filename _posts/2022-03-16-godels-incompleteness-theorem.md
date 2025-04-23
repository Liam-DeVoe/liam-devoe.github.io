---
title: "gödel's incompleteness theorem"
layout: post
tags: math
---

Ah, Gödel's incompleteness theorem. I won't say it's the most misused theorem in all of mathematics, but I would argue it has the worst ratio of "people who actually understand it" to "people who misapply it".

Here it is:

<div class="quote">For any sufficiently strong theory $T$, there is a sentence $\sigma$ which is independent of $T$.</div>

Before we can unpack it, you need a crash course in model theory. This will be a little bit painful, but I promise it's critically important.

# Sentences and Theories

Here are the axioms of group theory, which you'll find at the beginning of any standard textbook:

$$
\begin{equation}
\begin{aligned}
& \sigma_0: \forall a \forall b \forall c \ (c*(a*b) = (c*a)*b) \\
& \sigma_1: \forall a \ (e*a = a) \\
& \sigma_2: \forall a \exists b \ (a*b = e) \\
\end{aligned}
\end{equation}
$$

(If you're not familiar with group theory, don't worry; the actual content of these axioms is largely irrelevant for us. They state that $*$ is associative, has an identity $e$, and every element has an inverse respectively).

What your group theory textbook probably didn't tell you is that there's a language $L_{group}$ associated with group theory. This is the set of special symbols we'd like to be able to refer to in our sentences: $L_{group} = \\{e, *\\}$.

The three axioms above are examples of sentences. A **sentence** is a statement in first order logic which contains only logical symbols ($\lnot$, $\land$, $\lor$, $\implies$, $\iff$, $\forall$, $\exists$), or symbols from our language $L$. For instance, the following is not an $L_{group}$-sentence:

$$\forall a \ (a + a = a)$$

because $+$ isn't in $L_{group}$. Note that whether a statement is a sentence or not depends on the language, which is why we say $L_{group}$-sentence instead of just sentence. When the language is clear from context, we'll drop the $L$- prefix and call it a sentence.

We can bundle these axioms together into an object called a **theory**. $T_{group} = \\{\sigma_0, \sigma_1, \sigma_2\\}$ is the theory of groups. A theory is any set of sentences.[^1]

Here's the incompleteness theorem again:

<div class="quote">For any sufficiently strong theory $T$, there is a sentence $\sigma$ which is independent of $T$.</div>

We've defined **sentence** and **theory**. Let's tackle **independent** next.

# Models

To discuss independence of sentences, we first need to talk about models. We say that $\mathcal{A}$ is a model of a theory $T$ if $\sigma$ is true in $\mathcal{A}$ for all $\sigma \in T$.[^2]

Don't be scared by the notation. If you wanted to check whether something is a group or not, what do you do? You check that it satisfies all the axioms of being a group. That's all this definition is stating. Saying "$(\mathbb{Z}, +)$ is a group" is equivalent to saying "$(\mathbb{Z}, +)$ models $T_{group}$". And if $\mathcal{A}$ models $T$, we write $\mathcal{A} \vDash T$.

We need just one more definition. Let $T$ be any theory. Then $T$ is **complete** if, for all sentences $\sigma$ and for all models $\mathcal{A} \vDash T$ and $\mathcal{B} \vDash T$, $\sigma$ is true in $\mathcal{A}$ iff $\sigma$ is true in $\mathcal{B}$. In other words, "every model of $T$ agrees on the truth value of every sentence".

A natural question is whether $T_{group}$ is complete. Can you think of a sentence $\sigma$ which is true in some group $\mathcal{A} \vDash T_{group}$ but false in another group $\mathcal{B} \vDash T_{group}$? Hint: the answer is yes, there are several such sentences, and they aren't that complicated. Try and think of one now before you read on, if you like.

(pause...) if you said "$\mathcal{A}$ is abelian" (ie $*$ commutes in $\mathcal{A}$), you're correct! I also would have accepted "$\mathcal{A}$ has an element of order n" for some n. Here's a sentence that is true in $\mathcal{A}$ iff $\mathcal{A}$ is abelian:

$$
\sigma_{abelian} = \forall a \forall b \ (a*b = b*a)
$$

To see that $\sigma_{abelian}$ proves that $T_{group}$ is not complete, pick your favorite abelian group, say $(\mathbb{Z}, +)$, and your favorite non-abelian group, say $GL(2, \mathbb{R})$. $\sigma_{abelian}$ is true in $(\mathbb{Z}, +)$ and false in $GL(2, \mathbb{R})$, since addition commutes and matrix multiplication does not. But both $(\mathbb{Z}, +)$ and $GL(2, \mathbb{R})$ are models of $T_{group}$ — after all, they're both groups and thus satisfy the three axioms of $T_{group}$. So $\sigma_{abelian}$ is true in $(\mathbb{Z}, +) \vDash T_{group}$ and false in $GL(2, \mathbb{R}) \vDash T_{group}$, so $T_{group}$ is not complete.

# Independence

What about independence? Let $T$ be any theory and $\sigma$ be any sentence. Then $\sigma$ is **independent** of $T$ if there are two models $\mathcal{A} \vDash T$ and $\mathcal{B} \vDash T$ such that $\sigma$ is true in $\mathcal{A}$ and false in $\mathcal{B}$. In the example above, $\sigma_{abelian}$ is independent of $T_{group}$. A corollary is that a theory $T$ is not complete iff there is some sentence $\sigma$ which is independent of $T$. I'll do the proof explicitly below, but it's nothing more than unpacking the respective definitions.

<div class="quote">
$\implies$ Let $T$ be not complete. So there is some sentence $\sigma$, some model $\mathcal{A} \vDash T$ and $\mathcal{B} \vDash T$, such that either $\sigma$ is true in $\mathcal{A}$ and false in $\mathcal{B}$, or false in $\mathcal{A}$ and true in $\mathcal{B}$. In either case, $\sigma$ is independent.
</div>

<div class="quote">
$\impliedby$ Let $\sigma$ be a sentence independent of $T$. Then there are $\mathcal{A} \vDash T$ and $\mathcal{B} \vDash T$ such that $\sigma$ is true in $\mathcal{A}$ and false in $\mathcal{B}$. So $T$ is not complete. $\blacksquare$
</div>

If a theory $T$ is "not complete", we call $T$ incomplete.

Let's take a closer look at the incompleteness theorem, as stated:

<div class="quote">For any sufficiently strong theory $T$, there is a sentence $\sigma$ which is independent of $T$.</div>

We just proved that $T$ is incomplete iff there is a sentence $\sigma$ which is independent of $T$. So we can restate the theorem as:

<div class="quote">Any sufficiently strong theory $T$ is incomplete.</div>

This is where the "incompleteness" portion of the theorem's name comes from. Although these statements are equivalent, I'll continue to use the first, longer version, since I feel it's more intuitive (as it doesn't require you to unpack the definition of $T$ being incomplete).

Before I make our final definition of **sufficiently strong**, I want to take a detour into euclidean geometry as a final example to round out our discussion of theories and models.

# Euclidean geometry

Euclidean geometry is another example of a theory. It contains five axioms and three "undefined terms": point, line, and plane are undefined and are referenced in the axioms without definition. Does that sound familiar? We did the exact same thing in groups, using the "undefined terms" $*$ and $e$ in our axioms, and defining them to be part of our language $L_{group}$. It turns out that the notion of a language has always been hiding in euclidean geometry. The language of euclidean geometry is just $L_{euclid} = \\{\text{point}, \text{line}, \text{plane}\\}$. I'll call $T_{EG}$ the theory of euclidean geometry, which is the set of the five axioms of euclidean geometry.

You'll notice that I'm not giving a precise mathematic definition of the axioms, but that's because Euclid himself didn't really give precise mathematical definitions either. Euclidean geometry can in fact be made precise (see [Tarski's Axioms](https://en.wikipedia.org/wiki/Tarski%27s_axioms)), and everything I say below will still hold, but I'll avoid deviating too much from the euclidean geometry described in Euclid's Elements.

You may also know of the particularly contentious parallel postulate (PP), the fifth axiom of euclidean geometry. Some people thought that the parallel postulate could be proven from the rest of the axioms, and gave the name "neutral geometry" to the set of axioms of euclidean gemoetry without PP. I'll call the theory of neutral geometry $T_{NG} = T_{EG} \setminus \\{PP\\}$. They then showed PP could not be proven from the rest of the axioms by constructucting two models of $T_{NG}$: one in which PP was true (a model of euclidean geometry) and one in which PP is false (a model of elliptical geometry).

Once they had shown PP could not be proven from neutral geometry, they called PP independent of neutral geometry. Does this term "independent" sound familiar? It should — we defined $\sigma$ to be independent of $T$ if there are $\mathcal{A} \vDash T$, $\mathcal{B} \vDash T$ where $\sigma$ is true in $\mathcal{A}$ and false in $\mathcal{B}$. Here, $\sigma$ is the parallel postulate, $T$ is neutral geometry, $\mathcal{A}$ is a model of euclidean geometry, and $\mathcal{B}$ is a model of elliptical geometry. In general, proving that an axiom $\sigma \in T$ is "independent" of (cannot be proven from) the other axioms of $T$ is equivalent to proving that $\sigma$ is independent of $T \setminus \\{\sigma\\}$, in the formal sense of independence described above.

Because PP is independent of $T_{NG}$, $T_{NG}$ is incomplete. However, it turns out that $T_{EG} = T_{NG} \cup \\{\text{PP}\\}$ is complete, so by taking PP as a new axiom we've created a complete theory.[^3] We'll discuss this concept of "completing" a theory $T$ by adding new axioms again later, and whether this can save us from the consequences of the incompleteness theorem. Spoiler: it can't.

# Sufficiently strong

I've left the simplest – or at least, easiest to informally explain – for last. A theory $T$ is **sufficiently strong** if it contains the natural numbers, addition on the natural numbers, and multiplication on the natural numbers (or contains objects isomorphic to them). More formally, $T$ is sufficiently strong if it contains [Robinson arithmetic](https://en.wikipedia.org/wiki/Robinson_arithmetic), called $Q$. If you're familiar with peano arithmetic, $Q$ is peano arithmetic without induction.

Understanding *why* containing $Q$ is necessary gets to the heart of the proof of the incompleteness theorem and is a much deeper discussion than we can get into here, so I hope you'll forgive me for not going into any more detail.

# Bringing it all together

Let's recap:

* A sentence $\sigma$ is a statement in first order logic, potentially containing symbols from some language $L$
* A theory $T$ is a set of sentences
* $\mathcal{A}$ is a model of $T$ (written $\mathcal{A} \vDash T$) if $\sigma$ is true in $\mathcal{A}$ for all $\sigma \in T$
* A sentence $\sigma$ is independent of a theory $T$ if there are models $\mathcal{A} \vDash T$, $\mathcal{B} \vDash T$ with $\sigma$ true in $\mathcal{A}$ and false in $\mathcal{B}$
* A theory $T$ is sufficiently strong if it contains $Q$, aka robinson arithmetic (informally, if it contains the natural numbers, addition, and multiplication)

And finally, the incompleteness theorem itself:

<div class="quote">For any sufficiently strong theory $T$, there is a sentence $\sigma$ which is independent of $T$.</div>

Congratulations — you now know everything you need to understand the statement of the incompleteness theorem. If that was your goal, you can walk away here, but I'll discuss the consequences of this theorem next.

# Consequences

To start, a question: is the converse of the incompleteness theorem true? No. We saw above that $T_{group}$ has a sentence $\sigma_{abelian}$ which is independent of $T_{group}$, but $T_{group}$ certainly does not contain $Q$. Informally, this means that theories can be incomplete for "other reasons" than the incompleteness theorem (actually, it's quite easy to create incomplete theories; much easier than creating complete ones). The reason why the incompleteness theorem is so important is not because it applies to a large number of theories, but because the theories it does apply to are important ones that we would really prefer to be complete.

In particular, the incompleteness theorem often comes up adjacent to the foundations of mathematics, with theories like $\text{ZFC}$. Although perhaps not obvious just by looking at the axioms, $\text{ZFC}$ can prove the axioms of $Q$, and is in fact much, much stronger than it. So $\text{ZFC}$ is sufficiently strong and thus subject to the incompleteness theorem, so there is some $\sigma$ which is independent of $\text{ZFC}$. In other words, there are theorems (sentences) which we will never be able to prove or disprove from the axioms of $\text{ZFC}$.

This probably doesn't sound too bad. So what? Well, think about your favorite mathematical field (which almost certainly uses $\text{ZFC}$ as its mathemtical foundations, unless you're a category theorist). Then think about some famous unsolved conjecture in that field. Most people think there are only two options: either that conjecture is true, or it's false. The incompleteness theorem says there's a third possibility: the conjeture is one of these independent sentences $\sigma$, and thus can never be proven or disproven in $\text{ZFC}$.

I would say that proving a famous theorem independent is a much worse fate than proving it either true or false. Consider $T_{NG}$, the theory of neutral geometry we discussed above, and the theorem under discussion to be the parallel postulate PP, which we know is independent of $T_{NG}$. When PP was found to be independent of $T_{NG}$, it split the world of euclidean geometry in two. In one camp are the worlds in which PP is true; we call these euclidean geometries, with theory $T_{NG} \cup \\{\text{PP}\\}$. In the other camp are the worlds in which PP is false; we call these non-euclidean geometries, with theory $T_{NG} \cup \\{\lnot \text{PP}\\}$. Because PP is independent of $T_{NG}$, both of these worlds are "equally valid". In my opinion, having two possible worlds is worse than knowing for certain which "world" we live in, like we would if PP was not independent of $T_{NG}$ (and therefore either true or false).

However, there's a reason why non-euclidean geometries are significantly less studied: most people believe PP is "intuitively true", and study euclidean geometry instead of non-euclidean geometry. This is true of PP, but it's not true of all independent sentences. Sometimes an independent sentence really does fracture a theory into multiple, equally popular camps. In other words, it's not always obvious which "choice" to make (eg whether to add PP or $\lnot$PP).

For instance, in set theory, the [Continuum Hypothesis](https://en.wikipedia.org/wiki/Continuum_hypothesis) (CH) is the most well known example of a theorem independent of $\text{ZFC}$. When it was proven to be independent, it split the world of set theory in two, just like PP did. But this time it's worse, because there is a large amount of disagreement among set theorists about whether CH is intuitively true. If you tried to get $\text{ZFC} \cup \\{\text{CH}\\}$ accepted as the foundation of mathematics (instead of $\text{ZFC} \cup \\{\lnot \text{CH}\\}$ or just $\text{ZFC}$), you would get significant pushback from set theorists, beacuse to them, both worlds are equally interesting.

You might hold out hope that alright, fine, $\text{ZFC}$ has some independent sentences, but they're sentences we didn't really care about anyway. This is actually mostly true if you're not a set theorist and don't work with graduate level math! Most sentences independent of $\text{ZFC}$ come from set theory, and the rest are complicated statements in other fields, most of which I don't even understand the statement of.[^4] But the incompleteness theorem puts a "cap", so to speak, on $\text{ZFC}$ (and thus mathematics): the deeper into a subject you go, the closer and closer you brush up against independent statements. And if you're particularly unlucky, you'll actually run into a theorem in your work which is independent of $\text{ZFC}$, and you'll curse the incompleteness theorem when you do.

So, sentences being independent of a theory is bad, and all theories which can serve as the fondation of mathematics have independent sentences (because they are, to a tee, sufficiently strong). This is the single most important implication of the incompleteness theorem.

## Incompleteness of $T_{group}$

But wait — if a theory $T$ being incomplete is bad, and we proved that $T_{group}$ is incomplete above, isn't that bad news for group theorists? Well, it's not *good*, but it's also not bad. It's true that $\sigma_{abelian}$ splits $T_{group}$ into two theories: $T_{group} \cup \\{\sigma_{abelian}\\}$ and $T_{group} \cup \\{\lnot \sigma_{abelian}\\}$. But these are just the theories of abelian and non-abelian groups respectively. If I had asked you whether studying abelian and non-abelian groups separately bothers you, you would have looked at me like I'm crazy. After all, if you want to prove something about abelian groups, you just assume that $G$ is abelian (but note that this is identical to working in $T_{group} \cup \\{\sigma_{abelian}\\}$).

The difference lies in that $T_{group}$ is not trying to be a theory of mathematics. You don't particularly care if you can't prove every possible statement for all groups, because if you can't, you can always look at a specific group you care about and prove whether that statement is true in that group or not. This isn't possible in a theory of mathematics.[^5]

## Completeness of $T_{EG}$

But wait — we said earlier that the theory of euclidean geometry, $T_{EG}$, was complete. Does this contradict the incompleteness theorem? No, because $T_{EG}$ is not "sufficiently strong". There are a number of interesting theories which are complete, like $T_{EG}$, but aren't strong enough to be subject to the incompleteness theorem.

## "Completing" a theory

Recall that we saw $T_{NG}$ (neutral geometry), which is incomplete, could be extended to a complete theory $T_{EG}$ (euclidean geometry) by adding the parallel postulate. We say that $T_{EG}$ is a "completion" of $T_{NG}$, that $T_{NG}$ can be "completed" by adding PP, etc.

You might wonder if we could pull the same trick for theories affected by the incompleteness theorem. Given some sufficiently strong theory $T$, the incompleteness theorem says there is some $\sigma$ independent of $T$. Could we complete $T$ by adding either $\sigma$ or $\lnot \sigma$ to $T$ as an axiom? The answer is no, regardless of which we choose. Adding an axiom to a theory never makes that theory weaker (ie prove less sentences) — it can only make it stronger. This new theory $T' = T \cup \\{\sigma\\}$ would still be sufficiently strong and thus satisfy the incompleteness theorem, so there is some new sentence $\sigma'$ which is independent of $T'$.

So no matter how many independent sentences we add as axioms to a sufficiently strong theory, it will still be sufficiently strong and subject to the incompleteness theorem. A sufficiently strong theory can never be "completed".

# Independent sentences are "true"

This misunderstanding (I'm tempted to say "abuse") is the singular reason I wrote this post, so you'll have to forgive me if I rant a bit here. The single most common misuse of the incompleteness theorem is stating that the independent sentence is somehow "true". Here's a direct quote [from wikipedia](https://en.wikipedia.org/wiki/G%C3%B6del%27s_incompleteness_theorems):

<div class="quote">For any such consistent formal system, there will always be statements about natural numbers that are true, but that are unprovable within the system.</div>

(They're using "consistent formal system" to be some theory $T$, "statements about the natural numbers" to be some sentence $\sigma$, and "unprovable within the system" to mean "independent of $T$").

Except this is wrong. An independent sentence $\sigma$ is absolutely not "true". It is, *by definition*, true in some model $\mathcal{A} \vDash T$ and false in some other model $\mathcal{B} \vDash T$, so calling it "true" is nonsense. It's neither true nor false; it's independent.

What people really mean when they say that an independent sentence $\sigma$ is true is that it's true in the "standard model", and therefore, they argue, intuitively true. What is the standard model? Nothing more than a particular model $\mathcal{A} \vDash T$ we have arbitrarily chosen as intuitive for visualizing $T$. For instance, the standard model of euclidean geometry $T_{EG}$ is the plane $\mathbb{R}^2$.

But for other theories, it's not clear at all what the standard model is – say, for $T_{group}$. You might suggest $$(\mathbb{Z}, +)$$, but there's no good reason to choose that group over, say $$(\mathbb{Z}_8, +)$$, or even $$GL(2, \mathbb{R})$$. Here, the concept of a "standard model" breaks down.

For theories which have a standard model, this line of thinking does have some philosophical merit. I just wish people would say "there is a sentence which cannot be proven from $T$ but is true in the standard model", instead of saying "there is a true sentence which cannot be proven", which sounds like a contradiction. This seeming contradiction bothered me for many years when reading about the incompleteness theorem, and I was greatly relieved to eventually learn that people were simply misinterpreting the theorem.

## Gödel's completeness theorem

Before his incompleteness theorem, Gödel proved another theorem about the completeness of first order logic. Informally, this theorem says that for all theories $T$ and sentences $\sigma$, if $\sigma$ is true in every model $\mathcal{A} \vDash T$, then there is a proof of $\sigma$ from the axioms of $T$. In other words, there is a proof of every true statement.

The naming of these theorems suggests a contradiction: how can we have both Gödel's completeness theorem and Gödel's incompleteness theorem?

Well, because they refer to two different notions of completeness. "completeness" in the completeness theorem means that "everything which is true is provable". However, "incompleteness" in the incompleteness theorem means that some theories $T$ have sentences which are neither true nor false in $T$. These independent sentences don't even satisfy the conditions of the completeness theorem (since they're not true in every model), so these two theorems are entirely orthogonal.

# Technicalities

I haven't been entirely truthful with you. There are two extra assumptions we need to add before we get the true incompleteness theorem. They deal with what are essentially edge cases – though very important edge cases.

## Satisfiable

First, we require that the theory $T$ be **satisfiable**. A theory $T$ is **satisfiable** if there is any model $\mathcal{A} \vDash T$ at all. Equivalently, $T$ is satisfiable if its axioms are consistent, ie you can't derive a contradiction from them. If we allowed $T$ to be unsatisfiable, then the incompleteness theorem would fail in the trivial case: let $T$ be any sufficiently strong, unsatisfiable theory. Then there are no models $\mathcal{A} \vDash T$, so vacuously, there are no independent sentences $\sigma$ (since an independent sentence requires at least two models). But this would contradict the incompleteness theorem.

Here's our updated incompleteness theorem:

<div class="quote">For any sufficiently strong, satisfiable theory $T$, there is a sentence $\sigma$ which is independent of $T$.</div>

## Recursively enumerable

For what are actually pretty technical reasons, we also require $T$ to "recursively enumerable". This is equivalent to saying that the elements of $T$ are "computable", ie there is an algorithm which, given any sentence $\sigma$, returns true if $\sigma \in T$ and false otherwise. It's not worth getting into the details here, but this basically rules out crazy theories where you just throw in so many axioms that you're eventually able to prove everything in all models. Any "reasonable" theory like $\text{ZFC}$ or $Q$ is recursively enumerable.

You might also see such theories being called "decidable", as in, you can "decide" whether a sentence $\sigma$ is an element of $T$.[^6]

So our updated incompleteness theorem is then:

<div class="quote">For any sufficiently strong, satisfiable, recursively enumerable theory $T$, there is a sentence $\sigma$ which is independent of $T$.</div>

You can see why I didn't want to lead with this definition :)

I promise that I'm not holding anything back anymore — this is the genuine, full incompleteness theorem which Gödel himself proved[^7]. These extra assumptions rarely come up in casual discussions, which is why I left them until now to discuss.

# Afterword

I debated a lot about which examples of theories to use, and in fact originally wrote a draft where I used the theory of real-valued vector spaces. Unfortunately, its axiomatization is quite dirty, and so I dropped it in favor of the theory of groups, even though I think more people would be familiar with vector spaces than groups. Oh well.

There are also some philosophical implications I wanted to include, but I don't feel qualified to discuss them. I'm also not really convinced how big the philosophical implications of the incompleteness theorem are.

[^1]: Since theories consist of sentences, and sentences depend on a language, you would be right to suspect that theories also depend on a language. Formally we call a theory $T$ an $L$-theory, where L is the language of the theory. We again drop the $L$- prefix when the langauge is clear from context.

[^2]: If $\sigma$ is true in $\mathcal{A}$, you'll see this written in the literature as $\mathcal{A} \vDash \sigma$. However, you'll see very shortly that this is an overloading of the $\vDash$ operator; its meaning changes depending on if the right hand side is a sentence $\sigma$ or a theory $T$. I've avoided writing $\mathcal{A} \vDash \sigma$ here for clarity, but it is the more precise usage.

[^3]: Proving that euclidean geometry is complete requires a more formal axiomatization than what Euclid gave, and so we turn to [Tarski's Axioms](https://en.wikipedia.org/wiki/Tarski%27s_axioms) (sometimes called elementary euclidean geometry) instead. This is outside the scope of this post, but Tarski proved that his theory was complete by showing that it admits quantifier elimination. Completeness follows from this since the language has no constants, which means the only sentences without quantifiers are $\top$ and $\bot$, which are true and false in every model respectively.

[^4]: See [List of statements independent of ZFC](https://en.wikipedia.org/wiki/List_of_statements_independent_of_ZFC).

[^5]: This is because any theory of mathematics can't prove that there are any models of that theory, or else the theory would be consistent, which contradicts Gödel's second incompleteness theorem. So there are no "specific models" of a theory of mathematics to look at — in fact, there are no models of a theory of mathematics at all.

[^6]: The multitude of names is thanks to computability theory, which proved that several distinct notions of computability (all with their own names) are actually exactly equivalent, and thus the names are interchangeable.

[^7]: Ok, fine, you got me: Gödel's original proof required something called [$\omega$-consistency](https://en.wikipedia.org/wiki/%CE%A9-consistent_theory), a strengthening of consistency. However, it turns out this condition can be weakened to consistency alone, with [Rosser's trick](https://en.wikipedia.org/wiki/Rosser%27s_trick).
