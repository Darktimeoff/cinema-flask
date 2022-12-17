from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .setup.db.models import Base


class Genre(Base):
    __tablename__ = 'genres'

    name = Column(String(30), unique=True, nullable=False)

    movies = relationship('Movie', back_populates='genre')

    def __repr__(self) -> str:
        return f'<Director id={self.pk} title={self.name} />'


class Director(Base):
    __tablename__ = 'directors'

    name = Column(String(100))

    movies = relationship('Movie', back_populates='directors')

    def __repr__(self) -> str:
        return f'<Director id={self.pk} title={self.name} />'


class Movie(Base):
    __tablename__ = 'movies'

    title = Column(String(100))
    description = Column(String(250))
    trailer = Column(String(300))
    year = Column(Integer)
    rating = Column(Integer)

    genre_id = Column(Integer, ForeignKey('genres.id'))
    director_id = Column(Integer, ForeignKey('directors.id'))

    genre = relationship(Genre, back_populates='movies')
    directors = relationship(Director, back_populates='movies')

    def __repr__(self) -> str:
        return f'<Movie id={self.pk} title={self.title} />'


class User(Base):
    __tablename__ = 'users'

    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(300), nullable=False)
    refresh_token = Column(String(300))
    name = Column(String(100))
    surname = Column(String(100))

    favorite_genre_id = Column(Integer, ForeignKey('genres.id'))

    favorite_genre = relationship(Genre)
