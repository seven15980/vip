from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta
from typing import Any, Optional
from ..config import settings

class JWTUtil:
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        生成 JWT access token。
        :param data: 需要编码到 token 的数据
        :param expires_delta: 过期时间间隔
        :return: JWT 字符串
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

    @staticmethod
    def decode_token(token: str) -> dict:
        """
        解码并校验 JWT token。
        :param token: JWT 字符串
        :return: 解码后的数据字典
        :raises: ExpiredSignatureError, JWTError
        """
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            return payload
        except ExpiredSignatureError as e:
            raise e
        except JWTError as e:
            raise e

# 兼容 API 层直接调用
create_access_token = JWTUtil.create_access_token
decode_access_token = JWTUtil.decode_token 