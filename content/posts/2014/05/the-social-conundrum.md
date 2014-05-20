Title: The conundrum of social coding
Date: 2014-05-20 20:00
Tags: social coding, python, semantic versioning,
Category: coding
Slug: the-conundrum-of-social-coding
Author: Kasper Jacobsen
Summary: -

A month and a half ago I started a new project.

I was looking for a way to easily bump the version on a project I am working on at Falcon Social. It's a problem I've run into before and since I had a few hours I started looking around for a python module that I could wrap a CLI-ish interface around and bump the version of the project before I pushed it to our GitLab servers and deploy it.

I had met the same problem during development of a NodeJS application last year and hadn't found a solution yet.

So I did what any other developer with a few spare hours on their hands would do - I started building my own, I never intended for it to become anything else than that, and I am not sure I want it to, still. So I get to a state where the module does what I want it to, an initial working state or an alpha if you will ([#2442ed0](https://github.com/Dinoshauer/SemVerPy/commit/2442ed0cbbcc935032ba8a634ef08be3c77a10bb)).

I leave it for the night and revisit it in the morning, showing it to my colleague and he starts suggesting improvements, talking about what could and should be done, and I think, yeah, he has some valid points. I get back to work and the module completely leaves my mind and a few days later he pokes me, saying didn't you see my pull requests? I disabled notifications from GitHub back when Falcon Social was hosting it's code on GitHub, because I got sick of all the email notifications from the pull requests I was not actually a part of. I never thought to check the [repo](https://github.com/Dinoshauer/SemVerPy), so I get on GitHub and, hey, presto! There are several pull requests there, waiting on me to review and comment on them, from my colleague. He had as well found himself with a few hours to spare and an intention to improve on my module.

So as it is now, he owns 90% of he commits on the repo (I haven't done the math or anything), and a few weeks ago, a third person had actually checked out the module because he was working on a module for semantic versioning as well and he had found that the module wasn't completely compliant with the [semantic version standard](http://semver.org/), and he thought it'd be a nice idea to join forces with us and develop a better, more feature-complete module for semantic versioning, sort of missing the point of my module (I am very grateful for the though, and if it had not turned out that there was a module that did what he was aiming to do, only better already we probably would have been coding on it together), as I only intended it for bumping versions, not the same validation as the other modules provide, although it can sort of do that now, thanks to my colleague.

