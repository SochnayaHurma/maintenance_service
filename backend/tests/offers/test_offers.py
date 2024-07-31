import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient

from app.models.cleaning import CleaningInDB
from app.models.users import UserInDB

pytest_mark = pytest.mark.asyncio


class TestOffersRoutes:
    """
    Набор тестов проверяющих работоспособность маршрутов роутера offers
    """
    WRONG_STATUS = "Маршрут %s не был найден"

    @pytest.mark.asyncio
    async def test_routes_exist(self, app: FastAPI,
                                client: AsyncClient, test_user2: UserInDB,
                                test_cleaning_with_offers: CleaningInDB
                                ) -> None:
        name_route_get_one = "offers:get-offer-from-user"
        response_get_one = await client.get(
            app.url_path_for(name_route_get_one, cleaning_id=test_cleaning_with_offers.id, username=test_user2.username)
        )
        assert response_get_one.status_code != status.HTTP_404_NOT_FOUND, self.WRONG_STATUS.format(name_route_get_one)

        name_route_get_list = "offers:list-offers-for-cleaning"
        response_get_list = await client.get(
            app.url_path_for(name_route_get_list, cleaning_id=1)
        )
        assert response_get_list.status_code != status.HTTP_404_NOT_FOUND, self.WRONG_STATUS.format(name_route_get_list)

        name_route_post = "offers:create-offer"
        response_post = await client.post(app.url_path_for(name_route_post, cleaning_id=1))
        assert response_post.status_code != status.HTTP_404_NOT_FOUND, self.WRONG_STATUS.format(name_route_post)

        name_route_put_accept = "offers:accept-offer-from-user"
        response_put_accept = await client.put(app.url_path_for(name_route_put_accept, cleaning_id=test_cleaning_with_offers.id, username=test_user2.username))
        assert response_put_accept.status_code != status.HTTP_404_NOT_FOUND, self.WRONG_STATUS.format(name_route_put_accept)

        name_route_put_cancel = "offers:cancel-offer-from-user"
        response_put_cancel = await client.put(app.url_path_for(name_route_put_cancel, cleaning_id=1))
        assert response_put_cancel.status_code != status.HTTP_404_NOT_FOUND, self.WRONG_STATUS.format(name_route_put_cancel)

        name_route_delete = "offers:rescind-offer-from-user"
        response_delete = await client.delete(app.url_path_for(name_route_delete, cleaning_id=1))
        assert response_delete.status_code != status.HTTP_404_NOT_FOUND, self.WRONG_STATUS.format(name_route_delete)
