import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get('/user')
async def get_user():
    return {'user': 'admin'}

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0')