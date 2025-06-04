# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_
from app import models, schemas
from app.database import SessionLocal, engine
from typing import List, Optional
from datetime import datetime, timezone


app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/books/", response_model=List[schemas.BookResponse])
def get_books(db: Session = Depends(get_db)):
    try:
        books = (
            db.query(models.Book)
            .options(
                joinedload(models.Book.authors),
                joinedload(models.Book.languages),
                joinedload(models.Book.subjects),
                joinedload(models.Book.bookshelves),
                joinedload(models.Book.formats)
            )
            .order_by(models.Book.download_count.desc())
            .limit(25)
            .all()
        )

        if not books:
            raise HTTPException(status_code=404, detail="No books found.")

        return books
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving books: {str(e)}")


@app.get("/books_advanced/", response_model=List[schemas.BookResponse])
def get_books_advanced(
    language: Optional[str] = None,
    mime_type: Optional[str] = None,
    topic: Optional[str] = None,
    author: Optional[str] = None,
    title: Optional[str] = None,
    page: int = 1,
    db: Session = Depends(get_db)
):
    try:
        query = db.query(models.Book).options(
            joinedload(models.Book.authors),
            joinedload(models.Book.languages),
            joinedload(models.Book.subjects),
            joinedload(models.Book.bookshelves),
            joinedload(models.Book.formats)
        )

        if language:
            lang_codes = [lang.strip().lower() for lang in language.split(",")]
            query = query.join(models.Book.languages).filter(
                models.Language.code.in_(lang_codes)
            )

        if mime_type:
            mime_types = [mime.strip() for mime in mime_type.split(",")]
            query = query.join(models.Book.formats).filter(
                models.Format.mime_type.in_(mime_types)
            )

        if topic:
            topics = [t.strip() for t in topic.split(",")]
            query = query.join(models.Book.subjects).join(models.Book.bookshelves).filter(
                or_(
                    *[models.Subject.name.ilike(f"%{t}%") for t in topics],
                    *[models.Bookshelf.name.ilike(f"%{t}%") for t in topics]
                )
            )

        if author:
            authors = [a.strip() for a in author.split(",")]
            query = query.join(models.Book.authors).filter(
                or_(*[models.Author.name.ilike(f"%{a}%") for a in authors])
            )

        if title:
            query = query.filter(models.Book.title.ilike(f"%{title}%"))

        books = query.order_by(
            models.Book.download_count.desc()
        ).offset(
            (page - 1) * 25
        ).limit(
            25
        ).all()

        if not books:
            raise HTTPException(status_code=404, detail="No matching books found.")

        return books
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving books: {str(e)}")
    
@app.get("/healthcheck")
def healthcheck():
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
@app.get("/healthcheck_new")
def healthcheck_new():
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat()
    }