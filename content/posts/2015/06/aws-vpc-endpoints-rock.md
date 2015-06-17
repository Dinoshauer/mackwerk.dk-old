Title: AWS VPC Endpoints rock
Date: 2015-06-16 22:00
Tags: AWS, VPC, cloud,
Category: Cloud
Slug: aws-vpc-endpoints-rock
Author: Kasper Jacobsen
Summary: -

I am managing one of our VPCs at work, it is the largest in our setup.

It has a private route table and a public one, the private route table has a
NAT instance connected as its Internet Gateway.

The NAT is running on a tiny `t2.micro` which has very limited network
throughput, ~`50 Mbps` if I remember correctly. Feel free to correct me!

We have a little over `12 TB` of data in our Elasticsearch cluster, and I
needed to snapshot the cluster onto S3, so I started snapshotting without
thinking about the poor NAT and the network got congested immediately.

![Network out]({attach}/images/network-out.png)

Every operation became unbearable, `ansible` playbooks started failing due to
timeouts when updating or deploying packages etc.

Recently, Amazon released a new feature called [VPC Endpoints][1]. It enables a
machine in a private route table to speak to other Amazon services (currently,
only S3) using their private IP, meaning that the bottleneck for calling the
S3 API is no longer the poor little NAT, but the instances network card.

It's really easy to set up, and very transparent, the whole thing is handled
internally by Amazon, so all you have to do is create the endpoint and add it
to your route tables (make sure you're not running any critical S3 operations
beforehand though).

[1]: https://aws.amazon.com/blogs/aws/new-vpc-endpoint-for-amazon-s3/
