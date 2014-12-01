# Download directory restructure

Below is the name of each filename/directory on downloads.mantidproject.org, a brief description of it, and the verdict of the usefulness of the file/dir.

* * *

**algorithm_screenshots/**

- **Description:** A directory of automatically generated screenshots.
- **TODO:** _Remove_ as these screenshots will be automatically generated in the new sphinx wiki documentation.

* * *

**Archive Releases/**

- **Description:** Very old build release notes (1.0.1449 to 1.0.2887).
- **TODO:** _Remove_ - As these are just release notes, and we do not plan to show release notes for ALL builds on the downloads archive page, (as we will host from 2.0 on SourceForge).

* * *

**debs/**

- **Description:** Contains `iPython` debian builds.
- **TODO:** _Remove_ - This does not seem to be used on the Mantid site.

* * *

**dev/**

- **Description:** Contains the generated HTML for the downloads page. This was uploaded to show what the site would look like.
- **TODO:** _Remove_ - This should be re-generated and uploaded to the root of downloads.mantidproject.org.

* * *

**docs/**

- **Description:** The automatically generated Sphinx Python documentation. This is _out-dated_, and can be found: [here](http://download.mantidproject.org/docs/current-release/python/html/changes.html)
- **TODO:** _UNDECIDED_ - If it is kept, we should update the layout/style to be similar to the main wiki.

* * *

**Documentation.zip**

- **Description:** Contains four `PDF` documents (Mantid SANS, MantidPlot Reference, MantidConcepts, MantidAlgorithms).
- **TODO:** _UNDECIDED_ - These should be moved to the document repo (or the relevant .tex instead, if it exists). This would free up space, and put them where they belong.

* * *

**google627bc235caa86225.html**

- **Description:** Used to verify Google webmasters account.
- **TODO:** _Remove_ - Once an account is verified, the related file (or HTML inserted) can be removed. As this is an old verification code, it should be removed.

* * *

**index2.psp, index.psp, jquery-1.10.2.min.js,
python25.psp, python27v1.psp, python27v2.psp, oldindex.psp,
VatesDownload.psp, images/, favicon.ico, download.psp,
showlog.psp, style1.css, logs**

- **Description:** Files relating to the old download page.
- **TODO:** _Remove_ - They are not used/required by the new download page, and should be removed.

* * *

**SampleData/**

- **Description:** Contains the sample data that exists on the downloads page.
- **TODO:** _Remove_ - This is no longer required as the sampleData now exists on sourceForge, and is linked in the new downloads page.

* * *

**sandbox/**

- **Description:** Contains some toy JavaScript examples
- **TODO:** _Remove_ - These are old examples, so should be removed.

* * *

**scriptrepository/**

- **Description:** Appears to be an outdated clone of the Mantid [scriptrepo](https://github.com/mantidproject/scriptrepository)
- **TODO:** _Remove_ - If unusaged, this should be removed..

* * *

**vcsetup.exe**

- **Description:** Appears to be a visual studio (vs?) installation file.
- **TODO:** _Remove_ - This appears to be unused.

* * *

**kits/**

- **Description:** Contains releases of Mantid (and the release notes) as far back as 1.0.3187.
- **TODO:** _UNDECIDED/REMOVE_ - We currently go back to Mantid 2.3 on the new downloads site, and SourceForge. I recommend removal of all versions (>=2.3), and instead host all older versions in a directory (as is down). This reduces the amount of files hosted.

* * *

**build_metrics/**

- **Description:** Contains several `.psp` files that provide a Mantid build report. This would no longer be required as we plan to use SourceForge for these statistics. This also appears to interact with and query Trac.
- **TODO:** _UNDECIDED/REMOVE_ -  I'm not sure how often this is used, but likely should be removed.

* * *

**CurrentBuild/**

- **Description:** Appears to be a visual studio (vs?) installation file.
- **TODO:** _Remove_ - This appears to be unused.

* * *

**master_builds/**

- **Description:** Contains a `json` file named `repository.json`.
- **TODO:** _UNDECIDED_ - I'm not sure what this file is used for.

* * *

**Development Releases/**

- **Description:** Contains various nightly builds from Jenkins jobs. There are 23 `.exe` files. As we hold the latest nightly version on SourceForge (which is also noted on the new downloads page) then these files are unused and taking up space.
- **TODO:** _UNDECIDED/REMOVE_ - If it's agreed that these files are unused, then they should be removed.

* * *

**prerequisites/**

- **Description:** Various `qt` `.zip` files for the, and `numpy/Python` for `Windows`.
- **TODO:** _UNDECIDED_ - This appears to be unused.

* * *

**msvcp71.dll**

- **Description:** This `dll` appears to be a `Microsoft C Runtime Library file`.
- **TODO:** _UNDECIDED_ -  I'm not sure why this is currently on the server, but likely should be removed.

* * *

**MuonSchool/**

- **Description:** Three Mantid installation files (.exe, .dmg, .deb) and an XML file.
- **TODO:** _Remove_ - These were likely used once at the Muon School, and won't be used again.

* * *

**useful files/**

- **Description:** This directory contains a file (VMS Prog Dump), which appears to be an OpenVMS backup.
- **TODO:** _UNDECIDED_ - I'm not sure of the usefullness of this file.

* * *

**videos/**

- **Description:** Various tutorial style videos for Mantid, for example, installation. This folder also contains various sub-folders that contain presentations. These should be uploaded to the documents repo, then removed from this folder.
- **TODO:** _UNDECIDED_ - I'm not sure of the usefullness of this file.

* * *

**webmailer/**

- **Description:** Appears to be an _old_ `PHP` form for emailing help/bugs (see: [here](http://download.mantidproject.org/webmailer/index.php))
- **TODO:** _Remove_ - As this is no longer used (I believe), it should be removed.

* * *
