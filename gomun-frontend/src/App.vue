<script setup lang="ts">
import { ref } from 'vue'
import MenuToggle from './components/MenuToggle.vue'
import SideNav from './components/SideNav.vue'

const sideOpen = ref(false)
const showAbout = ref(false)
</script>

<template>
  <div class="app">
    <header class="app__header">
      <div class="app__brand">
        <img src="/vite.svg" alt="logo" class="brand__logo" />
        <h1 class="brand__title">GOMUN - Zero-Gap HR Tech</h1>
      </div>
      <div class="app__actions">
        <button class="link" @click="showAbout = true">About</button>
        <MenuToggle v-model="sideOpen" />
      </div>
    </header>

    <main class="app__main" :class="{ 'with-rail': sideOpen }">
      <transition name="rail">
        <aside v-if="sideOpen" class="rail" @click.self="sideOpen=false">
          <SideNav :selectedIndex="0" />
        </aside>
      </transition>

      <section class="app__content">
        <!-- Keep the previously designed Home content -->
        <section class="hero">
          <div class="hero-bg" aria-hidden="true">
            <svg class="bg-svg" viewBox="0 0 1425 1119" xmlns="http://www.w3.org/2000/svg"><radialGradient id="gomun-a" cx="712.5" cy="559.5" gradientUnits="userSpaceOnUse" r="640.5843"><stop offset="0" stop-color="#d7ff96"/><stop offset=".27" stop-color="#d5fe93"/><stop offset=".4613" stop-color="#d1fc8a"/><stop offset=".6276" stop-color="#c8f87a"/><stop offset=".7799" stop-color="#bcf264"/><stop offset=".9212" stop-color="#adeb48"/><stop offset="1" stop-color="#a3e635"/></radialGradient><path d="m76.6 98c102.5-76.8 532.4-197 253.5 48.8s251.7 32.8 343.7 81.6-69.5 382.7-226.3 342.4-204.7-249.6-340-143.6-139.9-247.6-30.9-329.2zm983.4 868.8c118.6-107.8 166.1-217.7 314.9-310.3 148.8-92.7-73.3-140.1-155.3-60.3-82 79.7-166.8-10.9-256.6 142.2-73.3 125-21.6 336.2 97 228.4zm-899.1-142.6c23.1-38.3 225.3 16.2 235.8 91.7 6.7 48.7-69.5 82.1-57.6 136.3 10.2 46.4 77.6 73.3 83.8 65.5 14.7-18.2-293.7-241-262-293.5z" fill="url(#gomun-a)"/></svg>
          </div>
          <div class="hero-w hero-grid">
            <div class="hero-col">
              <span class="badge">긴급 매칭</span>
              <h2 class="hero__title">하이-스킬 공백, 0으로</h2>
              <p class="hero__subtitle">기업의 단기 숙련 인력 공백을 신속히 메우는 Zero‑Gap HR Tech 플랫폼</p>
              <div class="hero__actions">
                <button class="btn btn--primary">기업 대시보드 열기</button>
                <button class="btn">전문가 대시보드</button>
              </div>
              <ul class="stats">
                <li><strong>8000+</strong><span>누적 수행</span></li>
                <li><strong>3000+</strong><span>등록 전문가</span></li>
                <li><strong>50K+</strong><span>매칭 요청</span></li>
                <li><strong>80+</strong><span>카테고리</span></li>
              </ul>
            </div>
            <div class="hero-col">
              <div class="pgrid">
                <div class="tile" style="background-image:url('https://images.unsplash.com/photo-1470770903676-69b98201ea1c?q=80&w=600&auto=format&fit=crop');"></div>
                <div class="tile" style="background-image:url('https://images.unsplash.com/photo-1501785888041-af3ef285b470?q=80&w=600&auto=format&fit=crop');"></div>
                <div class="tile" style="background-image:url('https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=600&auto=format&fit=crop');"></div>
                <div class="tile" style="background-image:url('https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?q=80&w=600&auto=format&fit=crop');"></div>
                <div class="tile" style="background-image:url('https://images.unsplash.com/photo-1469474968028-56623f02e42e?q=80&w=600&auto=format&fit=crop');"></div>
                <div class="tile" style="background-image:url('https://images.unsplash.com/photo-1519681393784-d120267933ba?q=80&w=600&auto=format&fit=crop');"></div>
                <div class="tile" style="background-image:url('https://images.unsplash.com/photo-1441974231531-c6227db76b6e?q=80&w=600&auto=format&fit=crop');"></div>
                <div class="tile" style="background-image:url('https://images.unsplash.com/photo-1491553895911-0055eca6402d?q=80&w=600&auto=format&fit=crop');"></div>
                <div class="tile" style="background-image:url('https://images.unsplash.com/photo-1441974231531-c6227db76b6e?q=80&w=600&auto=format&fit=crop');"></div>
              </div>
              <p class="credit"><span>Picture by</span> <a href="https://unsplash.com" target="_blank" rel="noopener">Unsplash Authors</a></p>
            </div>
          </div>
        </section>

        <section class="catalog">
          <h3 class="catalog__title">카테고리</h3>
          <div class="catalog__grid">
            <article class="ccard"><header>경영/전략</header><p>신사업·조직개편·PMO</p><button class="linkBtn">더 알아보기</button></article>
            <article class="ccard"><header>회계/재무</header><p>세무·IPO·IR</p><button class="linkBtn">더 알아보기</button></article>
            <article class="ccard"><header>사무/행정</header><p>즉시 대체·운영 안정화</p><button class="linkBtn">더 알아보기</button></article>
          </div>
        </section>

        <section class="grid2">
          <div class="grid2__col">
            <article class="block">
              <header class="block__header">최근 요청</header>
              <ul class="list">
                <li>
                  <span class="list__title">재무/세무 긴급 검토(3일)</span>
                  <span class="list__meta">서울 · 2시간 전</span>
                </li>
                <li>
                  <span class="list__title">IPO 준비 회계 자문(2주)</span>
                  <span class="list__meta">경기 · 어제</span>
                </li>
                <li>
                  <span class="list__title">PMO 투입(1개월)</span>
                  <span class="list__meta">인천 · 2일 전</span>
                </li>
              </ul>
            </article>

            <article class="block">
              <header class="block__header">추천 전문가</header>
              <ul class="elist">
                <li>
                  <img src="/images/av1.svg" alt="" />
                  <div class="einfo"><strong>김하늘</strong><span>전략 컨설턴트 · 서울</span></div>
                  <span class="erating">4.8</span>
                </li>
                <li>
                  <img src="/images/av2.svg" alt="" />
                  <div class="einfo"><strong>박지우</strong><span>재무/세무 · 경기</span></div>
                  <span class="erating">4.5</span>
                </li>
              </ul>
            </article>
          </div>
          <div class="grid2__col">
            <article class="block">
              <header class="block__header">인사이트</header>
              <ul class="list">
                <li>
                  <span class="list__title"><a href="#" class="alink">긴급 투입 프리미엄, 어떻게 책정할까?</a></span>
                  <span class="list__meta">Price · 5분 읽기</span>
                </li>
                <li>
                  <span class="list__title"><a href="#" class="alink">중소기업 PMO 투입시 체크리스트</a></span>
                  <span class="list__meta">Operations · 6분 읽기</span>
                </li>
              </ul>
            </article>
          </div>
        </section>
      </section>

      <transition name="modal">
        <section v-if="showAbout" class="modal" @click="showAbout = false">
          <article class="modal__content" @click.stop>
            <h3 class="modal__title">GOMUN Prototype</h3>
            <p class="modal__text">하이-스킬 긱이코노미 기반의 Zero‑Gap HR Tech. 매칭/계약/정산 자동화와 품질 보증을 지향합니다.</p>
            <button class="modal__close" @click="showAbout = false">닫기</button>
          </article>
        </section>
      </transition>
    </main>
  </div>
</template>

<style scoped>
.app { --header-h: 56px }
.app__header {
  position: sticky; top: 0; height: var(--header-h);
  background: rgba(255,255,255,.82); border-bottom: 1px solid var(--border);
  -webkit-backdrop-filter: saturate(180%) blur(8px); backdrop-filter: saturate(180%) blur(8px);
  display:flex; align-items:center; justify-content:space-between; padding: 12px 20px; gap: 12px;
}
.app__brand { display:flex; align-items:center; gap:12px }
.brand__logo { width:28px; height:28px }
.brand__title { font-size:15px; font-weight:800; margin:0 }
.app__actions { display:flex; align-items:center; gap:12px }
.link { border:0; background:transparent; color:#667085; cursor:pointer }
.link:hover { color:#0f172a }

.app__main { position: relative; padding: 20px }
.app__content { background: transparent; padding: 0 }

.app__main.with-rail { padding-right: 340px }
.rail { position: fixed; top: var(--header-h); right: 0; bottom: 0; width: 320px; background: var(--surface); border-left:1px solid var(--border); box-shadow: 0 6px 30px rgba(15,23,42,.06) }
.rail-enter-active, .rail-leave-active { transition: transform .22s ease, opacity .22s ease }
.rail-enter-from, .rail-leave-to { transform: translateY(-8px); opacity: 0 }

/* Hero + sections styles */
.hero { text-align: center; padding: 36px 16px 20px }
.hero-w { position: relative; max-width: 1200px; margin: 0 auto; background: #fff; border: 1px solid var(--border); border-radius: 20px; padding: 36px; box-shadow: 0 12px 32px rgba(0,0,0,.04) }
.hero-bg { position: absolute; inset: 0; overflow: hidden; filter: blur(40px); opacity: .35; pointer-events: none; z-index: 0 }
.bg-svg { position: absolute; width: 130%; height: 130%; left: 50%; top: 50%; transform: translate(-50%, -50%) scale(1.2) }
.hero-grid { display: grid; grid-template-columns: 1.2fr 1fr; gap: 20px; align-items: center }
.hero-cover { display:flex; align-items:center; justify-content:center }
.badge { display:inline-block; padding: 6px 10px; background:#a3e635; color:#0a0a0a; border-radius: 8px; font-size: 12px; font-weight: 700; letter-spacing: .05em; margin-bottom: 8px }
.hero__title { font-size: clamp(24px, 2.6vw, 34px); line-height: 1.15; font-weight: 800; margin: 0 0 6px }
.hero__subtitle { color: var(--muted); margin: 0 0 16px }
.hero__actions { display:flex; gap:10px; justify-content:center; margin-bottom: 16px }
.btn { border:1px solid var(--border); background: var(--surface); color:#0f172a; padding:10px 14px; border-radius:10px; cursor:pointer; transition:.15s ease; text-decoration:none; display:inline-block }
.btn:hover { border-color:#cfd6e4 }
.btn:active { transform: translateY(1px) }
.btn--primary { background: var(--indigo, #6366f1); border-color: var(--indigo, #6366f1); color:#fff }
.stats { display:grid; grid-template-columns: repeat(4,1fr); gap: 12px; max-width: 740px; margin: 0 auto }
.stats li { background: #fff; border:1px solid var(--border); border-radius: 12px; padding: 10px 12px; display:flex; flex-direction:column; align-items:center }
.stats strong { font-size: 18px }
.stats span { color: var(--muted); font-size: 12px }
.pgrid { display:grid; grid-template-columns: repeat(3, 1fr); gap: 10px }
.tile { width: 100%; padding-top: 100%; background-size: cover; background-position: center; border-radius: 12px; border: 1px solid var(--border) }
.credit { text-align:left; color:#065f46; font-size: 12px; margin-top: 6px }
.credit span { opacity: .6 }

.catalog { margin-top: 24px }
.catalog__title { margin: 0 0 10px; font-size: 18px }
.catalog__grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 14px }
.ccard { background: #ffffff; border: 1px solid var(--border); border-radius: 14px; padding: 16px }
.ccard header { font-weight: 700; margin-bottom: 6px }
.ccard p { color: var(--muted); margin: 0 0 10px }
.linkBtn { border: 0; background: transparent; color: #2563eb; cursor: pointer }
.linkBtn:hover { text-decoration: underline }

.grid2 { display:grid; grid-template-columns: repeat(2, 1fr); gap: 16px; margin-top: 18px }
.block { background: var(--surface); border:1px solid var(--border); border-radius: 14px; padding: 14px; box-shadow: 0 6px 20px rgba(15,23,42,.04) }
.block__header { font-weight: 800; font-size: 16px; margin-bottom: 8px }
.list { display:grid; gap:10px }
.list li { display:flex; flex-direction:column; gap:2px; padding:8px; border-radius:10px }
.list li:hover { background: rgba(99,102,241,.05) }
.list__title { font-weight:700; font-size:14px }
.list__meta { font-size:12px; color: var(--muted) }
.alink { color: var(--indigo, #6366f1); text-decoration:none }
.alink:hover { text-decoration:underline }
.elist { display:grid; gap:10px }
.elist li { display:grid; grid-template-columns: 36px 1fr auto; align-items:center; gap:10px; padding:8px; border-radius:10px }
.elist li:hover { background: rgba(99,102,241,.05) }
.elist img { width:36px; height:36px; border-radius:50%; border:1px solid var(--border) }
.einfo strong { font-size:14px }
.einfo span { font-size:12px; color: var(--muted) }
.erating { font-size:12px; color:#111827; background:#eef2ff; border:1px solid #e7ecff; padding:2px 6px; border-radius:99px }
@media (max-width: 900px) { .grid2 { grid-template-columns:1fr } .hero-grid { grid-template-columns: 1fr } }
</style>
