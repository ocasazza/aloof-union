# aloof_union/exceptions.py
class AloofUnionError(Exception):
    """Base exception for aloof-union library."""

    pass


class ParserError(AloofUnionError):
    """Raised when parsing workflow content fails."""

    pass


class ValidationError(AloofUnionError):
    """Raised when workflow validation fails."""

    pass


class TranspilerError(AloofUnionError):
    """Raised when workflow transpilation fails."""

    pass
