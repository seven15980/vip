# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import StrictInt, StrictStr
from typing import Any
from openapi_server.models.api_admin_card_codes_post_request import ApiAdminCardCodesPostRequest
from openapi_server.models.api_admin_login_post_request import ApiAdminLoginPostRequest
from openapi_server.models.api_admin_memberships_user_id_renew_post_request import ApiAdminMembershipsUserIdRenewPostRequest
from openapi_server.models.api_login_post200_response import ApiLoginPost200Response
from openapi_server.models.api_membership_get200_response import ApiMembershipGet200Response
from openapi_server.models.api_profile_put_request import ApiProfilePutRequest
from openapi_server.models.api_redeem_post_request import ApiRedeemPostRequest
from openapi_server.models.api_register_post_request import ApiRegisterPostRequest
from openapi_server.security_api import get_token_bearerAuth

class BaseDefaultApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseDefaultApi.subclasses = BaseDefaultApi.subclasses + (cls,)
    async def api_admin_card_codes_code_logs_get(
        self,
        code: StrictStr,
    ) -> None:
        ...


    async def api_admin_card_codes_get(
        self,
    ) -> None:
        ...


    async def api_admin_card_codes_post(
        self,
        api_admin_card_codes_post_request: ApiAdminCardCodesPostRequest,
    ) -> None:
        ...


    async def api_admin_login_post(
        self,
        api_admin_login_post_request: ApiAdminLoginPostRequest,
    ) -> ApiLoginPost200Response:
        ...


    async def api_admin_memberships_get(
        self,
    ) -> None:
        ...


    async def api_admin_memberships_user_id_get(
        self,
        user_id: StrictInt,
    ) -> None:
        ...


    async def api_admin_memberships_user_id_renew_post(
        self,
        user_id: StrictInt,
        api_admin_memberships_user_id_renew_post_request: ApiAdminMembershipsUserIdRenewPostRequest,
    ) -> None:
        ...


    async def api_admin_statistics_get(
        self,
    ) -> None:
        ...


    async def api_login_post(
        self,
        api_register_post_request: ApiRegisterPostRequest,
    ) -> ApiLoginPost200Response:
        ...


    async def api_membership_get(
        self,
    ) -> ApiMembershipGet200Response:
        ...


    async def api_notifications_get(
        self,
    ) -> None:
        ...


    async def api_notifications_id_read_put(
        self,
        id: StrictInt,
    ) -> None:
        ...


    async def api_profile_get(
        self,
    ) -> None:
        ...


    async def api_profile_put(
        self,
        api_profile_put_request: ApiProfilePutRequest,
    ) -> None:
        ...


    async def api_redeem_post(
        self,
        api_redeem_post_request: ApiRedeemPostRequest,
    ) -> None:
        ...


    async def api_register_post(
        self,
        api_register_post_request: ApiRegisterPostRequest,
    ) -> None:
        ...
