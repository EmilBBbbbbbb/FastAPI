from pydantic import BaseModel, Field, EmailStr, ConfigDict
from fastapi import FastAPI

app = FastAPI()

data = {
    'email': 'EMAIL@mail.ru',
    'bio': None,
    'age': 12
}
class UserSchema(BaseModel):
    email: EmailStr
    bio: str | None = Field(max_length=1000)
    age: int = Field(ge=0, le=130)

    model_config = ConfigDict(extra='forbid')

users = []

@app.post('/users')
def add_user(user: UserSchema):
    users.append(user)
    return {'success': True}


@app.get('/users')
def get_users() -> list[UserSchema]:
    return users