<script setup lang="ts">
import { reactive, ref, watchEffect, watch, computed, provide } from 'vue'
import { RouterView, RouterLink, useRouter, useRoute } from 'vue-router'

import MenuToggle from './components/MenuToggle.vue'
import SideNav from './components/SideNav.vue'
import NotificationsPanel from './components/NotificationsPanel.vue'
import { login, register } from './services/auth'
import type { AuthResponse, RegisterPayload, Role } from './services/auth'
import { clearSession, isSessionExpired, readSession, saveSession } from './utils/session'
import type { StoredSession } from './utils/session'
import { notificationSeed } from './data/notifications'
import type { NotificationItem } from './data/notifications'
import { fetchNotifications, markNotification } from './services/notifications'

const router = useRouter()
const route = useRoute()

const sideOpen = ref(false)
const showAbout = ref(false)
const showAuth = ref(false)
const showNotifications = ref(false)
const dark = ref(false)
const notice = ref('')
let noticeTimer: ReturnType<typeof setTimeout> | null = null

const tabs = [
  { label: 'Home', to: '/' },
  { label: 'Overview', to: '/overview' },
  { label: 'Requests', to: '/requests' },
  { label: 'Experts', to: '/experts' },
  { label: 'Insights', to: '/insights' },
]

const roleOptions: Array<{ value: Role; label: string }> = [
  { value: 'guest', label: '게스트' },
  { value: 'expert', label: '전문가' },
  { value: 'company', label: '기업' },
]

const roleCopy: Record<Role, { label: string; description: string; avatar: string }> = {
  guest: { label: '게스트', description: '둘러보기 전용', avatar: '/images/av1.svg' },
  expert: { label: '전문가', description: '프로필/지원 가능', avatar: '/images/av3.svg' },
  company: { label: '기업', description: '요청 생성/매칭', avatar: '/images/av5.svg' },
}

const stored = readSession()
const initialSession = stored && !isSessionExpired(stored) ? stored : null
if (stored && isSessionExpired(stored)) clearSession()
const currentUser = ref<StoredSession | null>(initialSession)
provide('session', currentUser)

watch(currentUser, (val) => {
  saveSession(val)
})

const guestNotifications = notificationSeed.guest
const apiNotifications = ref<NotificationItem[]>([])
const notificationsLoading = ref(false)
const notificationsError = ref('')
const notifications = computed(() => (currentUser.value ? apiNotifications.value : guestNotifications))
const unreadNotifications = computed(() => notifications.value.filter((item) => !item.read).length)
const notificationRoleLabel = computed(() => {
  if (!currentUser.value) return '게스트'
  return roleCopy[currentUser.value.role]?.label ?? '사용자'
})

const activeRole = computed(() => (currentUser.value ? roleCopy[currentUser.value.role] : null))

const authMode = ref<'login' | 'register'>('login')
const authRole = ref<Role>('expert')
const authForm = reactive({
  name: '',
  email: '',
  password: '',
  confirm: '',
  specialty: '',
  companyName: '',
})
const termsAccepted = ref(false)
const authLoading = ref(false)
const authError = ref('')

const GUEST_SESSION_MS = 30 * 60 * 1000
const FALLBACK_SESSION_SECONDS = 60 * 60

function showNotice(message: string, autoOpenAuth = false) {
  notice.value = message
  if (noticeTimer) clearTimeout(noticeTimer)
  noticeTimer = setTimeout(() => {
    notice.value = ''
  }, 5000)
  if (autoOpenAuth) openAuth('login')
}

function formatRelativeTime(input?: string) {
  if (!input) return ''
  const date = new Date(input)
  if (Number.isNaN(date.getTime())) return ''
  const seconds = Math.floor((Date.now() - date.getTime()) / 1000)
  if (seconds < 60) return '방금 전'
  const minutes = Math.floor(seconds / 60)
  if (minutes < 60) return `${minutes}분 전`
  const hours = Math.floor(minutes / 60)
  if (hours < 24) return `${hours}시간 전`
  const days = Math.floor(hours / 24)
  return `${days}일 전`
}

async function loadNotifications() {
  if (!currentUser.value) {
    apiNotifications.value = []
    return
  }
  notificationsLoading.value = true
  notificationsError.value = ''
  try {
    const data = await fetchNotifications(currentUser.value.token)
    apiNotifications.value = data.map((item) => ({
      id: item.id,
      title: item.title,
      message: item.message,
      tag: item.tag,
      actionRoute: item.actionRoute,
      read: item.read,
      createdAt: item.createdAt,
      time: formatRelativeTime(item.createdAt),
      from: item.from,
    }))
  } catch (err) {
    notificationsError.value = err instanceof Error ? err.message : '알림을 불러오지 못했습니다.'
  } finally {
    notificationsLoading.value = false
  }
}

function buildSession(response: AuthResponse): StoredSession {
  const ttl = Math.max(response.expiresIn || FALLBACK_SESSION_SECONDS, 60)
  return {
    token: response.token,
    role: response.role,
    name: response.name,
    email: response.email,
    expiresAt: Date.now() + ttl * 1000,
  }
}

function toggleNotifications() {
  showNotifications.value = !showNotifications.value
  if (showNotifications.value && currentUser.value) loadNotifications()
}

function closeNotifications() {
  showNotifications.value = false
}

async function markAllNotificationsRead() {
  if (!notifications.value.length) return
  if (!currentUser.value) {
    notifications.value.forEach((item) => (item.read = true))
    return
  }
  const token = currentUser.value.token
  const unread = apiNotifications.value.filter((item) => !item.read)
  await Promise.all(unread.map((item) => markNotification(token, item.id, true).catch(() => null)))
  unread.forEach((item) => (item.read = true))
}

async function handleNotificationAction(item: NotificationItem) {
  if (!currentUser.value) {
    showNotifications.value = false
    openAuth('login')
    return
  }
  if (!item.read) {
    try {
      await markNotification(currentUser.value.token, item.id, true)
      item.read = true
    } catch (err) {
      console.error(err)
    }
  }
  showNotifications.value = false
  if (item.actionRoute) router.push(item.actionRoute)
}

function handleProfileClick() {
  if (!currentUser.value) {
    showNotice('로그인이 필요한 서비스입니다.', true)
    return
  }
  router.push('/profile')
}

function openAuth(mode: 'login' | 'register' = 'login') {
  authMode.value = mode
  Object.assign(authForm, { name: '', email: '', password: '', confirm: '', specialty: '', companyName: '' })
  termsAccepted.value = false
  authError.value = ''
  showAuth.value = true
}

function closeAuth() {
  showAuth.value = false
}

function loginAsGuest() {
  currentUser.value = {
    token: `guest-${Date.now()}`,
    role: 'guest',
    name: '게스트',
    email: 'guest@gomun.kr',
    expiresAt: Date.now() + GUEST_SESSION_MS,
  }
  showAuth.value = false
  showNotice('게스트 모드로 로그인했습니다.')
  apiNotifications.value = []
  notificationsError.value = ''
}

function validateAuthForm() {
  if (authMode.value !== 'register') return
  if (!termsAccepted.value) throw new Error('개인정보 처리방침에 동의해 주세요.')
  if (authForm.password !== authForm.confirm) throw new Error('비밀번호 확인이 일치하지 않습니다.')
  const strongPassword = /^(?=.*[A-Za-z])(?=.*\d).{8,}$/
  if (!strongPassword.test(authForm.password)) throw new Error('비밀번호는 8자 이상, 영문+숫자를 포함해야 합니다.')
  if (!authForm.name.trim()) throw new Error('이름을 입력해 주세요.')
  if (authRole.value === 'company' && !authForm.companyName.trim()) throw new Error('기업명을 입력해 주세요.')
  if (authRole.value === 'expert' && !authForm.specialty.trim()) throw new Error('전문 분야를 입력해 주세요.')
}

async function submitAuth() {
  authError.value = ''
  authLoading.value = true
  try {
    validateAuthForm()
    let response: AuthResponse
    if (authMode.value === 'login') {
      response = await login(authRole.value, authForm.email, authForm.password)
    } else {
      const payload: RegisterPayload = {
        role: authRole.value,
        name: authForm.name,
        email: authForm.email,
        password: authForm.password,
      }
      if (authRole.value === 'company') payload.companyName = authForm.companyName.trim()
      if (authRole.value === 'expert') payload.specialty = authForm.specialty.trim()
      response = await register(payload)
    }
    currentUser.value = buildSession(response)
    showAuth.value = false
    showNotice('정상적으로 인증되었습니다.')
  } catch (err) {
    authError.value = err instanceof Error ? err.message : '처리 중 문제가 발생했습니다.'
  } finally {
    authLoading.value = false
  }
}

function logout(message?: string) {
  currentUser.value = null
  clearSession()
  apiNotifications.value = []
  notificationsError.value = ''
  if (message) showNotice(message, true)
}

watchEffect(() => {
  if (currentUser.value && isSessionExpired(currentUser.value)) {
    logout('세션이 만료되었습니다. 다시 로그인해 주세요.')
  }
})

watch(
  () => currentUser.value,
  (session) => {
    showNotifications.value = false
    if (session) loadNotifications()
    else {
      apiNotifications.value = []
      notificationsError.value = ''
    }
  },
  { immediate: true },
)

function removeAuthQuery() {
  if (!route.query.auth) return
  const nextQuery = { ...route.query }
  delete nextQuery.auth
  router.replace({ query: nextQuery })
}

watch(
  () => route.query.auth,
  (val) => {
    if (!val) return
    const reason = Array.isArray(val) ? val[0] : val
    if (!reason) return
    if (reason === 'required') showNotice('로그인이 필요한 서비스입니다.', true)
    else if (reason === 'expired') showNotice('세션이 만료되었습니다. 다시 로그인해 주세요.', true)
    else if (reason === 'forbidden') showNotice('접근 권한이 없습니다.')
    removeAuthQuery()
  },
  { immediate: true },
)

watchEffect(() => {
  const html = document.documentElement
  if (dark.value) html.setAttribute('data-theme', 'dark')
  else html.removeAttribute('data-theme')
})

watch(
  () => route.path,
  (p) => {
    if (p === '/requests' || p === '/experts') sideOpen.value = true
    showNotifications.value = false
  },
  { immediate: true },
)
</script>



<template>

  <div class="app">

    <header class="app__header">

      <div class="app__brand">

        <img src="/vite.svg" alt="logo" class="brand__logo" />

        <h1 class="brand__title">GOMUN - Zero-Gap HR Tech</h1>

        <nav class="brand-tabs">

          <RouterLink v-for="t in tabs" :key="t.label" class="brand-tab" :to="t.to" active-class="is-active">

            {{ t.label }}

          </RouterLink>

        </nav>

      </div>

      <div class="app__actions">

        <div class="header__spacer"></div>

        <button class="link" @click="showAbout = true">About</button>

        <button class="icon" @click="dark = !dark" :aria-pressed="dark" title="Toggle theme">

          <svg v-if="!dark" width="18" height="18" viewBox="0 0 24 24" fill="none">

            <path

              d="M12 3v2m0 14v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2m18 0h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42M12 7a5 5 0 100 10 5 5 0 000-10z"

              stroke="currentColor"

              stroke-width="1.5"

            />

          </svg>

          <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none">

            <path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z" stroke="currentColor" stroke-width="1.5" fill="currentColor" />

          </svg>

        </button>

        <button
          class="icon notif-toggle"
          aria-label="Notifications"
          title="Notifications"
          :aria-expanded="showNotifications"
          @click="toggleNotifications"
        >

          <svg width="18" height="18" viewBox="0 0 24 24" fill="none">

            <path

              d="M15 17h5l-1.4-1.4A2 2 0 0118 14.2V11a6 6 0 10-12 0v3.2c0 .5-.2 1-.6 1.4L4 17h5m2 4a2 2 0 002-2H9a2 2 0 002 2z"

              stroke="currentColor"

              stroke-width="1.5"

            />

          </svg>

          <span class="notif-dot" v-if="unreadNotifications">{{ unreadNotifications }}</span>

        </button>

        <div class="role-pill" v-if="activeRole">

          <span>{{ activeRole.label }} · {{ currentUser?.name }}</span>

          <small>{{ activeRole.description }}</small>

        </div>

        <button class="link" v-if="currentUser" @click="() => logout()">Logout</button>

        <button class="link" v-else @click="openAuth('login')">Login</button>

        <img

          class="avatar-mini"

          :src="activeRole?.avatar || '/images/av1.svg'"

          :alt="activeRole?.label || 'guest'"

          @click="handleProfileClick"

          title="Profile"

        />

        <MenuToggle v-model="sideOpen" />

      </div>

    </header>

    <div class="app__notice" v-if="notice">

      {{ notice }}

    </div>

    <transition name="fade">

      <NotificationsPanel

        v-if="showNotifications"

        :items="notifications"

        :role-label="notificationRoleLabel"

        :unread="unreadNotifications"

        :loading="notificationsLoading"

        :error="notificationsError"

        @close="closeNotifications"

        @mark="markAllNotificationsRead"

        @open-action="handleNotificationAction"

      />

    </transition>

    <div class="notif-overlay" v-if="showNotifications" @click="closeNotifications"></div>



    <main class="app__main" :class="{ 'with-rail': sideOpen }">

      <transition name="rail">

        <aside v-if="sideOpen" class="rail" @click.self="sideOpen = false">

          <SideNav :is-auth="Boolean(currentUser)" />

        </aside>

      </transition>



      <transition name="modal">

        <section v-if="showAuth" class="modal" @click="closeAuth">

          <article class="modal__content modal__content--wide auth-modal" @click.stop>

            <div class="auth__header">

              <h3>GOMUN 로그인</h3>

              <div class="auth__tabs">

                <button :class="{ active: authMode === 'login' }" @click="authMode = 'login'">로그인</button>

                <button :class="{ active: authMode === 'register' }" @click="authMode = 'register'">회원가입</button>

              </div>

            </div>

            <div class="role-switch auth__roles">

              <button

                v-for="opt in roleOptions"

                :key="opt.value"

                type="button"

                :class="['role-switch__btn', { active: authRole === opt.value }]"

                @click="authRole = opt.value"

              >

                {{ opt.label }}

              </button>

            </div>

            <form class="auth__form" @submit.prevent="submitAuth">

              <label v-if="authMode === 'register'">

                <span>이름</span>

                <input v-model="authForm.name" placeholder="홍길동" autocomplete="name" required />

              </label>

              <label>

                <span>이메일</span>

                <input type="email" v-model="authForm.email" placeholder="email@gomun.kr" autocomplete="email" required />

              </label>

              <label>

                <span>비밀번호</span>

                <input type="password" v-model="authForm.password" placeholder="********" autocomplete="new-password" required />

              </label>

              <label v-if="authMode === 'register'">

                <span>비밀번호 확인</span>

                <input type="password" v-model="authForm.confirm" placeholder="********" autocomplete="new-password" required />

              </label>

              <label v-if="authMode === 'register' && authRole === 'expert'">

                <span>전문 분야</span>

                <input v-model="authForm.specialty" placeholder="예: 전략/PMO" />

              </label>

              <label v-if="authMode === 'register' && authRole === 'company'">

                <span>기업명</span>

                <input v-model="authForm.companyName" placeholder="고문컴퍼니" />

              </label>

              <label class="terms" v-if="authMode === 'register'">

                <input type="checkbox" v-model="termsAccepted" />

                <span>개인정보 처리방침 및 이용약관에 동의합니다.</span>

              </label>

              <p class="auth__error" v-if="authError">{{ authError }}</p>

              <button class="primary" type="submit" :disabled="authLoading || (authMode === 'register' && !termsAccepted)">

                {{ authLoading ? '처리 중...' : authMode === 'login' ? '로그인' : '회원가입' }}

              </button>

            </form>

            <div class="auth__guest">

              <span>아직 계정이 없나요?</span>

              <button class="ghost" @click="loginAsGuest">게스트로 둘러보기</button>

            </div>

          </article>

        </section>

      </transition>



      <section class="app__content">

        <RouterView />

      </section>



      <transition name="modal">

        <section v-if="showAbout" class="modal" @click="showAbout = false">

          <article class="modal__content" @click.stop>

            <h3 class="modal__title">GOMUN Prototype</h3>

            <p class="modal__text">하이-스킬 긱이코노미 기반 Zero-Gap HR Tech. 매칭·계약·정산 자동화로 품질을 보증하는 실험적 브랜드입니다.</p>

            <button class="modal__close" @click="showAbout = false">닫기</button>

          </article>

        </section>

      </transition>

    </main>

  </div>

</template>



<style scoped>

.app {

  --header-h: 56px;
  position: relative;

}

.app__header {

  position: sticky;

  top: 0;

  height: var(--header-h);

  background: #ffffff;

  border-bottom: 1px solid var(--border);

  z-index: 10;

  display: flex;

  align-items: center;

  justify-content: space-between;

  padding: 12px 20px;

  gap: 12px;

}

.app__brand {

  display: flex;

  align-items: center;

  gap: 12px;

}

.brand__logo {

  width: 28px;

  height: 28px;

}

.brand__title {

  font-size: 15px;

  font-weight: 800;

  margin: 0;

}

.brand-tabs {

  display: none;

  gap: 8px;

  margin-left: 14px;

}

.brand-tab {

  text-decoration: none;

  color: inherit;

  padding: 6px 10px;

  border-radius: 8px;

  font-size: 13px;

}

.brand-tab.is-active {

  background: rgba(99, 102, 241, 0.1);

  color: #1e1b4b;

  font-weight: 700;

}

@media (min-width: 900px) {

  .brand-tabs {

    display: flex;

  }

}

.app__actions {

  display: flex;

  align-items: center;

  gap: 12px;

}

.header__spacer {

  flex: 1;

}

.icon {

  border: 0;

  background: transparent;

  color: #475569;

  width: 32px;

  height: 32px;

  display: grid;

  place-items: center;

  border-radius: 8px;

  cursor: pointer;

}

.icon:hover {

  background: rgba(99, 102, 241, 0.08);

  color: #1e293b;

}

.role-switch {

  display: flex;

  background: #f8fafc;

  border: 1px solid var(--border);

  border-radius: 999px;

  padding: 2px;

}

.role-switch__btn {

  border: 0;

  background: transparent;

  font-size: 12px;

  padding: 4px 10px;

  border-radius: 999px;

  cursor: pointer;

  color: #475569;

}

.role-switch__btn.active {

  background: #fff;

  color: #0f172a;

  font-weight: 700;

  box-shadow: 0 4px 12px rgba(15, 23, 42, 0.08);

}

.role-pill {

  display: flex;

  flex-direction: column;

  align-items: flex-end;

  font-size: 11px;

  color: var(--muted);

  line-height: 1.2;

}

.role-pill span {

  font-weight: 700;

  color: #0f172a;

}

.avatar-mini {

  width: 28px;

  height: 28px;

  border-radius: 50%;

  border: 1px solid var(--border);

  cursor: pointer;

}

.app__notice {

  margin: 12px auto 0;

  max-width: 960px;

  background: rgba(163, 230, 53, 0.2);

  border: 1px solid rgba(163, 230, 53, 0.6);

  border-radius: 12px;

  padding: 10px 16px;

  font-size: 14px;

  color: #1f2d11;

  box-shadow: 0 6px 30px rgba(15, 23, 42, 0.05);

}

.link {

  border: 0;

  background: transparent;

  color: #667085;

  cursor: pointer;

}

.link:hover {

  color: #0f172a;

}

.notif-toggle {

  position: relative;

}

.notif-dot {

  position: absolute;

  top: -4px;

  right: -4px;

  min-width: 16px;

  height: 16px;

  padding: 0 4px;

  background: #ef4444;

  color: #fff;

  font-size: 10px;

  border-radius: 999px;

  display: inline-flex;

  align-items: center;

  justify-content: center;

  font-weight: 700;

}

.notif-overlay {

  position: fixed;

  inset: 0;

  background: transparent;

  z-index: 25;

}

.fade-enter-active,
.fade-leave-active {

  transition: opacity 0.2s ease, transform 0.2s ease;

}

.fade-enter-from,
.fade-leave-to {

  opacity: 0;

  transform: translateY(-6px);

}



.app__main {

  position: relative;

  padding: 20px;

}

.app__content {

  padding: 0;

}

.app__main.with-rail {

  padding-right: 340px;

}

.rail {

  position: fixed;

  top: var(--header-h);

  right: 0;

  bottom: 0;

  width: 320px;

  background: var(--surface);

  border-left: 1px solid var(--border);

  box-shadow: 0 6px 30px rgba(15, 23, 42, 0.06);

}

.rail-enter-active,

.rail-leave-active {

  transition: transform 0.22s ease, opacity 0.22s ease;

}

.rail-enter-from,

.rail-leave-to {

  transform: translateY(-8px);

  opacity: 0;

}



.modal {

  position: fixed;

  inset: 0;

  background: rgba(0, 0, 0, 0.08);

  display: grid;

  place-items: center;

  z-index: 20;

}

.modal__content {

  background: var(--surface);

  border: 1px solid var(--border);

  border-radius: 12px;

  max-width: 520px;

  width: 92vw;

  padding: 24px;

}

.modal__content--wide {

  max-width: 520px;

}

.modal__title {

  margin: 0 0 8px;

}

.modal__text {

  margin: 0 0 16px;

  color: var(--muted);

}

.modal__close {

  border: 0;

  background: var(--text, #0f172a);

  color: #fff;

  border-radius: 8px;

  padding: 8px 12px;

  cursor: pointer;

}

.modal-enter-active,

.modal-leave-active {

  transition: opacity 0.2s ease;

}

.modal-enter-from,

.modal-leave-to {

  opacity: 0;

}



.auth-modal {

  max-width: 520px;

}

.auth__header {

  display: flex;

  justify-content: space-between;

  align-items: center;

  gap: 12px;

}

.auth__tabs button {

  border: 0;

  background: transparent;

  padding: 4px 10px;

  border-radius: 8px;

  cursor: pointer;

  font-size: 12px;

}

.auth__tabs button.active {

  background: rgba(99, 102, 241, 0.12);

  color: #1e1b4b;

  font-weight: 700;

}

.auth__roles {

  margin: 12px 0;

}

.auth__form {

  display: flex;

  flex-direction: column;

  gap: 10px;

  margin-top: 10px;

}

.auth__form label {

  display: flex;

  flex-direction: column;

  gap: 4px;

  font-size: 12px;

  color: var(--muted);

}

.auth__form label.terms {

  flex-direction: row;

  align-items: center;

  gap: 8px;

  font-size: 13px;

  color: #1f2937;

}

.auth__form label.terms input[type='checkbox'] {

  width: 16px;

  height: 16px;

}

.auth__form input {

  border: 1px solid var(--border);

  border-radius: 8px;

  padding: 8px;

  font-size: 14px;

}

.auth__error {

  color: #ef4444;

  font-size: 12px;

  margin: 0;

}

.auth__guest {

  margin-top: 12px;

  display: flex;

  align-items: center;

  gap: 10px;

  font-size: 12px;

  color: var(--muted);

}

.primary {

  border: 0;

  background: linear-gradient(120deg, #a3e635, #10b981);

  color: #0f172a;

  font-weight: 700;

  border-radius: 999px;

  padding: 11px 18px;

  font-size: 13px;

  cursor: pointer;

  box-shadow: 0 12px 28px rgba(16, 185, 129, 0.35);

}

.ghost {

  border: 0;

  background: transparent;

  color: var(--muted);

  cursor: pointer;

  font-size: 12px;

}



:global(html[data-theme='dark'] .app__header) {

  background: #0f172a;

  color: #e2e8f0;

}

</style>
