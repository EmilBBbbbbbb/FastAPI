from fastapi import FastAPI, File, UploadFile

from fastapi.responses import StreamingResponse, FileResponse

app = FastAPI()

@app.post('/upload')
async def load_file(upload_file: UploadFile):
    file = upload_file.file
    name = upload_file.filename
    with open(name, 'wb') as f:
        f.write(file.read())


@app.post('/multi_upload')
async def load_file(upload_files: list[UploadFile]):
    for upload_file in upload_files:
        file = upload_file.file
        name = upload_file.filename
        with open(name, 'wb') as f:
            f.write(file.read())

@app.get('/files/{filename}')
async def get_file(filename: str):
    return FileResponse(filename)

def iterfile(filename: str):
    with open(filename, 'rb') as f:
        while chunk := f.read(1024*1024):
            yield chunk


@app.get('/files/streaming/{filename}')
async def get_file(filename: str):
    return StreamingResponse(iterfile(filename), media_type="video/mp4")