import os
import cv2
import sys
import numpy as np  # Need numpy for mixing

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.GrayExample.src.utils.response import build_response_mixer
from components.GrayExample.src.models.PackageModel import PackageModel
import copy

class MixerExample(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))

        self.image_main_id = self.request.get_param("inputImage")
        self.image_overlay_id = self.request.get_param("inputImageTwo")

        self.mix_config = self.request.get_param("MixMode")


        self.alpha = 0.5


        if "Alpha" in self.mix_config:
            self.alpha = float(self.mix_config["Alpha"])
        elif "Strength" in self.mix_config:
            strength = self.mix_config["Strength"]
            self.alpha = 0.8 if strength == "High" else 0.2

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def run(self):
        # 1. Get Both Images
        img1 = Image.get_frame(img=self.image_main_id, redis_db=self.redis_db)
        img2 = Image.get_frame(img=self.image_overlay_id, redis_db=self.redis_db)

        h, w = img1.value.shape[:2]
        img2_resized = cv2.resize(img2.value, (w, h))
        mixed_array = cv2.addWeighted(img1.value, 1 - self.alpha, img2_resized, self.alpha, 0)
        diff_array = cv2.absdiff(img1.value, img2_resized)

        wrapper_mix = copy.deepcopy(img1)  # Create a clone of the wrapper
        wrapper_mix.value = mixed_array  # Stuff the new data inside

        wrapper_diff = copy.deepcopy(img1)  # Create another clone
        wrapper_diff.value = diff_array

        self.image_mix = Image.set_frame(img=wrapper_mix, package_uID=self.uID, redis_db=self.redis_db)
        self.image_diff = Image.set_frame(img=wrapper_diff, package_uID=self.uID, redis_db=self.redis_db)


        return build_response_mixer(context=self)


if "__main__" == __name__:
    Executor(sys.argv[1]).run()