import type { Role } from '../services/auth'

export type StoredSession = {
  token: string
  role: Role
  name: string
  email: string
  expiresAt: number
}

export const STORAGE_KEY = 'gomun:user'

function getStorage() {
  if (typeof window === 'undefined') return null
  return window.localStorage
}

export function readSession(): StoredSession | null {
  const storage = getStorage()
  if (!storage) return null
  try {
    const raw = storage.getItem(STORAGE_KEY)
    if (!raw) return null
    const parsed = JSON.parse(raw) as StoredSession
    if (!parsed?.expiresAt || Number.isNaN(parsed.expiresAt)) return null
    return parsed
  } catch {
    return null
  }
}

export function isSessionExpired(session: StoredSession | null) {
  if (!session) return true
  return session.expiresAt <= Date.now()
}

export function saveSession(session: StoredSession | null) {
  const storage = getStorage()
  if (!storage) return
  if (!session) storage.removeItem(STORAGE_KEY)
  else storage.setItem(STORAGE_KEY, JSON.stringify(session))
}

export function clearSession() {
  saveSession(null)
}
