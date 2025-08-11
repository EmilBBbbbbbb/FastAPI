from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import select
from fastapi import FastAPI, Depends
import uvicorn
from typing import Annotated
from pydantic import BaseModel

app = FastAPI()

engine = create_async_engine('sqlite+aiosqlite:///books.db')

new_session = async_sessionmaker(engine, expire_on_commit=False)



async def get_session():
    async with new_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]

class Base(DeclarativeBase):
    pass


class BookModel(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]

class BookADDSchema(BaseModel):
    title: str
    author: str

class BookSchema(BookADDSchema):
    id: int


@app.post('/setup_database')
async  def create_table():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    return {'success': True}


@app.post('/books')
async def create_book(book: BookSchema, session: SessionDep):
    new_book = BookModel(title=book.title, author=book.author)
    session.add(new_book)
    await session.commit()
    return {'success': True}

@app.get('/books')
async def get_books(session: SessionDep):
    query = select(BookModel)
    result = await session.execute(query)

    return result.scalars().all()

if __name__ == '__main__':
    uvicorn.run('lesson_3:app',reload=True)