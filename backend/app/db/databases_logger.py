import typing
import logging

from databases import Database
from databases.interfaces import Record
from sqlalchemy.sql import ClauseElement


logger = logging.getLogger(__name__)


class DatabaseByLogger(Database):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.count = 0

    async def execute(
        self,
        query: typing.Union[ClauseElement, str],
        values: typing.Optional[dict] = None,
    ) -> typing.Any:
        self.count += 1
        logger.warning(f"{self.count}: {query}")
        return await super().execute(query=query, values=values)

    async def fetch_one(
        self,
        query: typing.Union[ClauseElement, str],
        values: typing.Optional[dict] = None,
    ) -> typing.Optional[Record]:
        self.count += 1
        logger.warning(f"{self.count}: {query}")
        return await super().fetch_one(query=query, values=values)

    async def fetch_all(
        self,
        query: typing.Union[ClauseElement, str],
        values: typing.Optional[dict] = None,
    ) -> typing.List[Record]:
        self.count += 1
        logger.warning(f"{self.count}: {query}")
        return await super().fetch_all(query=query, values=values)
