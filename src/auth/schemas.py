from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    id: int
    username: str
    role_id: int


class UserCreate(schemas.BaseUserCreate):
    id: int
    username: str
    role_id: int
