import { API_BASE, authHeaders, handleApiResponse } from './client'

export type ProfilePayload = {
  name?: string
  title?: string
  region?: string
  focus?: string
  availability?: string
  responseTime?: string
  phone?: string
  website?: string
  bio?: string
}

export async function fetchProfile(email: string, token: string): Promise<ProfilePayload> {
  const res = await fetch(`${API_BASE}/profile/${encodeURIComponent(email)}`, {
    headers: authHeaders(token),
  })
  return handleApiResponse<ProfilePayload>(res)
}

export async function updateProfile(email: string, payload: ProfilePayload, token: string): Promise<ProfilePayload> {
  const res = await fetch(`${API_BASE}/profile/${encodeURIComponent(email)}`, {
    method: 'PATCH',
    headers: authHeaders(token),
    body: JSON.stringify(payload),
  })
  return handleApiResponse<ProfilePayload>(res)
}
