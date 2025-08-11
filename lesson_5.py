import time
import asyncio

from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

def sync_task():
    time.sleep(3)
    print('sync task')

async def async_task():
    await asyncio.sleep(3)
    print('async task')


@app.get('/')
async def root(bg_task: BackgroundTasks):
    asyncio.create_task(async_task())

    bg_task.add_task(sync_task)
    return {'message': 'ok'}