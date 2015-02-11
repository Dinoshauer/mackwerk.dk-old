Title: JenkinsCI + dotCI + Tests = <3(!)
Date: 2015-02-11 22:40
Tags: JenkinsCI, CI, dotCI,
Category: CI
Slug: dotci-jenkins-publish-archive
Author: Kasper Jacobsen
Summary: -

*This is part 4 in a series of posts on DotCI and JenkinsCI.*

In the past posts we've had a quick gander at

* Installing MongoDB, Docker and setting up the DotCI plugin
* Creating a `Dockerfile` that enables us to clone private repos

So, we've got JenkinsCI all set up with DotCI and ready to run our tests.

First of all we need a `.ci.yml` file in the root of our project, this is the
file that the DotCI plugin will look for, parse and execute the instructions
from.

``.ci.yml``:

```YAML
image: docker.example.com/dotci/python3.4:c6704aa
run_params: "-v `pwd`:/output"
command:
  - pip install -r requirements.txt
  - py.test test.py --junitxml=/output/test-report.xml
```

I'll quickly walk through the parameters of the ``.ci.yml`` file here:

* ``image``: This option tells DotCi which docker image to use
    * **Note:** Don't use the ``latest`` tag as DotCi won't pull changes
      automatically
* ``run_params``: This option is **mandatory**
    * It tells docker to mount JenkinsCI's filesystem in the ``/output`` path
      (I'll get back to this part in a bit)
* ``command``: This option is a list
    * You simply add one command per list item
    * if a list item fails, the entire build will fail

This is a very simple example of a `.ci.yml`. You can read more about this spec
on [DotCI's repo][1], let's walk through it.

* We define which Docker image we want to run our commands in
* We tell docker to mount our current working directory in the `/output`
  folder inside the container
    * I'm doing this because I couldn't figure out how the [`plugins`][2]
      directive worked, so I collect the results in the Jenkins job
      configuration instead, more on this later on.
* Here comes the magic and all the fun bits and pieces. The `command` directive
  is a long list of all the commands you want the build to run, if any of the
  commands exit with a non-zero exit code the job will terminate and fail

So, that's our super simple ``.ci.yml`` file. **Let's move on to Jenkins!**

As you have probably noticed after installing the DotCI plugin a new item has
appeared in the sidebar: ``New DotCi Job``, this is the link you will want to
use when activating/creating new builds for DotCI from now on.

When you click on it the first time you'll be taken to GitHub's application
authentication page asking you to authenticate your application.

**Note!** If you're not being asked about access to private repos, go back and
head into the Jenkins system settings, tick off the private repo support
checkbox, save and start over.

Find your project in the list and activate it.

The job's main page has also changed, the build history is now taking up the
main part of the page, and there are tabs for *special* builds.

* All
* Mine - Builds triggered by you, by either push or manually triggered
* Master - All builds off the master branch

Triggering a build manually will let you select a branch from a dropdown,
populated with your projects branches (*very* nice feature!).

Run a build and see what happens, right now no test results will be recorded,
as you have to set that up in the job config. Go have a cup of coffee though,
as it's the first time Jenkins is building the job it most likely won't have
the docker image downloaded already.

So, your build finished successfully! Awesome, let's get some test results etc
recorded. Since we've mounted the container in the root of our workspace
test results will be available there as well.

Enable the the ``Publish JUnit test result report`` post-build action, if you
don't feel like being specific about it you can just put in ``*.xml``.

Save you build, and trigger a new one. This time, don't go for a cup of coffee
as your build will likely finish much faster this time as you will only have to
your ``command`` steps now, lean back and watch the build render these two
glorious lines of text!

    Recording test results
    ...
    setting commit status on Github for https://github.com/example/dotci-text/commit/d64a34aff2779f2a5bb1096803e0bb39ca001ab8

We've done it! DotCI is now running our instructions inside a docker container,
Jenkins is recording our test results and a commit status is even set on our
commit on GitHub!

**SUCCESS!**

Remember how I mentioned earlier that I couldn't figure out how to get the
plugins to work inside the container? Well, if you know how to or have figured
it out, please [open an issue][3] or [open a pull request][4] on the repo
hosting this site and let me know!

I already created an issue on the [DotCI-Plugins issuetracker (#3)][4] asking
for help, I'll be sure to update this page when I learn more.

Stay tuned for part 5! Quirks and retrospective.

[1]: https://github.com/groupon/dotci                                   "DotCI @ GitHub"
[2]: https://github.com/groupon/DotCi-Plugins-Starter-Pack              "DotCI-Plugins @ GitHub"
[3]: https://github.com/dinoshauer/mackwerk.dk/issues                   "Open issues @ mackwerk.dk"
[4]: https://github.com/dinoshauer/mackwerk.dk/pulls                    "PR @ mackwerk.dk"
[5]: https://github.com/groupon/DotCi-Plugins-Starter-Pack/issues/3     "Issue #3"
