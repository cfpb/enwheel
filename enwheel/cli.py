"""
enwheel

Usage:
    enwheel build
    enwheel build <name>
    enwheel generate
    enwheel serve [--port=8000]

Options:
    --port=PORT  port to serve on [default: 8000]
"""
import semver

from ConfigParser import SafeConfigParser
from glob import glob

import pip

from docopt import docopt
from wheel.util import matches_requirement
from wheel.install import WheelFile

from enwheel.git import tags_for_repo
from enwheel.html import rebuild_html
from enwheel.server import serve_command


def filter_tags(tags, ignore_before):
    for tag in tags:
        try:
            semver.parse_version_info(tag)
        except ValueError:
            print "%s is not a valid semantic version" % tag
            continue

        if semver.compare(tag, ignore_before) >= 0:
            yield tag

        else:
            print "%s < %s, ignoring" % (tag, ignore_before)


def wheel_exists(name, version):
    req = "%s==%s" % (name, version)
    candidate_filenames = glob("simple/dist/%s-*.whl" % name)
    candidates = [WheelFile(filename) for filename in candidate_filenames]
    return bool(matches_requirement(req, candidates))


def build_wheel(repo, tag):
        pip.main(['wheel', "git+" + repo+"@"+tag, '-wsimple/dist'])


def build_wheels_for_name(name, config):
    repo = config.get(name, 'repo')
    if config.has_option(name, 'ignore-before'):
        ignore_before = config.get(name, 'ignore-before')
    else:
        ignore_before = '0.0.0'

    tags = tags_for_repo(repo)

    has_candidates = None

    for tag in filter_tags(tags, ignore_before):
        has_candidates = True
        if wheel_exists(name, tag):
            print "Wheel already exists for %s@%s" % (name, tag)
        else:
            build_wheel(repo, tag)

    if not has_candidates:
        print "no candidate tags for %s" % name


def build_command(**kwargs):
    config = SafeConfigParser()
    config.readfp(open('repos.ini'))

    requested_name = kwargs.get('<name>')

    if requested_name:
        to_build = [kwargs.get('<name>')]
    else:
        to_build = config.sections()

    for name in to_build:
        build_wheels_for_name(name, config)


def main():
    arguments = docopt(__doc__)
    if arguments['build']:
        build_command(**arguments)
        rebuild_html()

    elif arguments['generate']:
        rebuild_html()

    elif arguments['serve']:
        serve_command(**arguments)


if __name__ == '__main__':
    main()
