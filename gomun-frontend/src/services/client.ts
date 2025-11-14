const RAW_BASE = (import.meta as any).env?.VITE_API_BASE ?? ''

function normalizeBase(raw: string) {
  const trimmed = raw.trim().replace(/\/+$/, '')
  if (!trimmed) return '/api'
  return trimmed.endsWith('/api') ? trimmed : `${trimmed}/api`
}

export const API_BASE = normalizeBase(RAW_BASE)

export async function handleApiResponse<T>(res: Response): Promise<T> {
  const raw = await res.text()
  if (!res.ok) {
    let message = `API 요청이 실패했습니다. (status ${res.status})`
    try {
      const data = JSON.parse(raw || '{}')
      message = data.message || data.detail || message
    } catch {
      message = `${message}: ${raw.slice(0, 120)}`
    }
    throw new Error(message)
  }
  return raw ? JSON.parse(raw) : ({} as T)
}

export function authHeaders(token?: string) {
  const headers: Record<string, string> = { 'Content-Type': 'application/json' }
  if (token) headers.Authorization = `Bearer ${token}`
  return headers
}
