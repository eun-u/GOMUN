<script setup lang="ts">
const props = defineProps<{ selectedIndex?: number }>()
const items = ['Home','기업 대시보드','전문가 대시보드','Popular','History']
</script>

<template>
  <nav class="sidenav">
    <ul>
      <li v-for="(label, i) in items" :key="i">
        <a href="#" :class="['btnlike', { active: (props.selectedIndex ?? 0)===i }]">
          <span>{{ label }}</span>
        </a>
      </li>
    </ul>
  </nav>
</template>

<style scoped>
.sidenav { width: 100%; max-width: 280px; background: transparent }
.sidenav ul { list-style:none; margin:0; padding:10px }
.btnlike { display:block; width:100%; height:40px; color:#0f172a; text-decoration:none; padding:10px; border-radius:10px }
.btnlike:hover { background:rgba(99,102,241,.08) }
.btnlike.active { background:rgba(99,102,241,.12); color:#3730a3 }
.btnlike span { font-size:14px; font-weight:600 }
</style>
