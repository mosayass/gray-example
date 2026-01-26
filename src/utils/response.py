
from sdks.novavision.src.helper.package import PackageHelper
from components.GrayExample.src.models.PackageModel import PackageModel, PackageConfigs, ConfigExecutor, GrayExampleOutputs, GrayExampleResponse, GrayExampleExecutor, OutputImage
from components.GrayExample.src.models.PackageModel import BlurExampleOutputs, BlurExampleResponse, BlurExampleExecutor
from components.GrayExample.src.models.PackageModel import MixerOutputs, MixerResponse, MixerExecutor, OutputImageMix, OutputImageDiff

def build_response(context):
    outputImage = OutputImage(value=context.image)
    Outputs = GrayExampleOutputs(outputImage=outputImage)
    grayExampleResponse = GrayExampleResponse(outputs=Outputs)
    grayExampleExecutor = GrayExampleExecutor(value=grayExampleResponse)
    executor = ConfigExecutor(value=grayExampleExecutor)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    # test
    return packageModel


def build_response_blur(context):
    outputImage = OutputImage(value=context.image)
    Outputs = BlurExampleOutputs(outputImage=outputImage)
    blurResponse = BlurExampleResponse(outputs=Outputs)
    blurExecutor = BlurExampleExecutor(value=blurResponse)
    executor = ConfigExecutor(value=blurExecutor)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel


def build_response_mixer(context):
    # Wrap Output 1
    out1 = OutputImageMix(value=context.image_mix)
    # Wrap Output 2
    out2 = OutputImageDiff(value=context.image_diff)

    # Add both to Outputs
    outputs = MixerOutputs(outputImageMix=out1, outputImageDiff=out2)

    mixerResponse = MixerResponse(outputs=outputs)
    mixerExecutor = MixerExecutor(value=mixerResponse)
    executor = ConfigExecutor(value=mixerExecutor)
    packageConfigs = PackageConfigs(executor=executor)

    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    return package.build_model(context)