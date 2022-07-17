from pydantic import BaseModel


class Namespace(BaseModel):
    id: int
    name: str
