<script setup lang="ts">
import { computed, reactive, ref, onMounted, inject } from 'vue'
import type { Ref } from 'vue'
import { experts } from '../data/experts'
import { fetchProfile, updateProfile } from '../services/profile'
import type { StoredSession } from '../utils/session'

const defaultProfile = {
  name: '김한울',
  title: '전략 컨설턴트',
  region: '서울',
  focus: '',
  availability: '즉시 투입',
  responseTime: '평균 4시간',
  phone: '010-1234-5678',
  website: 'https://gomun.kr',
  bio: '',
}

const fallbackSession = ref<StoredSession | null>(null)
const injectedSession = inject<Ref<StoredSession | null>>('session', fallbackSession)
const session = computed(() => injectedSession?.value ?? null)

const baseExpert = computed(() => {
  const email = session.value?.email
  if (!email) return null
  return experts.find((expert) => expert.email === email)
})

type ProfileState = {
  name: string
  title: string
  region: string
  focus?: string
  availability?: string
  responseTime?: string
  phone?: string
  website?: string
  bio?: string
  avatar?: string
}

const profile = reactive<ProfileState>({
  ...(baseExpert.value ?? defaultProfile),
})

const form = reactive({
  focus: profile.focus || '',
  phone: profile.phone || '',
  website: profile.website || '',
  bio: profile.bio || '',
})

const loading = ref(false)
const saving = ref(false)
const error = ref('')
const success = ref('')

async function loadProfile() {
  const email = session.value?.email
  const token = session.value?.token
  if (!email || !token) return
  loading.value = true
  error.value = ''
  try {
    const data = await fetchProfile(email, token)
    Object.assign(profile, { ...profile, ...data })
    Object.assign(form, {
      focus: data.focus ?? '',
      phone: data.phone ?? '',
      website: data.website ?? '',
      bio: data.bio ?? '',
    })
  } catch (err) {
    error.value = err instanceof Error ? err.message : '프로필을 불러오지 못했습니다.'
  } finally {
    loading.value = false
  }
}

async function saveProfile() {
  const email = session.value?.email
  const token = session.value?.token
  if (!email || !token) return
  saving.value = true
  success.value = ''
  error.value = ''
  try {
    const data = await updateProfile(email, {
      focus: form.focus,
      phone: form.phone,
      website: form.website,
      bio: form.bio,
    }, token)
    Object.assign(profile, { ...profile, ...data })
    success.value = '저장되었습니다.'
  } catch (err) {
    error.value = err instanceof Error ? err.message : '저장에 실패했습니다.'
  } finally {
    saving.value = false
  }
}

onMounted(loadProfile)

const locationText = computed(() => `${profile.region ?? '서울'}, 대한민국`)
</script>

<template>
  <section class="profile">
    <div class="pgrid">
      <aside class="pcol">
        <article class="card">
          <div class="card__body center">
            <img :src="baseExpert?.avatar || '/images/av1.svg'" alt="" class="avatar" />
            <h3 class="name">{{ profile.name }}</h3>
            <p class="muted">{{ profile.title }}</p>
            <p class="muted small">{{ locationText }}</p>
            <div class="actions">
              <button class="btn btn--primary">Contact</button>
              <button class="btn">Bookmark</button>
            </div>
          </div>
        </article>

        <article class="card">
          <ul class="plist">
            <li><span>Email</span><strong>{{ session?.email || 'hanul@gomun.kr' }}</strong></li>
            <li><span>Phone</span><strong>{{ profile.phone }}</strong></li>
            <li><span>Website</span><strong>{{ profile.website }}</strong></li>
          </ul>
        </article>
      </aside>

      <section class="pcol wide">
        <article class="card">
            <div class="card__body">
              <div class="prow"><label>Full Name</label><span>{{ profile.name }}</span></div>
              <div class="prow"><label>Email</label><span>{{ session?.email }}</span></div>
              <div class="prow"><label>Phone</label><span>{{ profile.phone }}</span></div>
              <div class="prow"><label>Address</label><span>{{ locationText }}</span></div>
            </div>
          </article>

        <div class="two">
          <article class="card h">
            <div class="card__body">
              <h4 class="smalltitle">프로필 편집</h4>
              <label class="edit-field">
                <span>Focus</span>
                <textarea v-model="form.focus" rows="2"></textarea>
              </label>
              <label class="edit-field">
                <span>Phone</span>
                <input v-model="form.phone" />
              </label>
              <label class="edit-field">
                <span>Website</span>
                <input v-model="form.website" />
              </label>
              <label class="edit-field">
                <span>Bio</span>
                <textarea v-model="form.bio" rows="3"></textarea>
              </label>
              <div class="save-row">
                <button class="btn btn--primary" :disabled="saving" @click="saveProfile">
                  {{ saving ? '저장 중...' : '저장하기' }}
                </button>
                <span class="status" v-if="success">{{ success }}</span>
                <span class="status error" v-if="error">{{ error }}</span>
              </div>
            </div>
          </article>
        </div>
      </section>
    </div>
  </section>
</template>

<style scoped>
.profile {
  padding: 10px;
}
.pgrid {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 16px;
}
.pcol.wide {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 14px;
  box-shadow: 0 6px 20px rgba(15, 23, 42, 0.04);
}
.card__body {
  padding: 14px;
}
.center {
  text-align: center;
}
.avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  border: 1px solid var(--border);
}
.name {
  margin: 8px 0 4px;
}
.actions {
  display: flex;
  gap: 8px;
  justify-content: center;
  margin-top: 8px;
}
.btn {
  border: 1px solid var(--border);
  background: #fff;
  color: #0f172a;
  padding: 8px 12px;
  border-radius: 10px;
  cursor: pointer;
}
.btn--primary {
  background: var(--indigo, #6366f1);
  color: #fff;
  border-color: var(--indigo, #6366f1);
}
.plist {
  display: grid;
}
.plist li {
  display: flex;
  justify-content: space-between;
  padding: 10px 14px;
  border-top: 1px solid var(--border);
}
.plist li:first-child {
  border-top: 0;
}
.prow {
  display: grid;
  grid-template-columns: 160px 1fr;
  align-items: center;
  padding: 10px 0;
  border-top: 1px solid var(--border);
}
.prow:first-child {
  border-top: 0;
}
.smalltitle {
  margin: 0 0 8px;
}
.two {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}
.h .k {
  margin-bottom: 10px;
}
.bar {
  width: 100%;
  height: 6px;
  background: #eef2ff;
  border-radius: 6px;
  overflow: hidden;
  border: 1px solid #e7ecff;
}
.bar i {
  display: block;
  height: 100%;
  background: var(--indigo, #6366f1);
}
.chip {
  display: inline-block;
  padding: 6px 10px;
  background: #f4f7ff;
  border: 1px solid #e7ecff;
  border-radius: 99px;
  margin: 4px;
}

@media (max-width: 900px) {
  .pgrid {
    grid-template-columns: 1fr;
  }
  .two {
    grid-template-columns: 1fr;
  }
}
</style>
.edit-field {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 13px;
  margin-bottom: 10px;
}
.edit-field input,
.edit-field textarea {
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 8px;
  font-family: inherit;
}
.save-row {
  display: flex;
  gap: 10px;
  align-items: center;
}
.status {
  font-size: 12px;
  color: var(--muted);
}
.status.error {
  color: #ec4899;
}
