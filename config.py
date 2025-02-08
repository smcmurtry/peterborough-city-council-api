import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@db:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
