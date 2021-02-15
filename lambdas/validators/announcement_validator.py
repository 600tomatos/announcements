from lambdas.helpers.validator import Validator


class AnnouncementValidator(Validator):
    MAX_TITLE_LEN = 100

    def perform_validate(self, validate_kwargs):
        return self.validate(**validate_kwargs)

    def validate_title(self, value):

        if not value:
            return self.error_message('Title is required')

        if not isinstance(value, str):
            return self.error_message('Title can only be a string')

        if len(value) > self.MAX_TITLE_LEN:
            return self.error_message(f'maximum title length {self.MAX_TITLE_LEN} characters')

    def validate_description(self, value):

        if not value:
            return self.error_message('Description is required')

        if not isinstance(value, str):
            return self.error_message('Description can only be a string')
