import os


class settings():
    JWT_SECRET_KEY :str  = os.getenv("SECRET_KEY", "change_in_production")
    JWT_ALGORITHM : str ="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES:int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    API_V1_STR: str = "/api/v1"

settings = settings()