#!/usr/bin/python3
# Generate .tgz archive from the contents of the web_static

from fabric.api import local
from datetime import datetime


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder"""

    local("mkdir -p versions")

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = "versions/web_static_{}.tgz".format(timestamp)

    result = local("tar -cvzf {} web_static".format(filename))

    if result.succeeded:
        return filename
    else:
        return None
    