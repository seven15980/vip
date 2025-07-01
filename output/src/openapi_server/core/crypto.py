import bcrypt

class Crypto:
    @staticmethod
    def hash_password(password: str, rounds: int = 12) -> str:
        """
        使用 bcrypt 对密码进行加密。
        :param password: 明文密码
        :param rounds: 加密轮数
        :return: 哈希后的密码字符串
        """
        salt = bcrypt.gensalt(rounds)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """
        校验明文密码与哈希值是否匹配。
        :param password: 明文密码
        :param hashed: 哈希后的密码字符串
        :return: 是否匹配
        """
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

# 兼容 API 层直接调用
hash_password = Crypto.hash_password
verify_password = Crypto.verify_password 