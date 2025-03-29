from jose import JWTError, jwt
from datetime import datetime, timedelta
from schemas import TokenData
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# SECKEY_KEY
# ALGORITHM
# Expiration time

SECKEY_KEY = "5vsddcjcnskcscdscsjkdndc558gfmitriotg79gvfvj" # This should be a long, random string
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data:dict):
    to_encode = data.copy()
    
    expire =  datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) # If error occur change this to .utcnow()
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECKEY_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token:str, credentials_exception):

    try:
        payload = jwt.decode(token, SECKEY_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        if not user_id:
            raise credentials_exception
        token_data = TokenData(id= str(user_id))

    except JWTError:
        raise credentials_exception

    return token_data

def get_current_user(token:str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    return  verify_access_token(token, credentials_exception)



