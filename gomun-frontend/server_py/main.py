import secrets
from datetime import datetime, timedelta, timezone
from uuid import uuid4
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List


class AuthPayload(BaseModel):
  role: str
  email: str
  password: str
  name: str | None = None
  companyName: str | None = None
  specialty: str | None = None


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


class NotificationCreatePayload(BaseModel):
  recipient: str
  title: str
  message: str
  tag: str | None = None
  actionRoute: str | None = None


class NotificationUpdatePayload(BaseModel):
  read: bool


app = FastAPI()
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

users: List[Dict[str, str]] = []
profiles: Dict[str, Dict[str, str]] = {}
notifications: Dict[str, List[Dict[str, Any]]] = {}
SESSION_DURATION = timedelta(hours=1)
sessions: Dict[str, Dict[str, Any]] = {}


def issue_session(email: str):
  token = secrets.token_urlsafe(32)
  expires_at = datetime.utcnow() + SESSION_DURATION
  sessions[token] = {"email": email, "expires_at": expires_at}
  return token, int(SESSION_DURATION.total_seconds())


def require_session(authorization: str | None):
  if not authorization or not authorization.startswith("Bearer "):
    raise HTTPException(status_code=401, detail="인증 토큰이 필요합니다.")
  token = authorization.split(" ", 1)[1].strip()
  session = sessions.get(token)
  if not session:
    raise HTTPException(status_code=401, detail="세션이 유효하지 않습니다.")
  if session["expires_at"] < datetime.utcnow():
    sessions.pop(token, None)
    raise HTTPException(status_code=401, detail="세션이 만료되었습니다.")
  return session["email"]


def find_user(email: str):
  return next((u for u in users if u["email"] == email), None)


@app.post("/api/login")
async def login(payload: AuthPayload):
  user = next(
    (u for u in users if u["role"] == payload.role and u["email"] == payload.email and u["password"] == payload.password),
    None,
  )
  if not user:
    raise HTTPException(status_code=401, detail="계정 정보를 확인해 주세요.")
  token, expires_in = issue_session(user["email"])
  return {"token": token, "role": user["role"], "name": user["name"], "email": user["email"], "expiresIn": expires_in}


@app.post("/api/register")
async def register(payload: AuthPayload):
  if len(payload.password) < 8 or not any(c.isalpha() for c in payload.password) or not any(c.isdigit() for c in payload.password):
    raise HTTPException(status_code=400, detail="비밀번호는 8자 이상, 영문+숫자를 포함해야 합니다.")
  if any(u["email"] == payload.email for u in users):
    raise HTTPException(status_code=409, detail="이미 등록된 이메일입니다.")
  if payload.role == "company" and not (payload.companyName or "").strip():
    raise HTTPException(status_code=400, detail="기업명을 입력해 주세요.")
  if payload.role == "expert" and not (payload.specialty or "").strip():
    raise HTTPException(status_code=400, detail="전문 분야를 입력해 주세요.")

  user = {
    "role": payload.role,
    "name": payload.name or "사용자",
    "email": payload.email,
    "password": payload.password,
    "companyName": payload.companyName or "",
    "specialty": payload.specialty or "",
  }
  users.append(user)

  if payload.role == "expert":
    profiles[payload.email] = {
      "name": user["name"],
      "title": payload.specialty or "전문가",
      "region": "",
      "focus": payload.specialty or "",
      "availability": "",
      "responseTime": "",
      "phone": "",
      "website": "",
      "bio": "",
    }

  token, expires_in = issue_session(user["email"])
  return {"token": token, "role": user["role"], "name": user["name"], "email": user["email"], "expiresIn": expires_in}


@app.get("/api/profile/{email}")
async def get_profile(email: str, authorization: str | None = Header(default=None)):
  requester = require_session(authorization)
  if requester != email:
    raise HTTPException(status_code=403, detail="본인 프로필만 조회할 수 있습니다.")
  profile = profiles.get(email)
  if not profile:
    raise HTTPException(status_code=404, detail="프로필을 찾을 수 없습니다.")
  return profile


@app.patch("/api/profile/{email}")
async def update_profile(email: str, payload: ProfilePayload, authorization: str | None = Header(default=None)):
  requester = require_session(authorization)
  if requester != email:
    raise HTTPException(status_code=403, detail="본인 프로필만 수정할 수 있습니다.")
  profile = profiles.get(email)
  if not profile:
    raise HTTPException(status_code=404, detail="프로필을 찾을 수 없습니다.")
  profiles[email] = {**profile, **{k: v for k, v in payload.dict().items() if v is not None}}
  return profiles[email]


@app.get("/api/notifications")
async def list_notifications(authorization: str | None = Header(default=None)):
  email = require_session(authorization)
  return notifications.get(email, [])


@app.post("/api/notifications")
async def create_notification(payload: NotificationCreatePayload, authorization: str | None = Header(default=None)):
  sender = require_session(authorization)
  recipient = find_user(payload.recipient)
  if not recipient:
    raise HTTPException(status_code=404, detail="수신자를 찾을 수 없습니다.")
  now = datetime.now(timezone.utc).isoformat()
  note = {
    "id": str(uuid4()),
    "title": payload.title,
    "message": payload.message,
    "tag": payload.tag,
    "actionRoute": payload.actionRoute,
    "read": False,
    "from": sender,
    "createdAt": now,
  }
  notifications.setdefault(payload.recipient, []).insert(0, note)
  return note


@app.patch("/api/notifications/{notification_id}")
async def update_notification(notification_id: str, payload: NotificationUpdatePayload, authorization: str | None = Header(default=None)):
  email = require_session(authorization)
  user_notifications = notifications.get(email, [])
  note = next((n for n in user_notifications if n["id"] == notification_id), None)
  if not note:
    raise HTTPException(status_code=404, detail="알림을 찾을 수 없습니다.")
  note["read"] = payload.read
  return note


@app.get("/api/experts")
async def list_experts():
  result = []
  for user in users:
    if user.get("role") != "expert":
      continue
    profile = profiles.get(user["email"], {})
    result.append(
      {
        "name": user["name"],
        "email": user["email"],
        "title": profile.get("title") or user.get("specialty") or "전문가",
        "region": profile.get("region") or "전국",
        "focus": profile.get("focus") or user.get("specialty") or "",
        "availability": profile.get("availability") or "협의 가능",
        "responseTime": profile.get("responseTime") or "24시간 이내",
        "avatar": profile.get("avatar") or "/images/av1.svg",
        "rating": 4.5,
      }
    )
  return result
