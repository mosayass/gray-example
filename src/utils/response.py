
from sdks.novavision.src.helper.package import PackageHelper
from components.GrayExample.src.models.PackageModel import PackageModel, PackageConfigs, ConfigExecutor, GrayExampleOutputs, GrayExampleResponse, GrayExampleExecutor, OutputImage


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