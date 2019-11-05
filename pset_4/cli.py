"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mcsci_utils` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``csci_utils.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``csci_utils.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import argparse

import luigi

from pset_4.tasks.stylize import Stylize

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument("-i", "--image", default='luigi.jpg' , action="store_true")
parser.add_argument("-m", "--model", default='rain_princess.pth')
args = parser.parse_args()

def main(args=None):
    luigi.build([
        # ContentImage(image='luigi.jpg'),
        # SavedModel(model='rain_princess.pth'),
        # DownloadImage(image='luigi.jpg'),
        # DownloadModel(model='rain_princess.pth'),
        Stylize(image=args.image,model=args.model)
    ], local_scheduler=True)
