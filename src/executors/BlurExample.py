import os
import cv2
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.GrayExample.src.utils.response import build_response_blur
from components.GrayExample.src.models.PackageModel import PackageModel


class BlurExample(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        self.kernel_size = self.request.get_param("KernelSize")
        self.image = self.request.get_param("inputImage")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def blur(self, image):
        # Kernel size must be odd (3, 5, 7...), we ensure it's odd or default to 5
        k = int(self.kernel_size) if self.kernel_size else 5
        if k % 2 == 0: k += 1
        return cv2.GaussianBlur(image, (k, k), 0)

    def run(self):
        img = Image.get_frame(img=self.image, redis_db=self.redis_db)

        img.value = self.blur(img.value)

        self.image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)

        packageModel = build_response_blur(context=self)
        return packageModel


if "__main__" == __name__:
    Executor(sys.argv[1]).run()