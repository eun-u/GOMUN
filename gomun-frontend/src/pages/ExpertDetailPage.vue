<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { experts } from '../data/experts'

const route = useRoute()
const expert = computed(() => experts.find((item) => item.id === Number(route.params.id)))
const merged = expert
</script>

<template>
  <section class="detail" v-if="merged">
    <RouterLink to="/experts" class="back">← 전문가 목록으로</RouterLink>
    <header class="hero">
      <img :src="expert?.avatar" :alt="expert?.name" />
      <div>
        <h1>{{ merged.name }}</h1>
        <p>{{ merged.title }}</p>
        <p class="meta">{{ merged.region }} · {{ merged.availability }} · 응답 {{ merged.responseTime }}</p>
      </div>
    </header>
    <article class="summary">
      <h2>핵심 포커스</h2>
      <p>{{ merged.focus }}</p>
      <ul>
        <li v-for="tag in expert?.keywords" :key="tag">#{{ tag }}</li>
      </ul>
      <div class="actions">
        <button class="primary">Send 요청 보내기</button>
      </div>
    </article>
    <article class="contact">
      <h3>Contact</h3>
      <ul>
        <li><span>Email</span><strong>{{ expert?.email }}</strong></li>
        <li><span>Phone</span><strong>{{ merged.phone }}</strong></li>
        <li><span>Website</span><strong>{{ merged.website }}</strong></li>
      </ul>
    </article>
  </section>
  <section class="detail" v-else>
    <p>전문가를 찾을 수 없습니다.</p>
    <RouterLink to="/experts" class="back">목록으로</RouterLink>
  </section>
</template>

<style scoped>
.detail {
  background: #fff;
  border: 1px solid var(--border);
  border-radius: 24px;
  padding: 28px;
  box-shadow: 0 16px 40px rgba(15, 23, 42, 0.08);
}
.back {
  text-decoration: none;
  color: #2563eb;
  display: inline-block;
  margin-bottom: 10px;
}
.hero {
  display: flex;
  gap: 18px;
  align-items: center;
}
.hero img {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  border: 4px solid #f3f4f6;
  object-fit: cover;
}
.meta {
  color: var(--muted);
}
.summary {
  margin-top: 20px;
}
.summary ul {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  list-style: none;
  padding: 0;
}
.summary li {
  background: rgba(15, 23, 42, 0.06);
  border-radius: 999px;
  padding: 4px 10px;
  font-size: 12px;
}
.error {
  color: #ef4444;
  margin-top: 12px;
}
.actions {
  margin-top: 18px;
}
.primary {
  border: 0;
  background: linear-gradient(120deg, #a3e635, #10b981);
  color: #0f172a;
  font-weight: 700;
  border-radius: 999px;
  padding: 12px 20px;
  font-size: 14px;
  cursor: pointer;
  box-shadow: 0 12px 28px rgba(16, 185, 129, 0.35);
}
.contact {
  margin-top: 24px;
  border-top: 1px solid var(--border);
  padding-top: 16px;
}
.contact ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 8px;
}
.contact li {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
}
.contact span {
  color: var(--muted);
}
</style>
