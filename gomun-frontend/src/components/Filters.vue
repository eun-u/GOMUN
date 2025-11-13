<script setup lang="ts">
import { ref, reactive, computed, onMounted, nextTick, watchEffect } from 'vue'
import type { Expert } from '../data/experts'
import { experts as seed } from '../data/experts'

const props = defineProps<{ mode: 'senior'|'company' }>()
const modeLabel = computed(() => props.mode === 'company' ? '전문가 탐색' : '프로젝트 탐색')

const all = ref<Expert[]>([])
const rating = reactive({ min: 5.0, max: 0 })
const filters = reactive<{ regions: Record<string, boolean>, categories: Record<string, boolean>, rating: number }>({ regions: {}, categories: {}, rating: 0 })
const menus = reactive({ regions: false, categories: false, rating: false })
const dropdown = reactive({ height: '0px' })
const menuEls = ref<HTMLElement[] | null>(null)

const activeMenu = computed(() => Object.keys(menus).reduce((acc, key, i) => (menus as any)[key] ? i : acc, -1))

const activeFilters = computed(() => {
  const cs = Object.keys(filters.regions).filter(c => filters.regions[c])
  const ks = Object.keys(filters.categories).filter(c => filters.categories[c])
  return { regions: cs, categories: ks, rating: (filters.rating > rating.min) ? [filters.rating] : [] }
})

const list = computed(() => {
  const { regions, categories } = activeFilters.value
  return all.value.filter(({ region, keywords, rating: r }) => {
    if (r < filters.rating) return false
    if (regions.length && !regions.includes(region)) return false
    return !categories.length || categories.every(cat => keywords.includes(cat))
  })
})

function setMenu(menu: keyof typeof menus, active: boolean) {
  ;(Object.keys(menus) as (keyof typeof menus)[]).forEach(k => menus[k] = !active && k === menu)
}

function setFilter(filter: 'regions'|'categories'|'rating', option?: string) {
  if (filter === 'regions' && option) {
    filters.regions[option] = !filters.regions[option]
  } else if (filter === 'categories' && option) {
    const current = !!filters.categories[option]
    clearFilter('categories', option, current)
  }
}

function clearFilter(filter: 'regions'|'categories'|'rating', except?: string, active?: boolean) {
  if (filter === 'rating') {
    filters.rating = rating.min
  } else {
    Object.keys(filters[filter]).forEach(opt => {
      ;(filters as any)[filter][opt] = except === opt && !active
    })
  }
}

function clearAllFilters() {
  ;(Object.keys(filters) as (keyof typeof filters)[]).forEach(key => clearFilter(key as any))
}

onMounted(async () => {
  // Seed mock data
  all.value = seed
  // initialize filter options
  all.value.forEach(({ region, keywords, rating: r }) => {
    if (!(region in filters.regions)) filters.regions[region] = false
    if (rating.max < r) rating.max = r
    if (rating.min > r || rating.min === 5.0) {
      rating.min = r
      filters.rating = r
    }
    keywords.forEach(k => { if (!(k in filters.categories)) filters.categories[k] = false })
  })
})

// watch dropdown height
watchEffect(async () => {
  await nextTick()
  const index = activeMenu.value
  const els = (menuEls.value || []) as any
  const el = els[index]
  dropdown.height = (!el ? 0 : el.clientHeight + 16) + 'px'
})
</script>

<template>
  <section class="filters-wrap">
    <small class="mode">{{ modeLabel }}</small>
    <nav class="nav">
      <menu class="nav__controls">
        <li v-for="(active, menu) in menus" :key="menu" class="nav__label"
          :class="{ 'nav__label--active': active, 'nav__label--filter': activeFilters[menu as 'regions'|'categories'|'rating'].length }"
          @click="setMenu(menu as any, (menus as any)[menu])">
          {{ menu }}
        </li>
        <li class="nav__label nav__label--clear" @click="clearAllFilters">Clear all</li>
      </menu>
    </nav>

    <transition-group name="dropdown" tag="section" class="dropdown" :style="dropdown">
      <menu v-for="(options, filter) in filters" :key="filter" class="filters" v-show="(menus as any)[filter]" ref="menuEls">
        <li v-if="filter === 'rating'" class="filters__rating">
          <output>
            <label>Minimum rating:&nbsp;</label>
            {{ Number(filters.rating).toFixed(1) }}
          </output>
          <input v-model.number="filters.rating" class="filters__range" type="range" :min="rating.min" :max="rating.max" step="0.1"/>
        </li>
        <template v-else>
          <li v-for="(active, option) in options as Record<string, boolean>" :key="option" class="filters__item" :class="{ 'filters__item--active': active }" @click="setFilter(filter as any, option as string)">
            {{ option }}
          </li>
        </template>
      </menu>
    </transition-group>

    <transition-group name="cards" tag="ul" class="cards">
      <li class="card" v-for="ex in list" :key="ex.id">
        <div class="card__info">
          <img class="avatar-img" :src="ex.avatar || '/images/avatar.svg'" alt="" />
          <h3 class="card__name">{{ ex.name }}</h3>
          <blockquote class="card__title">{{ ex.title }}</blockquote>
        </div>
        <ul class="card__details">
          <li class="card__data">
            <label class="card__label">지역</label>
            <p class="card__text" @click="clearFilter('regions', ex.region)">{{ ex.region }}</p>
          </li>
          <li class="card__data">
            <label class="card__label">Rating</label>
            <p class="card__text">{{ ex.rating.toFixed(1) }}</p>
          </li>
        </ul>
        <ul class="tags">
          <li v-for="k in ex.keywords" :key="k" class="tag" @click="setMenu('categories', false); setFilter('categories', k)">{{ k }}</li>
        </ul>
      </li>
    </transition-group>
  </section>
</template>

<style scoped>
.filters-wrap { position: relative; font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; color: #3d5358 }
.mode { display:block; margin-bottom: 6px; color:#94a3b8 }
.nav { display:flex; justify-content: space-between; align-items: center; margin: 0 0 8px; padding: 8px 0; border-bottom: 1px solid #e6e8eb }
.nav__controls { display:flex; align-items:center; gap: 8px; list-style:none; margin:0; padding:0 }
.nav__label { position:relative; text-transform: capitalize; cursor:pointer; padding: 4px 8px; border-radius: 6px }
.nav__label:hover { background:#f5f7fa }
.nav__label--active { color:#e11d48 }
.nav__label--filter { color:#06b6d4 }
.nav__label--clear { color:#f68185; opacity: 0.9 }

.dropdown { position: relative; height: 0; overflow:hidden; transition: height 350ms }
.dropdown::after { content:''; position:absolute; bottom:0; left:0; width:100%; height: 12px; background: linear-gradient(to top, #fff, rgba(255,255,255,0)) }
.dropdown-enter-active, .dropdown-leave-active { position:absolute; width:100%; transition: opacity 200ms ease-in-out }
.dropdown-enter-from, .dropdown-leave-to { opacity:0 }

.filters { display:flex; flex-wrap: wrap; align-items:flex-start; gap: 8px; padding: 8px 0 }
.filters__item { border:1px solid #c5d0d1; border-radius: 6px; padding: 4px 8px; font-size: .9rem; cursor:pointer; transition: all .2s }
.filters__item:hover { border-color: #379a93 }
.filters__item--active { color: #fff; background:#379a93; border-color:#379a93 }
.filters__rating { width: 100%; display:flex; flex-direction:column; align-items:center; gap: 8px; padding: 12px 0 }
.filters__range { width: 220px }

.cards { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 14px; list-style:none; margin: 16px 0 0; padding: 0 }
.card { background: var(--surface); border:1px solid var(--border); border-radius: 12px; display:flex; flex-direction:column; justify-content:space-between; box-shadow: 0 6px 20px rgba(15,23,42,.04) }
.card__info { text-align:center; padding: 12px }
.avatar-img { width: 56px; height: 56px; border-radius: 50%; object-fit: cover; display:block; margin: 0 auto }
.card__name { margin: 8px 0 4px; font-size: 1.05rem }
.card__title { margin: 0; color:#64748b }
.card__details { display:flex; justify-content:space-between; gap: 12px; margin-top: 8px; padding: 8px 12px; background: #f8fafc; border-top: 1px solid #e6e8eb }
.card__label { font-size: .8rem; color:#64748b }
.card__text { margin: 2px 0 0 }
.card__text:hover { text-decoration: underline; cursor: pointer }
.tags { display:flex; flex-wrap:wrap; gap: 6px; padding: 10px 12px }
.tag { font-size: .78rem; padding: 4px 8px; border-radius: 99px; background: #f4f7ff; color:#1e293b; border:1px solid #e7ecff; cursor:pointer }
.tag:hover { background:#e2e8f0 }

.cards-move { transition: all 300ms ease }
.cards-enter-active { transition: all 200ms ease }
.cards-leave-active { transition: all 150ms ease; position:absolute }
.cards-enter-from, .cards-leave-to { opacity: 0; transform: scale(.98) }
</style>
