import { API_BASE, authHeaders, handleApiResponse } from './client'

export type RemoteNotification = {
  id: string
  title: string
  message: string
  tag?: string
  actionRoute?: string
  read: boolean
  createdAt: string
  from: string
}

export type NotificationPayload = {
  recipient: string
  title: string
  message: string
  tag?: string
  actionRoute?: string
}

export async function fetchNotifications(token: string) {
  const res = await fetch(`${API_BASE}/notifications`, {
    headers: authHeaders(token),
  })
  return handleApiResponse<RemoteNotification[]>(res)
}

export async function createNotification(token: string, payload: NotificationPayload) {
  const res = await fetch(`${API_BASE}/notifications`, {
    method: 'POST',
    headers: authHeaders(token),
    body: JSON.stringify(payload),
  })
  return handleApiResponse<RemoteNotification>(res)
}

export async function markNotification(token: string, id: string, read: boolean) {
  const res = await fetch(`${API_BASE}/notifications/${encodeURIComponent(id)}`, {
    method: 'PATCH',
    headers: authHeaders(token),
    body: JSON.stringify({ read }),
  })
  return handleApiResponse<RemoteNotification>(res)
}
