import os

import luigi
from luigi import ExternalTask, Parameter, Task, LocalTarget

from luigi.format import FileWrapper
from csci_utils.luigi.target import SuffixPreservingLocalTarget
from neural_style.neural_style import stylize
from pset_4.tasks.data import DownloadImage, DownloadModel


class Stylize(Task):
    """
    Luigi Taks that stylize images according to a model
    """

    model = Parameter(default=r"rain_princess.pth")
    image = Parameter(default=r"luigi.jpg")

    def requires(self):
        return {
            'image': self.clone(DownloadImage),
            'model': self.clone(DownloadModel)
        }

    def output(self):
        # return SuffixPreservingLocalTarget of the stylized image
        return SuffixPreservingLocalTarget(os.path.join('images_out', "luigiout.jpg"), format=luigi.format.Nop)

    def run(self):
        inputs = self.input()
        with self.output().temporary_path() as temp_output_path:
            class args:
                content_image = inputs['image'].path
                output_image = temp_output_path
                model = inputs['model'].path
                cuda = 0
                content_scale = None
                export_onnx = None

            stylize(args)
