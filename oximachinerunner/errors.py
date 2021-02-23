# -*- coding: utf-8 -*-
"""Defining custom exceptions for OximachineRunner"""
__all__ = [
    "OximachineRunnerException",
    "NoMetalError",
    "FeaturizationError",
    "PredictionError",
    "ModelNotFoundError",
    "ParsingError",
]


class OximachineRunnerException(Exception):
    """General class for oximachine errors"""


class NoMetalError(OximachineRunnerException):
    """Error that is thrown if there is no metal in the structure"""


class FeaturizationError(OximachineRunnerException):
    """Error that is thrown if the featurization fails"""


class PredictionError(OximachineRunnerException):
    """Error that is thrown if the prediction fails"""


class ModelNotFoundError(OximachineRunnerException):
    """Error that is thrown if the model could not be found"""


class ParsingError(OximachineRunnerException):
    """Error that is thrown if we cannot convert the structure into a pymatgen Structure object"""
