from pydantic import BaseModel, validator
from typing import List


class SensorData(BaseModel):
    data: List[float]
    #data2: float
    
    @validator("data",always=True)
    def ext(cls, v):
        data_len = 4
        if not len(v) == data_len:
            raise ValueError(f"Send exactly {data_len} values")
        return v


    #@validator("data2")
    #def temp_must_be_positive(cls, value):
    #    if value <= 0:
    #        raise ValueError(f"we expect temp >= 0, we received {value}")
    #    return value