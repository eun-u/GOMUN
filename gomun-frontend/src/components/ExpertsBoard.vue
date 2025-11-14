<script setup lang="ts">
import { computed, reactive } from 'vue'
import { RouterLink } from 'vue-router'
import type { Expert } from '../data/experts'
import { KOREAN_REGIONS } from '../data/options'

const REGIONS = ['전국', ...KOREAN_REGIONS]

const filters = reactive({
  region: '전국',
  search: '',
})

const props = defineProps<{ experts: Expert[]; loading?: boolean; error?: string }>()
const emit = defineEmits<{ 'send-request': [expert: Expert] }>()

const filteredExperts = computed<Expert[]>(() =>
  (props.experts || []).filter((expert) => {
    if (filters.region !== '전국' && expert.region !== filters.region) return false
    if (filters.search.trim()) {
      const term = filters.search.trim().toLowerCase()
      const haystack = `${expert.name} ${expert.title} ${expert.focus}`.toLowerCase()
      if (!haystack.includes(term)) return false
    }
    return true
  }),
)

function handleRequest(expert: Expert, event?: Event) {
  if (event) {
    event.preventDefault()
    event.stopPropagation()
  }
  emit('send-request', expert)
}
</script>

<template>
  <section class="experts-board">
    <header class="board-header">
      <div>
        <p class="label">전문가 보드</p>
        <h2>LinkedIn 감성의 1촌 리스트</h2>
        <p class="lede">간단 프로필을 확인하고, 상세 페이지에서 경험과 케이스를 확인하세요.</p>
      </div>
      <div class="filters">
        <label>
          <span>지역</span>
          <select v-model="filters.region">
            <option v-for="opt in REGIONS" :key="opt">{{ opt }}</option>
          </select>
        </label>
        <label class="search">
          <span>검색</span>
          <input v-model="filters.search" placeholder="이름, 역할, 키워드" type="search" />
        </label>
      </div>
    </header>

    <div class="cards">
      <article v-for="expert in filteredExperts" :key="expert.id" class="card">
        <RouterLink :to="`/experts/${expert.id}`" class="card-link">
          <div class="hero">
            <img class="avatar" :src="expert.avatar" :alt="expert.name" />
          </div>
          <div class="body">
            <h3>{{ expert.name }}</h3>
            <p class="title">{{ expert.title }}</p>
            <p class="meta">{{ expert.region }} · {{ expert.availability }}</p>
            <p class="rating">평점 {{ expert.rating.toFixed(1) }}</p>
          </div>
        </RouterLink>
        <button class="chip" type="button" @click.stop.prevent="handleRequest(expert, $event)">Send 요청 보내기</button>
      </article>
    </div>
    <p v-if="loading" class="empty">전문가 정보를 불러오는 중입니다...</p>
    <p v-else-if="error" class="empty error">{{ error }}</p>
    <p v-else-if="!filteredExperts.length" class="empty">조건에 맞는 전문가가 없습니다.</p>
  </section>
</template>

<style scoped>
.experts-board {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.board-header {
  background: #fff;
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.label {
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-size: 12px;
  color: var(--muted);
  margin: 0;
}
.lede {
  margin: 4px 0 0;
  color: var(--muted);
}
.filters {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 12px;
}
.filters label {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 12px;
  color: var(--muted);
}
.filters select,
.filters input {
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 8px;
  font-size: 14px;
}
.cards {
  display: grid;
  gap: 16px;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
}
.card {
  background: #fff;
  border-radius: 18px;
  border: 1px solid var(--border);
  overflow: hidden;
  box-shadow: 0 12px 20px rgba(15, 23, 42, 0.04);
}
.card-link {
  display: flex;
  flex-direction: column;
  gap: 12px;
  text-decoration: none;
  color: inherit;
  padding: 18px;
}
.hero {
  display: flex;
  justify-content: center;
}
.avatar {
  width: 96px;
  height: 96px;
  border-radius: 50%;
  border: 4px solid #f3f4f6;
  object-fit: cover;
}
.body h3 {
  margin: 0;
  text-align: center;
}
.title {
  margin: 4px 0 0;
  text-align: center;
  color: var(--muted);
  font-size: 14px;
}
.meta,
.rating {
  margin: 2px 0;
  text-align: center;
  color: var(--muted);
  font-size: 13px;
}
.chip {
  border: 1px solid #3b82f6;
  color: #0f172a;
  background: transparent;
  border-radius: 999px;
  padding: 8px 12px;
  width: 100%;
  font-weight: 600;
  cursor: pointer;
}
.chip:hover {
  background: rgba(59, 130, 246, 0.08);
}
.empty {
  text-align: center;
  color: var(--muted);
}
.empty.error {
  color: #ef4444;
}
</style>
