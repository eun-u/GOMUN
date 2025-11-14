from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


class AuthPayload(BaseModel):
  role: str
  email: str
  password: str
  name: str | None = None


app = FastAPI()
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_methods=["*"],
  allow_headers=["*"],
)

# users = [
#   {"role": "expert", "name": "김한울", "email": "hanul@gomun.kr", "password": "gomun123"},
#   {"role": "company", "name": "고문매칭 기업", "email": "company@gomun.kr", "password": "gomun123"},
# ]


@app.post('/api/login')
async def login(payload: AuthPayload):
  user = next((u for u in users if u['role'] == payload.role and u['email'] == payload.email and u['password'] == payload.password), None)
  if not user:
    raise HTTPException(status_code=401, detail='계정 정보를 확인해 주세요.')
  return {"token": f"mock-{payload.email}", "role": user["role"], "name": user["name"], "email": user["email"]}


@app.post('/api/register')
async def register(payload: AuthPayload):
  if any(u["email"] == payload.email for u in users):
    raise HTTPException(status_code=409, detail='이미 등록된 이메일입니다.')
  user = {"role": payload.role, "name": payload.name or "사용자", "email": payload.email, "password": payload.password}
  users.append(user)
  return {"token": f"mock-{payload.email}", "role": user["role"], "name": user["name"], "email": user["email"]}
