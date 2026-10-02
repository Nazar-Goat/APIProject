from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password:str, hashed_password:str) -> bool:
    """Checks if password matches with password existing in DB"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password:str) -> str:
    """Hashes password for saving in DB"""
    return pwd_context.hash(password)
