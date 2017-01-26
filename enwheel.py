import subprocess
import semver
import pip
import os

from functools import partial
from itertools import groupby
from ConfigParser import SafeConfigParser
from glob import glob
from wheel.util import matches_requirement
from wheel.install import WheelFile

config=SafeConfigParser()
config.readfp(open('repos.ini'))

def git_ls_remote(repo):
    return subprocess.check_output(['git','ls-remote',repo])

def refs_with_prefix(ls_remote_output, prefix=''):
    for line in ls_remote_output.split('\n'):
        if line:
            try:
                hash, ref = line.split('\t')
                if ref.startswith(prefix):
                    remainder = ref[len(prefix):]
                    yield remainder 
            except ValueError:
                continue

def qualified_tags(tags,ignore_before):
    for tag in tags:
        try:
            semver.parse_version_info(tag)
        except ValueError:
            continue

        if semver.compare(tag,ignore_before) > 0:
            yield tag
        
def wheel_exists(name, version):
    req = "%s==%s" % (name, version)
    candidate_names = glob("simple/dist/%s-*.whl" % name)
    candidates = [WheelFile(name) for name in candidate_names]
    return bool(matches_requirement(req,candidates))

def build_wheel(repo,tag):
        pip.main(['wheel',"git+" + repo+"@"+tag,'-wsimple/dist'])

def wrap_html(code):
    return "<!DOCTYPE html> <html> <body>" + code + " </body> </html>"""

def write_package_html(name, wheels):
    dir_name = 'simple/%s/' % name
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    outfile = open(dir_name + 'index.html' , "wb")
    code = "<ul>"
    for wheel in wheels:
        url = os.path.relpath(wheel.filename, dir_name)
        label = os.path.basename(wheel.filename)
        code += '<li><a href="%s">%s</a></li>' % (url,label)

    code += "</ul>"
    document = wrap_html(code)
    outfile.write(document)

def write_index_html(package_names):
    outfile = open('simple/index.html', 'wb')
    code = "<ul>"
    for name in package_names:
        code += '<li><a href="%s">%s</a></li>' % (name, name)

    code += "</ul>"
    document = wrap_html(code)
    outfile.write(document)
     

def rebuild_html():
    all_wheels = (WheelFile(name) for name in glob("simple/dist/*.whl"))
    packages = groupby(all_wheels,lambda w: w.parsed_filename.groupdict()['name'])
    package_names = []
    for package_name, wheels in packages:
        package_names.append(package_name)
        write_package_html(package_name, wheels)

    write_index_html(package_names)

for section in config.sections():
    repo = config.get(section,'repo')
    if config.has_option(section, 'ignore-before'):
        ignore_before = config.get(section,'ignore-before')
    else:
        ignore_before = '0.0.0'

    refs_raw = git_ls_remote(repo)
    tags = refs_with_prefix(refs_raw, prefix='refs/tags/')
    for tag in qualified_tags(tags, ignore_before):
        if wheel_exists(section,tag):
            print "Wheel already exists for %s@%s" % (section,tag)
        else:
            build_wheel(repo,tag) 

rebuild_html()
