A redesign of Mantid downloads
==================================

Motivation
----------

The background to this document is the formalisation and agreement of a redesign of the front and backend to the Mantid downloads page.

Current download system
------------------------------------

There are several notable issues with the current implementation of the downloads page, which include:

- Current webpage is hosted at ISIS, which makes updating difficult.
- No means of version control in place.
- Nightly builds are hosted at ISIS alongside the downloads pages.
- Manually counting the number of builds downloaded.
- Inconsistent styles used in relation to the main Mantid site.

Design proposal
------

A high-level summary of the design is that we will:

1. Leverage [jinja](http://jinja.pocoo.org/) as the backend templating engine. This allows includes of the Mantid wiki styles (for consistency), is lightweight and compliments sphinx.
2. Create a new repo on github to store the templates for the downloads website. This allows ease of updating and contribution amongst Mantid developers.
3. Host downloads _(releases, sample data, paraview, nightly builds)_ on sourceforge, and link to them directly in the webpage. This allows sourceforge to keep track of the download counters.
4. Completely redesign the frontend of the downloads page to ensure ease of use that makes use of modern techniques.
5. A `txt` file will be added that stores information for each release of Mantid. This will be used for the `latest release` on the downloads page, and all releases on the archives page.
6. The installation instructions for each Operating System of Mantid will be removed from the wiki and placed into this repo.
7. If a user is using an unsupported OS (Windows XP, Windows 32-bit, or < OSX 10.8) the `Latest release` will be changed (via JavaScript) to inform the user of this, and the most recent supported version of Mantid will be displayed for their OS.

### Nightly update

On the main Mantid downloads page a section will exist that provides users with the means of downloading the latest nightly build. A job will run that will update the URLS of each download link. This will be achieved by:

1. Jenkins nightly build job is run that outputs the names of each nightly build to a file (`nightlyNames.txt`).
2. A new job will be run for the downloads repo that will re-build and update the downloads page to include the new nightly URLS (by making use of `nightlyNames.txt`).

### Release update

At each release a `txt` file in the downloads repo will need to be updated to include the latest release information. This ensures that:

1. The _latest release_ on the main downloads page points to the correct sourceforge URL, and outputs the correct version (using the first item in the file).
2. The _archives_ page contains links to the correct sourceforge repos going back to as far as we have.

