import os

from itertools import groupby
from glob import glob

from wheel.install import WheelFile


def wrap_html(code):
    return "<!DOCTYPE html> <html> <body>" + code + " </body> </html>"""


def write_package_html(name, wheels):
    dir_name = 'simple/%s/' % name
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    outfile = open(dir_name + 'index.html', "wb")
    code = ""
    for wheel in wheels:
        url = os.path.relpath(wheel.filename, dir_name)
        label = os.path.basename(wheel.filename)
        code += '<a href="%s">%s</a><br/>' % (url, label)

    document = wrap_html(code)
    outfile.write(document)


def write_index_html(package_names):
    outfile = open('simple/index.html', 'wb')
    code = ""
    for name in package_names:
        code += '<a href="%s">%s</a><br/>' % (name, name)

    document = wrap_html(code)
    outfile.write(document)


def rebuild_html():
    all_wheels = (WheelFile(name) for name in glob("simple/dist/*.whl"))
    packages = groupby(all_wheels, lambda w:
                       w.parsed_filename.groupdict()['name'])
    package_names = []
    for package_name, wheels in packages:
        package_names.append(package_name)
        write_package_html(package_name, wheels)

    write_index_html(package_names)
