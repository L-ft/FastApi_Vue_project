from pydantic import BaseModel


# ---------------- Pydantic ----------------
class UserCreate(BaseModel):
    """
    用户创建模型。

    属性:
    username (str): 用户名。
    password (str): 原始密码。
    """
    username: str
    password: str


class Token(BaseModel):
    """
    JWT令牌响应模型。

    属性:
    access_token (str): 编码后的JWT令牌。
    token_type (str): 令牌类型，通常是"bearer"。
    """
    access_token: str
    token_type: str