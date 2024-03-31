import orjson
from pydantic import BaseModel


class OrjsonMixin(BaseModel):
    """Configure Base model"""

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson.dumps
