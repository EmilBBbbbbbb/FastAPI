import uvicorn
from fastapi import FastAPI, HTTPException, Response, Depends
from authx import AuthX, AuthXConfig
from pydantic import BaseModel

app = FastAPI()

config = AuthXConfig()
config.JWT_SECRET_KEY = 'SECRET'
config.JWT_ACCESS_COOKIE_NAME = 'MY_ACCESS_TOKEN'
config.JWT_TOKEN_LOCATION = ['cookies']

security = AuthX(config=config)


class UserLoginSchema(BaseModel):
    username: str
    password: str


@app.post('/login')
def login(creds: UserLoginSchema, response: Response):
    if creds.username == 'admin' and creds.password == 'admin':
        token = security.create_access_token(uid="12345")
        response.set_cookie(key=config.JWT_ACCESS_COOKIE_NAME, value=token)
        return {'access_token': token}
    raise HTTPException(status_code=401, detail='Incorrect username or password')

@app.get('/protected', dependencies=[Depends(security.access_token_required)])
def protected():
    return {'data': 'TOP SECRET'}


if __name__ == '__main__':
    uvicorn.run('lesson_4:app', reload=True)