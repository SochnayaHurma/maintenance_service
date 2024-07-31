from typing import Callable, Type
from databases import Database

from fastapi import Depends, Request

from app.db.repositories.base import BaseRepository
from app.core.config import DEBUG


def get_database(request: Request) -> Database:
    yield request.app.state._db
    if DEBUG:
        request.app.state._db.count = 0


def get_repository(repo_type: Type[BaseRepository]) -> Callable:
    def get_repo(db: Database = Depends(get_database)) -> Type[BaseRepository]:
        return repo_type(db)
    return get_repo
