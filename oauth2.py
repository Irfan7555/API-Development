from jose import JWTError, jwt
from datetime import datetime, timedelta

# SECKEY_KEY
# ALGORITHM
# Expiration time

SECKEY_KEY = "5vsddcjcnskcscdscsjkdndc558gfmitriotg79gvfvj" # This should be a long, random string
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 


def create_access_token(data:dict):
    to_encode = data.copy()
    
    expire =  datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECKEY_KEY, algorithm=ALGORITHM)

    return encoded_jwt