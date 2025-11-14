import { API_BASE, handleApiResponse } from './client'

export type RemoteExpert = {
  name: string
  email: string
  title?: string
  region?: string
  focus?: string
  availability?: string
  responseTime?: string
  rating?: number
  avatar?: string
}

export async function fetchExperts() {
  const res = await fetch(`${API_BASE}/experts`)
  return handleApiResponse<RemoteExpert[]>(res)
}
