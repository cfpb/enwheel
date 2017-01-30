# enwheel

Starting with a file describing a set up git-hosted Python packages, generate
wheels and a PEP 503-compatible package repository.

The list of source packages looks like this, and is always called 'repos.ini':

This is a single-entry repos.ini that downloads all Django releases after 1.10.0:

```
[Django]
repo: https://github.com/django/django.git
ignore-before: 1.10.0
```

## Dependencies

This has not yet been tested with Python 3. Python dependencies are listed in
setup.py

## Installation

`pip install enwheel`


## Usage

```
Usage:
    enwheel build  (build all software listed in repos.ini)
    enwheel build <name> (build just one package, by name in repos.ini)
    enwheel generate  (refresh the Python repository at /simple/)
    enwheel serve [--port=8000] (start a toy web server hosting the contents of /simple/)
```

## Known issues

- We presume that the setup.py version will always reflect the git tag. For example
building Django at tag 1.10.2 will produce a Django wheel with version 1.10.2
- Capitalization in repos.ini matters, names must match the 'name' in setup.py
- We only process tags with valid, 3-part semantic versions, and no other text.
1.10.2 is valid, v.1.10.2 isn't.


## Getting involved


See [CONTRIBUTING](CONTRIBUTING.md).


----

## Open source licensing info
1. [TERMS](TERMS.md)
2. [LICENSE](LICENSE)
3. [CFPB Source Code Policy](https://github.com/cfpb/source-code-policy/)
