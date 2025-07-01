# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.default_api_base import BaseDefaultApi
import openapi_server.impl

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    Response,
    Security,
    status,
)

from openapi_server.models.extra_models import TokenModel  # noqa: F401
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

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/api/admin/card-codes/{code}/logs",
    responses={
        200: {"description": "使用记录"},
    },
    tags=["管理后台"],
    summary="查询某个卡密的使用记录",
    response_model_by_alias=True,
)
async def api_admin_card_codes_code_logs_get(
    code: StrictStr = Path(..., description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> None:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().api_admin_card_codes_code_logs_get(code)


@router.get(
    "/api/admin/card-codes",
    responses={
        200: {"description": "卡密列表"},
    },
    tags=["管理后台"],
    summary="查询卡密列表",
    response_model_by_alias=True,
)
async def api_admin_card_codes_get(
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> None:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().api_admin_card_codes_get()


@router.post(
    "/api/admin/card-codes",
    responses={
        200: {"description": "生成的卡密列表"},
    },
    tags=["管理后台"],
    summary="批量生成卡密",
    response_model_by_alias=True,
)
async def api_admin_card_codes_post(
    api_admin_card_codes_post_request: ApiAdminCardCodesPostRequest = Body(None, description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> None:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().api_admin_card_codes_post(api_admin_card_codes_post_request)


@router.post(
    "/api/admin/login",
    responses={
        200: {"model": ApiLoginPost200Response, "description": "登录成功"},
        401: {"description": "登录失败"},
    },
    tags=["管理后台"],
    summary="管理员登录",
    response_model_by_alias=True,
)
async def api_admin_login_post(
    api_admin_login_post_request: ApiAdminLoginPostRequest = Body(None, description=""),
) -> ApiLoginPost200Response:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().api_admin_login_post(api_admin_login_post_request)


@router.get(
    "/api/admin/memberships",
    responses={
        200: {"description": "会员列表"},
    },
    tags=["管理后台"],
    summary="查询会员列表",
    response_model_by_alias=True,
)
async def api_admin_memberships_get(
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> None:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().api_admin_memberships_get()


@router.get(
    "/api/admin/memberships/{user_id}",
    responses={
        200: {"description": "会员详情"},
    },
    tags=["管理后台"],
    summary="查询某个用户的会员详情",
    response_model_by_alias=True,
)
async def api_admin_memberships_user_id_get(
    user_id: StrictInt = Path(..., description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> None:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().api_admin_memberships_user_id_get(user_id)


@router.post(
    "/api/admin/memberships/{user_id}/renew",
    responses={
        200: {"description": "续费成功"},
    },
    tags=["管理后台"],
    summary="管理员手动为用户续费/调整会员",
    response_model_by_alias=True,
)
async def api_admin_memberships_user_id_renew_post(
    user_id: StrictInt = Path(..., description=""),
    api_admin_memberships_user_id_renew_post_request: ApiAdminMembershipsUserIdRenewPostRequest = Body(None, description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> None:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().api_admin_memberships_user_id_renew_post(user_id, api_admin_memberships_user_id_renew_post_request)


@router.get(
    "/api/admin/statistics",
    responses={
        200: {"description": "统计数据"},
    },
    tags=["管理后台"],
    summary="获取数据统计",
    response_model_by_alias=True,
)
async def api_admin_statistics_get(
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> None:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().api_admin_statistics_get()


@router.post(
    "/api/login",
    responses={
        200: {"model": ApiLoginPost200Response, "description": "登录成功"},
        401: {"description": "登录失败"},
    },
    tags=["用户"],
    summary="用户登录",
    response_model_by_alias=True,
)
async def api_login_post(
    api_register_post_request: ApiRegisterPostRequest = Body(None, description=""),
) -> ApiLoginPost200Response:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().api_login_post(api_register_post_request)


@router.get(
    "/api/membership",
    responses={
        200: {"model": ApiMembershipGet200Response, "description": "会员信息"},
    },
    tags=["会员"],
    summary="获取当前用户会员信息",
    response_model_by_alias=True,
)
async def api_membership_get(
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> ApiMembershipGet200Response:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().api_membership_get()


@router.get(
    "/api/notifications",
    responses={
        200: {"description": "通知列表"},
    },
    tags=["通知"],
    summary="获取系统通知列表",
    response_model_by_alias=True,
)
async def api_notifications_get(
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> None:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().api_notifications_get()


@router.put(
    "/api/notifications/{id}/read",
    responses={
        200: {"description": "标记成功"},
    },
    tags=["通知"],
    summary="标记通知为已读",
    response_model_by_alias=True,
)
async def api_notifications_id_read_put(
    id: StrictInt = Path(..., description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> None:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().api_notifications_id_read_put(id)


@router.get(
    "/api/profile",
    responses={
        200: {"description": "个人信息"},
    },
    tags=["用户"],
    summary="获取个人信息",
    response_model_by_alias=True,
)
async def api_profile_get(
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> None:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().api_profile_get()


@router.put(
    "/api/profile",
    responses={
        200: {"description": "修改成功"},
    },
    tags=["用户"],
    summary="修改个人信息",
    response_model_by_alias=True,
)
async def api_profile_put(
    api_profile_put_request: ApiProfilePutRequest = Body(None, description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> None:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().api_profile_put(api_profile_put_request)


@router.post(
    "/api/redeem",
    responses={
        200: {"description": "兑换结果"},
        400: {"description": "卡密无效或已使用"},
    },
    tags=["卡密"],
    summary="卡密兑换/续费",
    response_model_by_alias=True,
)
async def api_redeem_post(
    api_redeem_post_request: ApiRedeemPostRequest = Body(None, description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> None:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().api_redeem_post(api_redeem_post_request)


@router.post(
    "/api/register",
    responses={
        200: {"description": "注册成功"},
        400: {"description": "参数错误或邮箱已注册"},
    },
    tags=["用户"],
    summary="用户注册",
    response_model_by_alias=True,
)
async def api_register_post(
    api_register_post_request: ApiRegisterPostRequest = Body(None, description=""),
) -> None:
    if not BaseDefaultApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDefaultApi.subclasses[0]().api_register_post(api_register_post_request)
