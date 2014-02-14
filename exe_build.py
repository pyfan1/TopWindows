# exe_build.py - Build a py2exe frozen distribution for TopWindows
"""
Copyright (c) 2014 David Webster
See license.txt
"""

from __future__ import with_statement

import os
from zipfile import ZipFile, ZIP_STORED, ZIP_DEFLATED
from plumbum import local

app_name = "TopWindows"

class exebuildException(Exception):     pass
class NameExistsNotDir(exebuildException):     pass
class DeleteEverythingError(exebuildException):     pass

def delete_below_folder(target_folder):
    """Delete everything under a folder but not the folder itself.

       If the folder doesn't exist it is created.
    """
    tgt_dir = local.path(target_folder)
    # Simple-minded sanity check
    if len(tgt_dir.split()) < 4:
        raise DeleteEverythingError, "Looks like you're trying to delete everything on the disk!"
    if tgt_dir.exists():
        if tgt_dir.isdir():
            with local.cwd(tgt_dir):
                goners = tgt_dir // "*"
                goners.extend(tgt_dir // ".*")
                for e in goners:
                    e.delete()
        else:
            raise NameExistsNotDir, "\"%s\" exists but is not a folder." % target_folder
    else:
        tgt_dir.mkdir()

# Clean out build directories
delete_below_folder("build")
delete_below_folder("dist")

# Add license to our distro
local.path("license.txt").copy("dist")

# Run py2exe
local.python("setup.py", "py2exe")

# Put everything in dist into a zip file
dist_dir = local.path('dist')
z = ZipFile(app_name + '.zip', 'w', compression=ZIP_DEFLATED)
for f in dist_dir.list():
    z.write(os.path.join('dist', f.basename),
            os.path.join(app_name, f.basename))
z.close()

# Clean out build directories again
delete_below_folder("build")
delete_below_folder("dist")
