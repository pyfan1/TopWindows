"""
Copyright (c) 2013 David Webster
See license.txt
"""

from distutils.core import setup
import py2exe

setup(windows=['TopWindows.py'],

      options={ "py2exe":{ "excludes": ["Tkconstants","Tkinter","tcl"]
                         }
              }
     )
