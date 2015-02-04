Title: JenkinsCI + dotCI - Setup
Date: 2015-02-04 21:50
Tags: JenkinsCI, CI, dotCI,
Category: CI
Slug: dotci-jenkins-setup
Author: Kasper Jacobsen
Summary: -

*This is part 2 in a series of posts on DotCI and JenkinsCI.*

[DotCI][1] has a few requirements, besides Jenkins:

* [Docker][2] - For keeping build environments separate.
* [MongoDB][3] - For keeping track of builds. Build history is stored in MongoDB

I'm going to quickly go through installing both docker and MongoDB on an ubuntu 14.04 EC2 instance, however these instructions are pretty universal for any debian distro.

## Installing docker

Installing docker is easy, there are a couple of ways:

1. the docker version that ubuntu provides by default (`docker.io`)
2. docker manages a package repository themselves, which they keep up to date with the latest docker releases (`lxc-docker`)

We're going to go with docker's own repo, that way we are up to date with the latest release.

Docker kindly provides a guide with installation instructions for both methods [here][2-1], be sure to scroll down the page to get to the `lxc-docker` parts. I'll outline the steps here as well:

**Lazy (and you're-not-really-sure-what's-happening-way-but-hey-it's-automatic):**

    $ curl -sSL https://get.docker.com/ubuntu/ | sudo sh

**Better:**

    $ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9
    $ sudo sh -c "echo deb https://get.docker.com/ubuntu docker main > /etc/apt/sources.list.d/docker.list"
    $ sudo apt-get update
    $ sudo apt-get install lxc-docker

Now you will have docker installed and the daemon running! Great success! But we're not quite done yet. Docker commands needs to be run with `sudo` on ubuntu out-of-the-box, DotCI doesn't do that, so we are going to add the `jenkins` user to the `docker` group, allowing docker commands to be run from Jenkins.

    $ usermod -aG docker jenkins

Now we're all set up to use `docker` commands with Jenkins!

If you are using a private docker repository now would be a good time to

    $ sudo su - jenkins
    $ docker login

## Installing MongoDB

If you thought installing docker was easy you're in for a treat. MongoDB is just as easy! [Look here for instructions.][3-1]

The same goes for MongoDB, ubuntu provides some packages and MongoDB provides some newer, up to date packages.

* Ubuntu's own packages are called mongodb*
* MongoDB's packages are called mongodb-org*

MongoDB doesn't provide a script that you can download and run automatically, so I'm just going to outline the steps here again for reference:

    $ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
    $ sudo sh -c "echo deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen > /etc/apt/sources.list.d/mongodb.list"
    $ sudo apt-get update
    $ sudo apt-get install mongodb-org

MongoDB is now running, there are no extra setup steps for Jenkins to access the database.

Stay tuned for part 3! Using DotCI with private repositories.


[1]: https://github.com/groupon/dotCI                                       "DotCI @ GitHub"
[2]: https://docker.io/                                                     "Docker"
[2-1]: https://docs.docker.com/installation/ubuntulinux/                    "Docker installation guide"
[3]: https://www.mongodb.org/                                               "MongoDB"
[3-1]: http://docs.mongodb.org/manual/tutorial/install-mongodb-on-ubuntu/   "MongoDB installation guide"
