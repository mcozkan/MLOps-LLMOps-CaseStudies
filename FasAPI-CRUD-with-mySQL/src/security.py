from passlib.context import CryptContext

# Passlib, bcrypt definition:
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

"""
#While entering our password, compares the hash and hash in the database if it is matched or not...
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
"""