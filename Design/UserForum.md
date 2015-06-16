Motivation
==========

Our current help system is limited and is not considered very effective. Some limitations are:

  * initial email contact is limited to small group of people
  * answers only get seen by the person sending the question
  * emails can be missed and then nothing ever happens

PMB has asked that we setup a forum and use this as our main communication with users. 

This document will not follow the usual design document format but will be used to track choices/decisions made about
various options.

Requirements
============
1. Can signup/signin without tremendous hurdles
2. Anonymous posting ????
3. Posts to mantid-help will have to be inserted (manually/automatically) (not so sure about this we can change where we direct people)
4. UI must be simple enough to not need (much) documentation
5. Price ???
6. Responsive from all mantid partner facilities

Options
=======

Vanilla Forums
--------------

http://vanillaforums.org

### Hosted Example
http://mantidtest.createaforum.com/

A bit restricted by the hosting platform.  Ad free for 30 days then $5pcm to stay add free.

### Self Hosted

* Open-source version does not have all PRO features
* Email hard to get working
* Looks poor out of the box

MyBB
----

http://www.mybb.com/

### Example
http://mantidtest.icyboards.net/

A bit restricted by the hosting platform.  Ad free cost is $10pcm.

Discourse
---------

http://www.discourse.org/

Sandbox that is reset daily - http://try.discourse.org/ 

### Hosted option

* Offer a one off install on DreamHost for $99 then monthly fee to Dreamhost. $10/$20 would be sufficient
* Other hosted packages are available at higher cost.

### Self hosted

* Open-source project and free version contains all features
* Simply Docker-based install with good documentation
* Options for login via GitHub, Google, Twitter, Facebook
* Supports pinned topics
* UI layout non-standard for forums but posts support 
  * code-highlighting
  * drag-n-drop image uploads
  * Markdown, HTML, BBcode
  * Inline previews
* Notification settings can be set after post is created. Not required to post - defaults operate like GitHub
* No anonymous posting
* example implementation is here - http://198.74.56.37:8081/ 


StackOverflow
-------------
Create a "mantidproject" tag.

https://stackoverflow.com/

Disqus
------

https://disqus.com/websites/
