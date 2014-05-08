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

Workflow
------

### Nightly release

1. A jenkins job is run nightly that outputs the names of each nightly build to a file (`nightly.txt`) and then pushes this file to the downloads repo.
2. A new job is run for the downloads repo that will re-build it and update the downloads page to include the new nightly URLS (obtained from `nightly.txt`) once the repo is changed.

### Release update

1. Developer `clones` the download repo _or_ updates their local copy.
2. Developer runs `create-manifest.py` with the release version number. This generates a new file in the `releases` folder with the corrosponding version, e.g.

    python tools/create-manifest.py 3.2

3. Developer runs `python tools/build-site.py` to generate the static site. This script uses the files in the `releases` folder to popular the _latest release_ information, and the _archives_ page.
4. Once the developer verifies the contents of the static site is correct (e.g. all download links work correctly) they add the release file generate above (`git add releases/*`)
5. They then commit the change made and push it to origin. Once modified a jenkins job is ran that re-builds the site on the Mantid server.

Folder structure
------

The proposed folder structure of the repo is:

	.
	├── README.md
	│
	├── releases
	│   ├── nightly.txt
	│   ├── 3.1.1.txt
	│   ├── ... other releases ...
	│   └── 1.0.txt
	│
	├── static
	│   ├── css
	│   │   └── main.css
	│   ├── img
	│   │   └── icon.css
	│   └── js
	│       └── main.css
	│
	├── templates
	│   ├── base.html
	│   ├── archives.html
	│   ├── instructions.html
	│   └── downloads.html
	│
	└── tools
		├── build-site.py
		└── create-manifest.py
