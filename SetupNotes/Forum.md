Forum/Help Setup Notes
======================

[Discourse](http://www.discourse.org/) was [chosen](https://github.com/mantidproject/documents/blob/master/Project-Management/TechnicalSteeringCommittee/meetings/2015/TSC-meeting-2015-07-07.md)
as the system to host the Mantid help forum. This document describes the current setup on the mantidproject Linode.

Installation
------------

Discourse has a docker-based installation. The [setup instructions](https://github.com/discourse/discourse/blob/master/docs/INSTALL-cloud.md) assume the installation on a new
Dreamhost VM but the sections from [here](https://github.com/discourse/discourse/blob/master/docs/INSTALL-cloud.md#install-docker--git)
onwards are general.

Mailserver
----------

We use http://mandrill.com as our transactional email service. The login details are with TSC members.
