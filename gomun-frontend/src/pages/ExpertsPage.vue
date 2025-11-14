<script setup lang="ts">
import { computed, inject, onMounted, ref } from 'vue'
import type { Ref } from 'vue'
import ExpertsBoard from '../components/ExpertsBoard.vue'
import { experts as baseExperts, registerDynamicExpert, type Expert } from '../data/experts'
import { fetchExperts } from '../services/experts'
import { createNotification } from '../services/notifications'
import type { StoredSession } from '../utils/session'

const session = inject<Ref<StoredSession | null>>('session', ref(null))

const remoteExperts = ref<Expert[]>([])
const loadingExperts = ref(false)
const expertsError = ref('')
const requestStatus = ref('')
let statusTimer: ReturnType<typeof setTimeout> | null = null

function setStatus(message: string) {
  requestStatus.value = message
  if (statusTimer) clearTimeout(statusTimer)
  statusTimer = setTimeout(() => {
    requestStatus.value = ''
  }, 4000)
}

async function loadDynamicExperts() {
  loadingExperts.value = true
  expertsError.value = ''
  try {
    const data = await fetchExperts()
    remoteExperts.value = data.map((item) =>
      registerDynamicExpert({
        name: item.name,
        title: item.title || item.focus || '전문가',
        region: item.region || '전국',
        rating: item.rating ?? 4.5,
        keywords: item.focus ? item.focus.split(/[\s,]+/).filter(Boolean).slice(0, 3) : [],
        avatar: item.avatar || '/images/av1.svg',
        focus: item.focus || '',
        availability: item.availability || '협의 가능',
        responseTime: item.responseTime || '24시간 이내',
        email: item.email,
      }),
    )
  } catch (err) {
    expertsError.value = err instanceof Error ? err.message : '전문가 정보를 불러오지 못했습니다.'
  } finally {
    loadingExperts.value = false
  }
}

onMounted(loadDynamicExperts)

const boardExperts = computed(() => [...remoteExperts.value, ...baseExperts])

async function handleRequest(expert: Expert) {
  if (!session.value?.token) {
    setStatus('요청을 보내려면 로그인하세요.')
    return
  }
  if (!expert.email) {
    setStatus('이 전문가의 연락처가 없어 요청을 보낼 수 없습니다.')
    return
  }
  setStatus('요청 알림 전송 중...')
  try {
    await createNotification(session.value.token, {
      recipient: expert.email,
      title: '새로운 매칭 요청',
      message: `${session.value.name || '기업'}님이 매칭을 요청했습니다.`,
      tag: '요청',
      actionRoute: '/requests',
    })
    setStatus('요청 알림을 보냈습니다.')
  } catch (err) {
    setStatus(err instanceof Error ? err.message : '요청을 전송하지 못했습니다.')
  }
}
</script>

<template>
  <section class="experts-page">
    <ExpertsBoard :experts="boardExperts" :loading="loadingExperts" :error="expertsError" @send-request="handleRequest" />
    <p class="req-status" v-if="requestStatus">{{ requestStatus }}</p>
  </section>
</template>

<style scoped>
.experts-page {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.req-status {
  text-align: center;
  font-size: 13px;
  color: #2563eb;
}
</style>
