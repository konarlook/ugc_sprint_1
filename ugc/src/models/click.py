from datetime import datetime
from pydantic import StrictStr, validator

from pydantic import BaseModel


class Click(BaseModel):
    user_id: StrictStr
    event_dt: StrictStr
    current_url: StrictStr
    destination_url: StrictStr

    @validator('event_dt', pre=True, always=True)
    def set_datetime_utcnow(cls, v):
        return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
