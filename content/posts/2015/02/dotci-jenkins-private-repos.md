Title: JenkinsCI + dotCI + Private repos = \o/
Date: 2015-02-08 18:25
Tags: JenkinsCI, CI, dotCI,
Category: CI
Slug: dotci-jenkins-private-repos
Author: Kasper Jacobsen
Summary: -

*This is part 3 in a series of posts on DotCI and JenkinsCI.*

One of the first things I ran into after setting up DotCI on a Jenkins instance
was that I couldn't get the plugin to clone our private repositories. This is
because repos are cloned with ``https`` inside the docker container so there is
no credentials for git to use.

It seems DotCI has tried to remedy this by using deploy keys, but for some reason
they do not work. [@joeandaverde][1] opened a [ticket regarding this issues][2]
and found a work around, by adding a file called ``.git-credentials`` to the
home directory of the user running the ``git clone`` command and then adding a
``.gitconfig`` that tells git to look in this file for credentials.

The good thing about this way is that you can use an OAuth token instead of
exposing your password in a plain-text file.

The bad thing about this is that, you're exposing your OAuth token in a plain-
text file. I'd recommend to not commit this file into your SCM, and to keep the
docker image in a private docker repository as well, minimizing the risk of
people getting their hands on your OAuth token.

After almost pulling my hair out, I found a guy on GitHub who had made
repositories while testing out DotCI the same way I've been doing, and his work
has been much help for this particular step! Check out [@glogiotatidis][3].

I based the base image in this post on his [DotCI Base Test Runner][4] image.

Let's get started.

Here's my file-layout for the base image:

    tree ~/dotci/base/
    ├── docker
    ├── Dockerfile
    ├── gitconfig
    └── git-credentials

We'll go through it one file at a time. Let's start at the top.

* **docker**: This file overwrites the docker command inside your docker
    container. All it does is that it adds a ``.git`` folder to the
    ``.dockerignore`` file so docker won't spend time copying git files to
    another container. **NOTE:** It's only really valuable to use if
    you're going to be using the ``Dockerfile`` style builds with DotCI

```
    cat ~/dotci/base/docker
    #!/bin/bash

    # Source:
    # https://github.com/glogiotatidis/dotci-base-docker-image

    if [ "$1" == "build" ];
    then
        if [ ! -z $2 ];
        then
            echo ".git" >> "${@: -1}"/.dockerignore
            find "${@: -1}" | xargs touch -t 201401010000.00
        fi
    fi

    /bin/docker "$@"
```

* **Dockerfile**: Here's where all the magic happens. We build from the debian
    image, because it's smaller than the ubuntu one and it can still get all
    the things we need.

    1. Update and install git as this is our only dependency in the base image,
        clean apt caches so they don't take up image space and are also
        invalidated
    2. Then we copy in our resources

```
    cat ~/dotci/base/Dockerfile
    FROM debian:stable

    RUN apt-get update \
        && apt-get -y install git \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*

    COPY docker /usr/local/bin/docker
    COPY git-credentials /root/.git-credentials
    COPY gitconfig /root/.gitconfig
```

* **gitconfig**: This is the file that will tell ``git`` to look for
    credentials in a file. Crucial!

```
    cat ~/dotci/base/gitconfig
    [credential]
        helper = store
```

* **git-credentials**: The credentials file, remember: Bad idea to commit this
    file to your SCM!

```
    cat ~/dotci/base/git-credentials
    https://<OAUTH-TOKEN>:x-oauth-basic@github.com
```

Now that you've got your base image you can create images inheriting from this
one for all your needs, and you're able to clone private repositories!

Many thanks to my colleague [@Tenzer][5] for his great help with this step.

Stay tuned for [part 4](../dotci-jenkins-publish-archive)! Running jobs and
archiving artifacts and publishing test results.

[1]: https://github.com/joeandaverde                            "Joe Andaverde @ GitHub.com"
[2]: https://github.com/groupon/DotCi/issues/103                "Unable to authenticate with private Github repo - fails build every time #103"
[3]: https://github.com/glogiotatidis                           "glogiotatidis @ GitHub"
[4]: https://github.com/glogiotatidis/dotci-base-docker-image   "glogiotatidis @ DotCI Base Test Runner"
[5]: https://twitter.com/tenzer                                 "Tenzer @ Twitter"
