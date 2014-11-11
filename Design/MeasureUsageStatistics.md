Overview
--------
There is an open question as to what operating systems users have when running mantid. This design is intended to address that question. There are two services described below. The first is one for logging unique startups of mantid with information on what operating system and version of mantid. This utility will leave room for being extended for additional usage information (e.g. GUIs used) and allow for opting out of sending statistics. The second service will provide information on the recent versions of mantid (version number and download url). Both services should be implemented using [RESTful desgn principles](https://restful-api-design.readthedocs.org/en/latest/).

Usage Statistics
----------------
The usage statistics will be sent by an algorithm that creates a separate thread to get system information and send information through the network. The algorithm will have additional properties to supply additional information (e.g. GUIs used). In order to have useful statistics there will be a unique key. The unique key will be a hash made from the user name and the mac address (or ip address) of the system. The other information that will be sent are operating system (name, version, byte size), startup date/time, and version of mantid. This information should allow for a better statistics of what operating systems are used than the [sourceforge downloads](http://sourceforge.net/projects/mantid/files/3.2/stats/timeline).

An example is to have a `POST` request to a url with the following document.
```json
{
  "uid": "1d621f60d4ba72f9efb0a1172bbc3328",
  "getOSName": "???",
  "getOSArchitecture": "???",
  "getComputerName": "???",
  "getOSVersion": "???",
  "ParaView": "true",
  "mantidVersion": "3.2.1",
  "mantidSha": "8223fbc53f5f8d8be259d675171439a648f93183"
}
```

Latest Version
--------------
It would be useful to have a web service that provided the latest versions and download URLs (usable in wget). This would be a programatic version of information currently available [on sourceforge](http://sourceforge.net/projects/mantid/files/3.2/).

An example is to have a `GET` request to a url with the following returned.
```json
{
  "collection": [
    {
      "version": "3.2.1",
      "links": [
        {
          "os": "win64",
          "url": "http://sourceforge.net/projects/mantid/files/3.2/mantid-3.2.1-win64.exe/download"
        },
        {
          "os": "osx",
          "url": "http://sourceforge.net/projects/mantid/files/3.2/mantid-3.2.1-MountainLion.dmg/download"
        },
        {
          "os": "rhel6",
          "url": "http://sourceforge.net/projects/mantid/files/3.2/mantid-3.2.0-1.el6.x86_64.rpm/download"
        },
        {
          "os": "ubuntu10.04",
          "url": "http://sourceforge.net/projects/mantid/files/3.2/mantid_3.2.1-1_amd64.deb/download"
        }
      ]
    },
    {
      "version": "3.2.0",
      "links": [
        {
          "os": "win64",
          "url": "http://sourceforge.net/projects/mantid/files/3.2/mantid-3.2.0-win64.exe/download"
        }
      ]
    }
  ]
}
```
