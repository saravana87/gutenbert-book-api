# app/models.py
from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

# ---- Junction Tables (define FIRST) ----
class BookAuthor(Base):
    __tablename__ = "books_book_authors"
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books_book.id"))
    author_id = Column(Integer, ForeignKey("books_author.id"))

class BookSubject(Base):  # Add this missing model
    __tablename__ = "books_book_subjects"
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books_book.id"))
    subject_id = Column(Integer, ForeignKey("books_subject.id"))

class BookBookshelf(Base):  # Add this missing model
    __tablename__ = "books_book_bookshelves"
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books_book.id"))
    bookshelf_id = Column(Integer, ForeignKey("books_bookshelf.id"))

class BookLanguage(Base):
    __tablename__ = "books_book_languages"
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books_book.id"))
    language_id = Column(Integer, ForeignKey("books_language.id"))

# ---- Core Tables (define AFTER junctions) ----
class Book(Base):
    __tablename__ = "books_book"
    id = Column(Integer, primary_key=True)
    title = Column(String(1024))
    download_count = Column(Integer)
    gutenberg_id = Column(Integer, unique=True)
    media_type = Column(String(16))
    
    # Relationships (now safe to use)
# Update relationships to use viewonly=False
    authors = relationship("Author", secondary="books_book_authors", back_populates="books", viewonly=False)
    languages = relationship("Language", secondary="books_book_languages", back_populates="books", viewonly=False)
    subjects = relationship("Subject", secondary="books_book_subjects", back_populates="books", viewonly=False)
    bookshelves = relationship("Bookshelf", secondary="books_book_bookshelves", back_populates="books", viewonly=False)
    formats = relationship("Format", back_populates="book", viewonly=False, lazy="select")

# ---- Other tables (Author, Subject, etc.) ----
class Author(Base):
    __tablename__ = "books_author"
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    birth_year = Column(SmallInteger, nullable=True)
    death_year = Column(SmallInteger, nullable=True)
    books = relationship("Book", secondary="books_book_authors", back_populates="authors")

class Subject(Base):
    __tablename__ = "books_subject"
    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    books = relationship("Book", secondary="books_book_subjects", back_populates="subjects")

class Bookshelf(Base):
    __tablename__ = "books_bookshelf"
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    books = relationship("Book", secondary="books_book_bookshelves", back_populates="bookshelves")

class Language(Base):
    __tablename__ = "books_language"
    id = Column(Integer, primary_key=True)
    code = Column(String(4), unique=True)
    books = relationship("Book", secondary="books_book_languages", back_populates="languages")

class Format(Base):
    __tablename__ = "books_format"
    id = Column(Integer, primary_key=True)
    mime_type = Column(String(32))
    url = Column(String(256))
    book_id = Column(Integer, ForeignKey("books_book.id"))
    book = relationship("Book", back_populates="formats")