#!/usr/bin/python3
"""
Fabric file
"""
import os
from datetime import datetime
from fabric.api import local


env.hosts = ["18.234.105.201", "100.26.162.114"]
env.user = "ubuntu"


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
        return False

    try:
        # Get the name of the archive
        new_path = archive_path.split('/')[-1]
        # Get the name of the archive without extension
        folder = new_path.split('.')[0]
        
        # upload the archive 
        put(archive_path, "/tmp/")
        # uncompress
        run ("tar -xzf /tmp/{} -C /data/web_static/releases/{}".format(new_path, folder))
        # remove the archive
        run ("rm  /tmp/{}".format(new_path)
        # delete the symbolic link
        run ("rm -rf /data/web_static/current")
        # move the content of web_static from uncompress folder
        run ("mv /data/web/static/releases/{}/web_static/* /data/web/static/releases/{}".format(folder, folder)
        # Remove content of web_static from uncompress folder
        run ("rm -rf /data/web_static/releases/{}/web_static".format(folder))
        # create a new symoblic link
        run ("ln -sf /data/web_static/releases/{}  /data/web_static/current".format(folder))
        return True
    except OSError:
        return False
