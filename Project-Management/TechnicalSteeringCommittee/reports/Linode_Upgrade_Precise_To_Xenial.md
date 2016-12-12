Summary
-------

This document describes the process that will take place to migrate the Linode server from Ubuntu Precise Pangolin to Ubuntu Xenial Xerus.

Motivation
----------

The Linode server is currently running Ubuntu Precise Pangolin (12.04). This will reach EOL (end-of-life) in April 2017 and so will no longer
receive any further updates, security or otherwise. The server will be migrated to the latest LTS version of Ubuntu whose EOL date is April 2021.

Description
-----------

The Linode machine currently provides the following services:

* Wiki - www.mantidproject.org
* Static docs - docs.mantidproject.org
* Doxygen - doxygen.mantidproject.org
* Jenkins - builds.mantidproject.org
* Leeroy - builds.mantidproject.org:5000
* Forums - forums.mantidproject.org/help.mantidproject.org
* Download page - download.mantidproject.org
* Script repository downloading - download.mantidproject.org/scriptrepository
* Script repository upload - upload.mantidproject.org
* Instrument schema - schema.mantidproject.org
* External Data Central Repository - 198.74.56.37/ftp/external-data

Transition
==========

There are 2 approaches to take when upgrading the OS:

1. use the in-built `dist-upgrade` command to go `12.04`->`14.04`->`16.04`
2. stand up a new linode instance, perform the setup, swap IP addresses with the original and delete the old one.

The first approach requires 2 upgrade steps, introducing more risk into the process and might require just as much time if the upgrade goes
wrong and a clean setup is required anyway.

The second approach will allow more flexibility to keep existing services running and only have minimal downtime. Linode would charge `$80` at first
for a new instance but would refund any time until the end of the next billing cycle if it is deleted. This seems like the most sensible option
as it is very low cost and provides fallback.

### Common system packages required:

* `git`
* Java
* Docker

### Current ppa list:

Apt Configuration
-----------------

### Additions to `/etc/sources.list`

```
# Jenkins LTS repo
deb http://pkg.jenkins-ci.org/debian-stable binary/
```

### Additional files in `/etc/sources.list.d`:

### `docker.list`

```
deb https://get.docker.com/ubuntu docker main
```

### `git-core-ppa-precise.list`

```
deb http://ppa.launchpad.net/git-core/ppa/ubuntu precise main
deb-src http://ppa.launchpad.net/git-core/ppa/ubuntu precise main
```

### `longview.list`

```
deb http://apt-longview.linode.com/ precise main
```

### `webupd8team-java-precise.list`

```
deb http://ppa.launchpad.net/webupd8team/java/ubuntu precise main
deb-src http://ppa.launchpad.net/webupd8team/java/ubuntu precise main
```

### Nginx

It is proposed that Apache be replaced by [NGINX](https://www.nginx.com/resources/wiki/). NGINX provides better scalablity and places a lower
fooprint on the server.

### Wiki

A mediawiki site. The database settings are in the `LocalSettings.php` file. The DB will need to be exported and restored to the
new mediawiki instance. Other setup instructions for the bootstrap theme can be found at https://github.com/martyngigg/MantidWiki

Packages required from Ubuntu repositories for various extensions:

* `build-essential`
* `dvipng`
* `ocaml`
* `texlive-fonts-recommended`
* `texlive-lang-greek`
* `texlive-latex-recommended`

### Static Documenation (docs, doxygen)

Static HTML that can be served directly by Apache or NGINX.

### Jenkins

Self-contained package. The current configuration will need to be exported to the new instance.

This would be a good time to review the list of plugins that are in active use to try and reduce the memory
footprint and load time of Jenkins.

### Leeroy

Our Leeory fork lives at https://github.com/rosswhitfield/leeroy.

The current configuration will need to be backed up and transferred to the new instance.

### Forums

Discourse-based and setup is via a docker image. Instructions can be found at https://meta.discourse.org/t/move-your-discourse-instance-to-a-different-server/15721

### Download page

Another static site that can simply be served by NGINX.

### Script repository Download

Scripts live on GitHub at https://github.com/mantidproject/scriptrepository Apache points at a clone of the contents and the local copy is kept in sync by
http://builds.mantidproject.org/view/All/job/sync_scripts_download/

### Script repository Upload

Served by a WSGI application. Source code at https://github.com/mantidproject/upload.mantidproject.org.

The Apache configuration sets up the WSGI server and will need to be transferred to NGINX.

Requires:

* `python-httplib2`

### Instrument Schema

Apache points at the contents of https://github.com/mantidproject/mantid/tree/master/instrument/Schema

NGINX needs to be configured to serve this.

###  External Data

#### Download

External data is currently set to see `198.74.56.37/ftp/external-data/` as the base of the address for data downloads. It is pointed
at a directory that currently contains an MD5 directory will all of the files contained within it.

NGINX needs to be configured to server this.

#### Upload

Developers currently expect http://198.74.56.37/ftp/external-data/upload/ to point to a page to upload data files to the central repository.
The upload mechanism is supported by a small CGI application and the source code is sitting directly on the server.

NGINX needs to be configured to run this and also the code should be backed up in source control somewhere.
