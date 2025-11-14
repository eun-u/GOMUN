import { API_BASE, handleApiResponse } from './client'

export type Role = 'guest' | 'expert' | 'company'

export type AuthResponse = {
  token: string
  role: Role
  name: string
  email: string
  expiresIn: number
}

export type RegisterPayload = {
  role: Role
  name: string
  email: string
  password: string
  companyName?: string
  specialty?: string
}

export async function login(role: Role, email: string, password: string) {
  const res = await fetch(`${API_BASE}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ role, email, password }),
  })
  return handleApiResponse<AuthResponse>(res)
}

export async function register(payload: RegisterPayload) {
  const res = await fetch(`${API_BASE}/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  return handleApiResponse<AuthResponse>(res)
}

