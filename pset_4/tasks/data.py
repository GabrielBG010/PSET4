import os

import luigi
from luigi import ExternalTask, Parameter, Task, LocalTarget

from luigi.contrib.s3 import S3Target
from luigi.format import FileWrapper


class ContentImage(ExternalTask):
    """
    Luigi Task that check that the image exists
    """
    # Source of the image
    IMAGE_ROOT = "s3://pset4-gabrielbg010/pset4/images/"
    # Name of the image
    image = Parameter(default="luigi.jpg")  # Filename of the image under the root s3 path

    def output(self):
        # return the S3Target of the image
        return S3Target(os.path.join(self.IMAGE_ROOT, self.image), format=luigi.format.Nop)


class SavedModel(ExternalTask):
    """
    Luigi Task that check that the model exists
    """
    # Source of the image
    MODEL_ROOT = "s3://pset4-gabrielbg010/pset4/saved_models/"
    # Filename of the model
    model = Parameter(default="rain_princess.pth")

    def output(self):
        # return the S3Target of the model
        return S3Target(os.path.join(self.MODEL_ROOT, self.model), format=luigi.format.Nop)


class DownloadModel(Task):
    """
    Luigi Task that download the model
    """
    S3_ROOT = 's3://pset4-gabrielbg010/pset4/'
    LOCAL_ROOT = os.path.abspath('data')
    SHARED_RELATIVE_PATH = 'saved_models'

    model = Parameter(default=r"rain_princess.pth")  # luigi parameter

    def requires(self):
        # Depends on the SavedModel ExternalTask being complete
        # i.e. the file must exist on S3 in order to copy it locally
        return self.clone(SavedModel)

    def output(self):
        return LocalTarget(os.path.join(self.SHARED_RELATIVE_PATH, self.model), format=luigi.format.Nop)

    def run(self):
        #Reading of the input file
        with self.input().open(mode='r') as binary_file:
            bdata = binary_file.read()  # Read the whole file at once

        # Writting of the output file "The model"
        with open(self.output().path, 'wb') as binary_file:
            binary_file.write(bdata)


class DownloadImage(Task):
    """
    Luigi Task that download the image
    """
    S3_ROOT = 's3://pset4-gabrielbg010/pset4/'
    LOCAL_ROOT = os.path.abspath('data')
    SHARED_RELATIVE_PATH = 'images'

    image = Parameter(default="luigi.jpg")  # Luigi parameter

    def requires(self):
        return self.clone(ContentImage)

    def output(self):
        return LocalTarget(os.path.join(self.SHARED_RELATIVE_PATH, self.image), format=luigi.format.Nop)

    def run(self):
        # Reading of the input file
        with self.input().open(mode='r') as binary_file:
            bdata = binary_file.read()  # Read the whole file at once

        # Writting of the output file "The model"
        with open(self.output().path, 'wb') as binary_file:
            binary_file.write(bdata)
