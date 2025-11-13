from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict


class AuthPayload(BaseModel):
  role: str
  email: str
  password: str
  name: str | None = None


class ProfilePayload(BaseModel):
  name: str | None = None
  title: str | None = None
  region: str | None = None
  focus: str | None = None
  availability: str | None = None
  responseTime: str | None = None
  phone: str | None = None
  website: str | None = None
  bio: str | None = None


app = FastAPI()
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

users: list[Dict[str, str]] = [
  {"role": "expert", "name": "김한울", "email": "hanul@gomun.kr", "password": "gomun123"},
  {"role": "company", "name": "고문매칭 기업", "email": "company@gomun.kr", "password": "gomun123"},
]

profiles: Dict[str, Dict[str, str]] = {
  "hanul@gomun.kr": {
    "name": "김한울",
    "title": "전략 컨설턴트",
    "region": "서울",
    "focus": "대기업 HQ 전략실 및 중견기업 PMO 리드",
    "availability": "즉시 투입",
    "responseTime": "평균 4시간",
    "phone": "010-1234-5678",
    "website": "https://gomun.kr",
    "bio": "하이-스킬 공백을 메우는 Zero-Gap HR 전문가입니다.",
  }
}


@app.post("/api/login")
async def login(payload: AuthPayload):
  user = next(
    (u for u in users if u["role"] == payload.role and u["email"] == payload.email and u["password"] == payload.password),
    None,
  )
  if not user:
    raise HTTPException(status_code=401, detail="계정 정보를 확인해 주세요.")
  return {"token": f"mock-{payload.email}", "role": user["role"], "name": user["name"], "email": user["email"]}


@app.post("/api/register")
async def register(payload: AuthPayload):
  if any(u["email"] == payload.email for u in users):
    raise HTTPException(status_code=409, detail="이미 등록된 이메일입니다.")
  user = {"role": payload.role, "name": payload.name or "사용자", "email": payload.email, "password": payload.password}
  users.append(user)
  if payload.role == "expert":
    profiles[payload.email] = {
      "name": user["name"],
      "title": "전문가",
      "region": "서울",
      "focus": "",
      "availability": "즉시 투입",
      "responseTime": "평균 4시간",
      "phone": "",
      "website": "",
      "bio": "",
    }
  return {"token": f"mock-{payload.email}", "role": user["role"], "name": user["name"], "email": user["email"]}


@app.get("/api/profile/{email}")
async def get_profile(email: str):
  profile = profiles.get(email)
  if not profile:
    raise HTTPException(status_code=404, detail="프로필을 찾을 수 없습니다.")
  return profile


@app.patch("/api/profile/{email}")
async def update_profile(email: str, payload: ProfilePayload):
  profile = profiles.get(email)
  if not profile:
    raise HTTPException(status_code=404, detail="프로필을 찾을 수 없습니다.")
  profiles[email] = {**profile, **{k: v for k, v in payload.dict().items() if v is not None}}
  return profiles[email]
