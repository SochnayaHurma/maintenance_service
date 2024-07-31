from typing import List
from collections import Counter
import datetime

import pytest
from httpx import AsyncClient
from fastapi import FastAPI, status

from app.models.cleaning import CleaningInDB


class TestFeedRoutes:
    @pytest.mark.asyncio
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient) -> None:
        response = await client.get(app.url_path_for("feed:get-cleaning-feed-for-user"))
        assert response.status_code != status.HTTP_404_NOT_FOUND


class TestCleaningFeed:
    FEED_CLEANING_NAME = "feed:get-cleaning-feed-for-user"
    @pytest.mark.asyncio
    async def test_cleaning_feed_returns_valid_response(
            self,
            app: FastAPI,
            authorized_client: AsyncClient,
            test_list_of_new_and_updated_cleanings: List[CleaningInDB]
    ) -> None:
        cleanings_ids = [cleaning.id for cleaning in test_list_of_new_and_updated_cleanings]

        response = await authorized_client.get(
            app.url_path_for(self.FEED_CLEANING_NAME)
        )
        assert response.status_code == status.HTTP_200_OK
        cleaning_feed = response.json()
        assert isinstance(cleaning_feed, list)
        assert len(cleaning_feed) == 20
        assert set(feed_item["id"] for feed_item in cleaning_feed).issubset(set(cleanings_ids))

    @pytest.mark.asyncio
    async def test_cleaning_feed_response_is_ordered_correctly(
            self, app: FastAPI,
            authorized_client: AsyncClient,
            test_list_of_new_and_updated_cleanings: List[CleaningInDB],
    ) -> None:
        response = await authorized_client.get(app.url_path_for(self.FEED_CLEANING_NAME))
        assert response.status_code == status.HTTP_200_OK
        cleaning_feed = response.json()
        for feed_item in cleaning_feed[:13]:
            assert feed_item["event_type"] == "is_update"
        for feed_item in cleaning_feed[13:]:
            assert feed_item["event_type"] == "is_create"

    @pytest.mark.asyncio
    async def test_cleaning_feed_can_paginate_correctly(
            self, app: FastAPI,
            authorized_client: AsyncClient,
            test_list_of_new_and_updated_cleanings: List[CleaningInDB]
    ) -> None:
        response_page_1 = await authorized_client.get(
            app.url_path_for(self.FEED_CLEANING_NAME)
        )
        feed_page_1 = response_page_1.json()
        assert len(feed_page_1) == 20
        ids_page_1 = {feed_item["id"] for feed_item in feed_page_1}
        new_start_date = feed_page_1[-1]["event_timestamp"]

        response_page_2 = await authorized_client.get(
            app.url_path_for(self.FEED_CLEANING_NAME),
            params={"page_chunk_size": 20, "starting_date": new_start_date}

        )
        assert response_page_2.status_code == status.HTTP_200_OK
        feed_page_2 = response_page_2.json()
        assert len(feed_page_2) == 20
        ids_page_2 = {feed_item["id"] for feed_item in feed_page_2}
        assert ids_page_2 != ids_page_1

    @pytest.mark.asyncio
    async def test_cleaning_feed_can_paginate_correctly(
            self, app: FastAPI,
            authorized_client: AsyncClient,
            test_list_of_new_and_updated_cleanings: List[CleaningInDB]
    ) -> None:
        starting_date = datetime.datetime.now() + datetime.timedelta(minutes=10)
        combos = []
        for chunk_size in (25, 15, 10):
            response = await authorized_client.get(
                app.url_path_for(self.FEED_CLEANING_NAME),
                params={"starting_date": starting_date, "page_chunk_size": chunk_size}
            )
            assert response.status_code == status.HTTP_200_OK
            feed_to_dict = response.json()
            assert len(feed_to_dict) == chunk_size
            id_and_event_combo = {f"{item['id']}-{item['event_type']}" for item in feed_to_dict}
            combos.append(id_and_event_combo)
            starting_date = feed_to_dict[-1]["event_timestamp"]
        length_of_all_id_combos = sum(len(combo) for combo in combos)
        assert len(set().union(*combos)) == length_of_all_id_combos

    @pytest.mark.asyncio
    async def test_cleaning_feed_has_created_and_updated_items_for_modified_cleaning_jobs(
            self, app: FastAPI,
            authorized_client: AsyncClient,
            test_list_of_new_and_updated_cleanings: List[CleaningInDB]
    ) -> None:
        response_page_1 = await authorized_client.get(
            app.url_path_for(self.FEED_CLEANING_NAME),
            params={"page_chunk_size": 30}
        )
        assert response_page_1.status_code == status.HTTP_200_OK
        page_1_to_dict = response_page_1.json()
        ids_page_1 = [item["id"] for item in page_1_to_dict]
        starting_date = page_1_to_dict[-1]["updated_at"]
        response_page_2 = await authorized_client.get(
            app.url_path_for(self.FEED_CLEANING_NAME),
            params={"page_chunk_size": 33, "starting_date": starting_date}
        )
        assert response_page_2.status_code == status.HTTP_200_OK
        page_2_to_dict = response_page_2.json()
        ids_page_2 = [item["id"] for item in page_2_to_dict]

        id_counts = Counter(ids_page_1 + ids_page_2)
        assert len([id for id, cnt in id_counts.items() if cnt > 1]) == 13
