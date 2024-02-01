#!/usr/bin/python3
"""
Fabric file
"""
from datetime import datetime
import os
from fabric.api import local, run, put, env

env.hosts = ["18.234.105.201", "100.26.162.114"]
env.user = "ubuntu"
env.key_filename = '/AirBnB_clone_v2/my_key'


def do_pack():
    """
    method that generate a .tgz archive
    """
    try:
        if os.path.isdir("versions") is False:
            local("mkdir versions")

        date = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_name = f" versions/web_static_{date}.tgz"

        local("tar -cvzf {} web_static".format(archive_name))
        return archive_name
    except CommandFailed:
        return None


def do_deploy(archive_path):
    """
    method for deploy web static into servers
    """
    if os.path.isfile(archive_path) is False:
        print("failed file doesn't exist")
        return False

    # Get the name of the archive
    new_path = archive_path.split('/')[-1]
    # Get the name of the archive without extension
    folder = new_path.split('.')[0]

    # upload the archive
    if put(archive_path, "/tmp/{}".
            format(new_path)).failed is True:
        return False
    # Creating the right path
    if run("rm -rf /data/web_static/releases/{}/".
            format(folder)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
            format(folder)).failed is True:
        return False
    # uncompress
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
            format(new_path, folder)).failed is True:
        return False
    # remove the archive
    if run("rm  /tmp/{}".format(new_path)).failed is True:
        return False
    # move the content of web_static from uncompress folder
    if run("mv /data/web_static/releases/{}/web_static/*\
            /data/web_static/releases/{}".
            format(folder, folder)).failed is True:
        return False

    # delete the symbolic link
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    # Remove content of web_static from uncompress folder
    if run("rm -rf /data/web_static/releases/{}/web_static".
            format(folder)).failed is True:
        return False
    # create a new symoblic link
    if run("ln -sf /data/web_static/releases/{} /data/web_static/current".
            format(folder)).failed is True:
        return False

    print("New version deployed!")
    return True
