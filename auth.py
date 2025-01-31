from fastapi import APIRouter,HTTPException,Request,Depends
from fastapi.security import OAuth2PasswordRequestForm
from schemas import RegisterSchema,LoginSchema
from models import User
from general import dependency
from passlib.context import CryptContext
from jose import jwt,JWTError
from datetime import datetime, timedelta
from pytz import timezone
from config import SECRET_KEY,ALGORITHM
# pip install python-jose[cryptography] bu jwt token generate qilish uchun

# pip install passlib[bcrypt] passwordni hashlash uchun 

router = APIRouter(tags=["auth"],prefix="/auth")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone('Asia/Tashkent')) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    token =  jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_access_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        print(e)
        raise HTTPException(status_code=400, detail="Token expired or invalid")

@router.post("/register",status_code=201)
async def register_user(register_user: RegisterSchema,db: dependency):
    if db.query(User).filter(User.email == register_user.email).first():
        raise HTTPException(status_code=400,detail="This email address is already registered")
    if db.query(User).filter(User.username == register_user.username).first():
        raise HTTPException(status_code=400, detail="This username is already taken")
    
    user = User(
        first_name=register_user.first_name,
        last_name=register_user.last_name,
        email=register_user.email,
        age=register_user.age,
        username=register_user.username,  
        password=pwd_context.hash(register_user.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user



@router.post("/login",status_code=200)
async def login_user(login_schema: LoginSchema,db: dependency,request: Request):
    print("REQ",request.headers)
    user = db.query(User).filter(User.username == login_schema.username).first()
    if not user or not pwd_context.verify(login_schema.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    data_for_token = {"id": user.id,"username": user.username}
    return {
        "success": True,
        "message": "Successfully authenticated",
        "token": create_access_token(data_for_token),
    }
    
# @router.post("/token",status_code=200)
# async def login_user(db: dependency,form_data: OAuth2PasswordRequestForm = Depends()):
#     user = db.query(User).filter(User.username == form_data.username).first()
#     if not user or not pwd_context.verify(form_data.password, user.password):
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
    
#     data_for_token = {"id": user.id,"username": user.username}
#     token = create_access_token(data_for_token)
#     return {"access_token": token, "token_type": "bearer"}