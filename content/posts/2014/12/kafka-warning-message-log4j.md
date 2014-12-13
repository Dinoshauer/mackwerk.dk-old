Title: Kafka's warning message about log4j
Date: 2014-12-13 09:00
Tags: Kafka, Apache Kafka, Log4J, Kafka-0.8.1.1
Category: ops
Slug: kafka-warning-message-log4j
Author: Kasper Jacobsen
Summary: -

TL;DR - This will probably fix your problem.

    wget http://www.slf4j.org/dist/slf4j-1.7.7.tar.gz
    tar -zxf slf4j-1.7.7.tar.gz
    cp slf4j-1.7.7/slf4j-nop-1.7.7.jar kafka/core/build/dependant-libs-2.8.0/

I've been tinkering with setting up Kafka a lot these days and whenever I ran
one of the ``.sh`` scripts inside Kafka's ``bin`` folder it would start with
something like this:

    SLF4J: Failed to load class "org.slf4j.impl.StaticLoggerBinder".
    SLF4J: Defaulting to no-operation (NOP) logger implementation
    SLF4J: See http://www.slf4j.org/codes.html#StaticLoggerBinder for further details.

Ás you can read from the output, it's not really that big of a deal when you're
just running benchmarks etc. But it still annoyed me enough to try and find the
solution to the problem.

I eventually landed on [this page][1] that tells you, that you need to download
the log4j jars yourself and put them in the ``lib`` directory of your kafka root.

I've been using Kafka 0.8.1.1 and it seemed that didn't work out very well, I
don't know if the ``lib`` directory is not in Kafka's classpath or whatever
(not too experienced with Java). So I started looking around in the
``bin/kafka-run-class.sh`` script that  every other script wraps and it was
creating the classpath in there. So here's what I did with my log4j files:

    wget http://www.slf4j.org/dist/slf4j-1.7.7.tar.gz
    tar -zxf slf4j-1.7.7.tar.gz
    cp slf4j-1.7.7/slf4j-nop-1.7.7.jar kafka/core/build/dependant-libs-2.8.0/


[1]: http://yaohuangportal.wordpress.com/2014/06/24/kafka-console-producer-sh-kafka_2-10-0-8-1-reported-slf4j-failed-to-load-class-org-slf4j-impl-staticloggerbinder/
