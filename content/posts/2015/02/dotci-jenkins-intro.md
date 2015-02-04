Title: JenkinsCI + dotCI = <3(?)
Date: 2015-02-04 21:00
Tags: JenkinsCI, CI, , dotCI,
Category: CI
Slug: dotci-jenkins-intro
Author: Kasper Jacobsen
Summary: -

This is part 1 of (atleast 3, hopefully 4) in a series of posts I'm going to be writing up on using the DotCI plugin with JenkinsCI. I realized while writing up another post (it'll be part 3 of this series) that this should be a series of posts or it's going to turn in to a very long rant looking wall of text.

I maintain the CI server and design deploy flows at Falcon Social, we use JenkinsCI and it's awesome. It has helped us come a long way already, with push-button deploys, pipelines and the works.

I've used TravisCI for open source projects at Falcon and my own projects all run tests with Travis, it's a great product, and the ease of use and setup it brings with it is pretty much unrivaled when comparing Travis to Jenkins.

DotCI is a project made by Groupon, it aims to make it *really* easy to test your code and push the result of the build to a GitHub commit so you can see the build status on the commit.

Of course you can achieve all these things with some manual work, but no one likes manual work, that's why we're in the automation business!

DotCI does a lot of interesting things, it requires a GitHub application to get a list of all your repos (it'll fetch your own and your organizations repos). Once you're authorized you can then select a repo from the dropdown list and create a build, doing that will enable a custom webhook on GitHub used for pushes and opening PR's.

Key features:

* GitHub integration
* Automatic building of jobs on pushes and opening PR's, basically what TravisCI does
* Clear separation of jobs by default
* Status on commits using the GitHub status API
* 3 build types
    * Docker
    * Dockerfile
    * install_packages (I won't be covering this one)

Great! So now we have something like TravisCI but for JenkinsCI users!

Stay tuned for part 2 - Getting JenkinsCI ready for DotCI
