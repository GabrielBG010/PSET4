# import hashlib
import argparse

import luigi

from pset_4.hash_str import get_csci_salt, hash_str
from pset_4.tasks.stylize import Stylize


def get_user_hash(username, salt=None):
    salt = salt or get_csci_salt()
    return hash_str(username, salt=salt)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("-i", "--image", default='luigi.jpg' , action="store_true")
    parser.add_argument("-m", "--model", default='rain_princess.pth')
    args = parser.parse_args()

    luigi.build([
        # ContentImage(image='luigi.jpg'),
        # SavedModel(model='rain_princess.pth'),
        # DownloadImage(image='luigi.jpg'),
        # DownloadModel(model='rain_princess.pth'),
        Stylize(image=args.image,model=args.model)
    ], local_scheduler=True)
