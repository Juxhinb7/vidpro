from typing import Union

from pydantic import BaseModel


class Result(BaseModel):
    """
    Return type for methods or functions with try, except operations.
    """
    output: Union[str, dict] # The output can be either str or dict
    has_error: bool