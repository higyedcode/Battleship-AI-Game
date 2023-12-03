class WrongDataTypeError(Exception):
    pass


class DuplicateIdError(Exception):
    pass


class IdNotFoundError(Exception):
    pass


class InvalidShipProperty(Exception):
    pass


class InvalidPositionError(Exception):
    def __str__(self):
        return 'Invalid Position Error'


class PositionAlreadyGuessedError(Exception):
    def __str__(self):
        return 'Position is already guessed!'

