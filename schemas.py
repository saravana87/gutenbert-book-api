# app/schemas.py
from pydantic import BaseModel
from typing import List, Optional

class AuthorSchema(BaseModel):
    name: str
    birth_year: Optional[int] = None
    death_year: Optional[int] = None

    class Config:
        orm_mode = True

class LanguageSchema(BaseModel):
    code: str

    class Config:
        orm_mode = True

class SubjectSchema(BaseModel):
    name: str

    class Config:
        orm_mode = True

class BookshelfSchema(BaseModel):
    name: str

    class Config:
        orm_mode = True

class FormatSchema(BaseModel):
    mime_type: str
    url: str

    class Config:
        orm_mode = True

class FormatResponse(BaseModel):
    mime_type: str
    url: str
    
    class Config:
        orm_mode = True

class BookResponse(BaseModel):
    id: int
    title: Optional[str] = None  # Allows NULL/None values
    download_count: int | None = None  # Python 3.10+ syntax
    authors: List[AuthorSchema]
    languages: List[LanguageSchema]
    subjects: List[SubjectSchema]
    bookshelves: List[BookshelfSchema]    
    download_links: Optional[List[FormatSchema]] = None

    class Config:
        orm_mode = True