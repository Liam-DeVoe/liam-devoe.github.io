---
title: My agent management software
date: 2026-04-29
slug: plait
tags: coding
---

I write a lot of code. Or rather, I *used* to write a lot of code. After Claude Opus ~4.5, it's now more accurate to say that I review and design a lot of code.

Around the release of Opus 4.5 was also when I started working on [Hegel](https://hegel.dev/). As a greenfield project spanning multiple repositories, my work on Hegel surfaced pain points I don't normally encounter when working on Hypothesis or other projects, such as managing the frequent small PRs and merge conflicts that come with a young, active codebase.

Thanks to some combination of these two factors, I found myself settling on a wishlist for tooling around my development flow:

- I now context switch—a lot. I'm writing a feature spec one moment, bouncing design ideas off an agent the next, before getting pulled away to review a third agent's work. All while waiting for a long-running research or implementation agent in the background. I need something that manages my various task states, so I always feel that I can walk away and come back later.
- Coordinating a change across multiple repositories requires a context switch to manage their branches, PRs, and GitHub interlinks. It shouldn't have to. I want to say what I want once, across all repositories, and let the agents get the git details right.
- I never want to manually resolve a merge conflict again. The agents are here. We have the technology.

And, well—seeing as coding agents have made personalized tooling cheap (but *not* free, despite some claims to the contrary!), I figured I'd spend a week building exactly such a tool.

# Plait

Here's Plait, my agent management software[^1]:

![](/images/plait_homepage.png)

The unit of work in a repository is a *worktop*. Each worktop has a git worktree, and has a nullable 1:1 correspondence with a pull request. That is, you can think of a worktop as scoped to the same unit of work as a PR, but which may or may not have an associated PR yet.

A worktop can contain multiple Claude sessions:

![](/images/plait_worktop.png)

Claude sessions are standard `claude` processes. Claude code persists sessions on disk automatically, which Plait resumes on demand with `claude --resume <session_id>`.

My most used workflow is to open a new worktop and talk with its session, eventually telling it to PR its changes. Many worktops only need this single session. Others, especially more involved features, benefit from the advanced context management you get with multiple sessions.

In the background, every 5 minutes, Plait kicks off a daemon process. This daemon checks for state changes in any worktops with associated pull requests. Is there a merge conflict? Has the CI turned from green to red? Are there new PR comments or reactions?

If so, the daemon starts a *tend* session. This is a Claude session with instructions to resolve the merge conflict, fix the CI if caused by our changes, and resolve any comments addressed towards it. Tend sessions are saved for each worktop if I need to inspect them later.[^2]

Finally, Plait has a higher order notion called a *slate*. A slate orchestrates multiple worktops, potentially across repositories.

![](/images/plait_slate.png)

I start a slate whenever a change touches more than one repository. I talk with the slate's session until I'm confident it has enough context to spawn sessions whose instructions I won't need to immediately revise. The slate then creates the appropriate worktops, spawning a session in each with instructions to implement its portion of the feature.

From here, I have two options. I can either dip down to a specific worktop to manually manage its sessions. Or, if I realize I need to make a cross-repo adjustment, I can tell that to the slate session, and have it spawn and manage the worktop sessions for me.

As an escape hatch to the underlying tools, I can always click `VS Code` on a worktop to open a VS Code window at that worktree. And I can click `VS Code` on a Claude session to open the same, additionally with a terminal window opened to that Claude session.[^3]

[Plait is open-source here](https://github.com/Liam-DeVoe/plait). I make no guarantees of support or stability. In fact, I almost guarantee it *won't* work for you!

To be clear, I fully expect Plait to be obsolete within 12 months. Either because one of the AI labs releases an AI-native GitHub that I feel is as good or better than Plait, or because the AI labs have made substantially more than just this workflow obsolete. For now, I'm enjoying it!

[^1]: Heavily vibecoded, but not entirely. I gave detailed guidance on all the UI and the actual semantics, and on several gritty technical decisions.
[^2]: Useful for debugging why a tend session didn't respect some part of its system prompt, for example.
[^3]: I don't need these often, but when I do, I *really* need them.
