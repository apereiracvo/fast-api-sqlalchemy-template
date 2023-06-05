from fastapi_camelcase import CamelModel


class Base(CamelModel):
    class Config:
        orm_mode = True
