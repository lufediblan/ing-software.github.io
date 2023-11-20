from bcrypt import hashpw, gensalt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    salt = gensalt()
    hashed_password = hashpw(password.encode("utf-8"), salt)
    return hashed_password

def verfiy_password(plane_password, hashed_password):
    return pwd_context.verify(plane_password, hashed_password)