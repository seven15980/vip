# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import StrictInt, StrictStr  # noqa: F401
from typing import Any  # noqa: F401
from openapi_server.models.api_admin_card_codes_post_request import ApiAdminCardCodesPostRequest  # noqa: F401
from openapi_server.models.api_admin_login_post_request import ApiAdminLoginPostRequest  # noqa: F401
from openapi_server.models.api_admin_memberships_user_id_renew_post_request import ApiAdminMembershipsUserIdRenewPostRequest  # noqa: F401
from openapi_server.models.api_login_post200_response import ApiLoginPost200Response  # noqa: F401
from openapi_server.models.api_membership_get200_response import ApiMembershipGet200Response  # noqa: F401
from openapi_server.models.api_profile_put_request import ApiProfilePutRequest  # noqa: F401
from openapi_server.models.api_redeem_post_request import ApiRedeemPostRequest  # noqa: F401
from openapi_server.models.api_register_post_request import ApiRegisterPostRequest  # noqa: F401


def test_api_admin_card_codes_code_logs_get(client: TestClient):
    """Test case for api_admin_card_codes_code_logs_get

    查询某个卡密的使用记录
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/api/admin/card-codes/{code}/logs".format(code='code_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_api_admin_card_codes_get(client: TestClient):
    """Test case for api_admin_card_codes_get

    查询卡密列表
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/api/admin/card-codes",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_api_admin_card_codes_post(client: TestClient):
    """Test case for api_admin_card_codes_post

    批量生成卡密
    """
    api_admin_card_codes_post_request = openapi_server.ApiAdminCardCodesPostRequest()

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/api/admin/card-codes",
    #    headers=headers,
    #    json=api_admin_card_codes_post_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_api_admin_login_post(client: TestClient):
    """Test case for api_admin_login_post

    管理员登录
    """
    api_admin_login_post_request = openapi_server.ApiAdminLoginPostRequest()

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/api/admin/login",
    #    headers=headers,
    #    json=api_admin_login_post_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_api_admin_memberships_get(client: TestClient):
    """Test case for api_admin_memberships_get

    查询会员列表
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/api/admin/memberships",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_api_admin_memberships_user_id_get(client: TestClient):
    """Test case for api_admin_memberships_user_id_get

    查询某个用户的会员详情
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/api/admin/memberships/{user_id}".format(user_id=56),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_api_admin_memberships_user_id_renew_post(client: TestClient):
    """Test case for api_admin_memberships_user_id_renew_post

    管理员手动为用户续费/调整会员
    """
    api_admin_memberships_user_id_renew_post_request = openapi_server.ApiAdminMembershipsUserIdRenewPostRequest()

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/api/admin/memberships/{user_id}/renew".format(user_id=56),
    #    headers=headers,
    #    json=api_admin_memberships_user_id_renew_post_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_api_admin_statistics_get(client: TestClient):
    """Test case for api_admin_statistics_get

    获取数据统计
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/api/admin/statistics",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_api_login_post(client: TestClient):
    """Test case for api_login_post

    用户登录
    """
    api_register_post_request = openapi_server.ApiRegisterPostRequest()

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/api/login",
    #    headers=headers,
    #    json=api_register_post_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_api_membership_get(client: TestClient):
    """Test case for api_membership_get

    获取当前用户会员信息
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/api/membership",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_api_notifications_get(client: TestClient):
    """Test case for api_notifications_get

    获取系统通知列表
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/api/notifications",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_api_notifications_id_read_put(client: TestClient):
    """Test case for api_notifications_id_read_put

    标记通知为已读
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/api/notifications/{id}/read".format(id=56),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_api_profile_get(client: TestClient):
    """Test case for api_profile_get

    获取个人信息
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/api/profile",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_api_profile_put(client: TestClient):
    """Test case for api_profile_put

    修改个人信息
    """
    api_profile_put_request = openapi_server.ApiProfilePutRequest()

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/api/profile",
    #    headers=headers,
    #    json=api_profile_put_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_api_redeem_post(client: TestClient):
    """Test case for api_redeem_post

    卡密兑换/续费
    """
    api_redeem_post_request = openapi_server.ApiRedeemPostRequest()

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/api/redeem",
    #    headers=headers,
    #    json=api_redeem_post_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_api_register_post(client: TestClient):
    """Test case for api_register_post

    用户注册
    """
    api_register_post_request = openapi_server.ApiRegisterPostRequest()

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/api/register",
    #    headers=headers,
    #    json=api_register_post_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

