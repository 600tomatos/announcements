from datetime import datetime
from abc import ABC, abstractmethod


class ValidationError(Exception):
    def __init__(self, message):
        super().__init__(message)


class Validator(ABC):
    """Base class for validators"""

    @classmethod
    def check(cls, value):
        """Helper method that takes out the logic of creating a validator outside view.
           It is understood that validation begins with the perform_validate method.
        """

        return cls().perform_validate(value)

    @abstractmethod
    def perform_validate(self, *args, **kwargs):
        """Any additional logic that can break validation into smaller logical parts"""

        pass

    def remember_validation_data(self, data):
        self.validation_data = data

    def validate(self, *args, **kwargs):
        """The main validation method that takes only keyword arguments and calls the validator functions,
             which should be called in the format validate_ <key>
        """

        available_validators = [func for func in dir(self) if func.startswith('validate')]
        if args:
            raise ValidationError('Only keyword arguments allowed')
        for key, value in kwargs.items():
            current_validator_name = f'validate_{key}'
            if not current_validator_name in available_validators:
                raise ValidationError(f'Unable to find validator for key: {key}.'
                                      f'Define a function for validation in the format: validate_<key>')
            validator = getattr(self, current_validator_name)
            error = validator(value)
            if error:
                return error

    def error_message(self, info):
        return f'validation error: {info}'
