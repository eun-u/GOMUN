<script setup lang="ts">
import type { NotificationItem } from '../data/notifications'

defineProps<{ items: NotificationItem[]; roleLabel: string; unread: number; error?: string; loading?: boolean }>()
const emit = defineEmits<{ close: []; mark: []; openAction: [item: NotificationItem] }>()

function handleAction(item: NotificationItem) {
  emit('openAction', item)
}
</script>

<template>
  <section class="notif" role="dialog" aria-label="알림" aria-modal="false">
    <header class="notif__header">
      <div>
        <strong>{{ roleLabel }} 알림</strong>
        <span v-if="unread" class="notif__unread">{{ unread }}개의 새 소식</span>
      </div>
      <div class="notif__actions">
        <button class="ghost" @click="$emit('mark')">모두 읽음 처리</button>
        <button class="ghost" @click="$emit('close')">닫기</button>
      </div>
    </header>
    <ul class="notif__list">
      <li v-for="item in items" :key="item.id" :class="['notif__item', { read: item.read }]">
        <div class="notif__tag" v-if="item.tag">{{ item.tag }}</div>
        <div class="notif__body">
          <strong>{{ item.title }}</strong>
          <p>{{ item.message }}</p>
          <div class="notif__meta">
            <span class="notif__from" v-if="item.from">{{ item.from }}</span>
            <small>{{ item.time }}</small>
          </div>
        </div>
        <button v-if="item.actionLabel" class="notif__btn" @click="handleAction(item)">
          {{ item.actionLabel }}
        </button>
      </li>
    </ul>
    <p class="notif__status" v-if="loading">알림을 불러오는 중...</p>
    <p class="notif__status error" v-else-if="error">{{ error }}</p>
    <p v-else-if="!items.length" class="notif__empty">새로운 알림이 없습니다.</p>
  </section>
</template>

<style scoped>
.notif {
  position: absolute;
  top: 60px;
  right: 20px;
  width: min(360px, calc(100vw - 32px));
  background: var(--surface, #fff);
  border: 1px solid var(--border);
  border-radius: 16px;
  box-shadow: 0 24px 50px rgba(15, 23, 42, 0.15);
  padding: 14px;
  z-index: 30;
}
.notif__header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 8px;
}
.notif__header strong {
  font-size: 15px;
}
.notif__unread {
  display: block;
  color: #16a34a;
  font-size: 12px;
}
.notif__actions {
  display: flex;
  gap: 6px;
}
.ghost {
  border: 0;
  background: transparent;
  font-size: 12px;
  color: #475467;
  cursor: pointer;
}
.ghost:hover {
  color: #111827;
}
.notif__list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 320px;
  overflow: auto;
}
.notif__item {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 10px;
  padding: 10px;
  border-radius: 12px;
  background: rgba(99, 102, 241, 0.06);
}
.notif__item.read {
  opacity: 0.65;
  background: var(--surface);
  border: 1px solid var(--border);
}
.notif__tag {
  font-size: 10px;
  font-weight: 700;
  color: #6366f1;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding-top: 4px;
}
.notif__body strong {
  display: block;
  margin-bottom: 4px;
}
.notif__body p {
  margin: 0;
  font-size: 13px;
  color: #475467;
}
.notif__meta {
  display: flex;
  gap: 6px;
  align-items: center;
  color: #94a3b8;
  font-size: 11px;
}
.notif__from {
  font-weight: 600;
  color: #475467;
}
.notif__status {
  text-align: center;
  font-size: 12px;
  color: var(--muted);
  margin: 10px 0 0;
}
.notif__status.error {
  color: #ef4444;
}
.notif__btn {
  align-self: center;
  border: 0;
  background: rgba(16, 185, 129, 0.15);
  color: #047857;
  padding: 6px 10px;
  border-radius: 999px;
  font-size: 12px;
  cursor: pointer;
}
.notif__btn:hover {
  background: rgba(16, 185, 129, 0.3);
}
.notif__empty {
  text-align: center;
  font-size: 13px;
  color: var(--muted);
  margin: 8px 0 0;
}
</style>
