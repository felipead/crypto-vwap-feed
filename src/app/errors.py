from typing import Dict, List, Optional


class ApplicationError(Exception):
    pass


class SchemaValidationError(ApplicationError):
    def __init__(self, message: str, failures: Optional[Dict[str, List[str]]] = None):
        super().__init__(f'{message} => {failures}' if failures else message)
