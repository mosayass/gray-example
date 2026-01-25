
from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Image, Inputs, Configs, Outputs, Response, Request, Output, Input, Config


class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"

class InputImageTwo(Input):
    # Notice the unique name. This is crucial!
    name: Literal["inputImageTwo"] = "inputImageTwo"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Second Image"

class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image],Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"


class KeepSideFalse(Config):
    name: Literal["False"] = "False"
    value: Literal[False] = False
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Disable"


class KeepSideTrue(Config):
    name: Literal["True"] = "True"
    value: Literal[True] = True
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Enable"


class KeepSideBBox(Config):
    """
        Rotate image without catting off sides.
    """
    name: Literal["KeepSide"] = "KeepSide"
    value: Union[KeepSideTrue, KeepSideFalse]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Keep Sides"


class Degree(Config):
    """
        Positive angles specify counterclockwise rotation while negative angles indicate clockwise rotation.
    """
    name: Literal["Degree"] = "Degree"
    value: int = Field(ge=-359.0, le=359.0,default=0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["[-359, 359]"] = "[-359, 359]"

    class Config:
        title = "Angle"



class ConfigKernelSize(Config):
    name: Literal["KernelSize"] = "KernelSize"
    value: int = Field(default=5, ge=1, le=21)  # Slider or Input for Blur strength
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Blur Strength (Odd Number)"


class BlurExampleConfigs(Configs):
    kernelSize: ConfigKernelSize


class BlurExampleInputs(Inputs):
    inputImage: InputImage


class BlurExampleOutputs(Outputs):
    outputImage: OutputImage


class BlurExampleRequest(Request):
    inputs: Optional[BlurExampleInputs]
    configs: BlurExampleConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }


class BlurExampleResponse(Response):
    outputs: BlurExampleOutputs

class BlurExampleExecutor(Config):
    name: Literal["BlurExample"] = "BlurExample"
    value: Union[BlurExampleRequest, BlurExampleResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Blur Filter"
        json_schema_extra = {"target": {"value": 0}}

class GrayExampleInputs(Inputs):
    inputImage: InputImage


class GrayExampleConfigs(Configs):
    degree: Degree
    drawBBox: KeepSideBBox


class GrayExampleOutputs(Outputs):
    outputImage: OutputImage


class GrayExampleRequest(Request):
    inputs: Optional[GrayExampleInputs]
    configs: GrayExampleConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }


class GrayExampleResponse(Response):
    outputs: GrayExampleOutputs




class GrayExampleExecutor(Config):
    name: Literal["GrayExample"] = "GrayExample"
    value: Union[GrayExampleRequest, GrayExampleResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "GrayExample"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }

class OutputImageMix(Output):
    name: Literal["outputImageMix"] = "outputImageMix"
    value: Union[List[Image], Image]
    type: str = "object"
    class Config: title = "Mixed Result"

class OutputImageDiff(Output):
    name: Literal["outputImageDiff"] = "outputImageDiff"
    value: Union[List[Image], Image]
    type: str = "object"
    class Config: title = "Difference Result"

class ConfigAlpha(Config):
    name: Literal["Alpha"] = "Alpha"
    value: float = Field(default=0.5, ge=0.0, le=1.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput" # Type 1: Text Input
    class Config: title = "Alpha Value (0.0 - 1.0)"

class ConfigModeManual(Config):
    name: Literal["Manual"] = "Manual"
    value: ConfigAlpha # Links to the Number Field
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config: title = "Manual Alpha"

class ConfigStrength(Config):
    name: Literal["Strength"] = "Strength"
    value: Literal["Low", "High"] = "Low"
    type: Literal["string"] = "string"
    field: Literal["dropdownlist"] = "dropdownlist"
    class Config: title = "Strength Level"

class ConfigModePreset(Config):
    name: Literal["Preset"] = "Preset"
    value: ConfigStrength
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config: title = "Use Preset"

class ConfigMixMode(Config):
    name: Literal["MixMode"] = "MixMode"
    value: Union[ConfigModeManual, ConfigModePreset]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    restart: Literal[True] = True
    class Config: title = "Mixing Mode"

class MixerConfigs(Configs):
    mixMode: ConfigMixMode

class MixerInputs(Inputs):
    inputMain: InputImageMain
    inputOverlay: InputImageOverlay

class MixerOutputs(Outputs):
    outputMix: OutputImageMix
    outputDiff: OutputImageDiff

class MixerRequest(Request):
    inputs: MixerInputs
    configs: MixerConfigs

    class Config: json_schema_extra = {"target": "configs"}


class MixerResponse(Response):
    outputs: MixerOutputs


class MixerExecutor(Config):
    name: Literal["MixerExample"] = "MixerExample"
    value: Union[MixerRequest, MixerResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Image Mixer (2 In / 2 Out)"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[BlurExampleExecutor,GrayExampleExecutor,MixerExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    restart: Literal[True] = True

    class Config:
        title = "Taskkk"
        # json_schema_extra = {
        #     "target": "value"
        # }


class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["GrayExample"] = "GrayExample"
