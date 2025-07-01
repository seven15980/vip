import random
import string
from typing import List, Set

def generate_card_code(length: int = 12, prefix: str = "", charset: str = string.ascii_uppercase + string.digits) -> str:
    """
    生成单个卡密。
    :param length: 卡密长度（不含前缀）
    :param prefix: 前缀
    :param charset: 可用字符集
    :return: 卡密字符串
    """
    code = ''.join(random.choices(charset, k=length))
    return f"{prefix}{code}"

def batch_generate_card_codes(count: int, length: int = 12, prefix: str = "", charset: str = string.ascii_uppercase + string.digits) -> List[str]:
    """
    批量生成唯一卡密。
    :param count: 数量
    :param length: 单个卡密长度
    :param prefix: 前缀
    :param charset: 字符集
    :return: 唯一卡密列表
    """
    codes: Set[str] = set()
    while len(codes) < count:
        code = generate_card_code(length, prefix, charset)
        codes.add(code)
    return list(codes) 