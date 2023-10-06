#!/usr/bin/python3
# Fabric script for deploying web_static to web servers

"""Fabric script for deploying web_static to web servers"""
from fabric.api import env, put, run
from os.path import exists

env.hosts = ['52.3.244.240', '52.91.146.187']
env.user = 'ubuntu'  # Update with your SSH username


def do_deploy(archive_path):
    """
    Distributes an archive to web servers

    Parameters:
    archive_path (str): The path to the archive

    Returns:
    bool: True if all operations were successful, False otherwise
    """

    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web servers
        put(archive_path, "/tmp/")

        # Get the base name and file name without extension
        base_name = archive_path.split("/")[-1]
        file_name = base_name.split(".")[0]

        # Create the destination folder on the web servers
        dest_path = "/data/web_static/releases/{}/".format(file_name)
        run("mkdir -p {}".format(dest_path))

        # Uncompress the archive to the destination folder
        run("tar -xzf /tmp/{} -C {}".format(base_name, dest_path))

        # Delete the archive from the web servers
        run("rm /tmp/{}".format(base_name))

        # Copy files to the web_static/releases folder instead of moving them
        run("cp -r {0}web_static/* {0}".format(dest_path))

        # Delete the symbolic link from the web servers
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link on the web servers
        run("ln -s {} /data/web_static/current".format(dest_path))

        # Check if the link was successfully updated
        current_link = run("readlink -f /data/web_static/current")
        if current_link == dest_path:
            print("New version deployed!")
            return True
        else:
            return False

    except Exception:
        return False
    