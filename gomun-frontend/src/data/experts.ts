export type Expert = {
  id: number
  name: string
  title: string
  region: string
  rating: number
  keywords: string[]
  avatar?: string
  years?: number
  focus?: string
  availability?: string
  responseTime?: string
  email?: string
  phone?: string
  website?: string
}

export const experts: Expert[] = [
  {
    id: 1,
    name: '김한울',
    title: '전략 컨설턴트',
    region: '서울',
    rating: 4.9,
    keywords: ['경영', '전략', '조직개편'],
    avatar: '/images/av1.svg',
    years: 22,
    focus: '대기업 HQ 전략실 및 중견기업 중장기 PMO',
    availability: '즉시 투입',
    responseTime: '평균 4시간',
    email: 'hanul@gomun.kr',
    phone: '010-1234-5678',
    website: 'https://gomun.kr',
  },
  {
    id: 2,
    name: '박도윤',
    title: '재무·회계 책임',
    region: '경기',
    rating: 4.7,
    keywords: ['재무', '회계', 'IR'],
    avatar: '/images/av2.svg',
    years: 25,
    focus: 'IPO/IFRS 고도화 & 라운드별 재무 전략',
    availability: '48시간 이내',
    responseTime: '평균 3시간',
    email: 'doyun@gomun.kr',
    phone: '010-2345-6789',
    website: 'https://finance.gomun.kr',
  },
  {
    id: 3,
    name: '이서준',
    title: '프로세스 혁신 PM',
    region: '인천',
    rating: 4.5,
    keywords: ['PM', '프로세스', '운영'],
    avatar: '/images/av3.svg',
    years: 18,
    focus: '유통/CS 운영 표준화 및 옴니채널 구축',
    availability: '1주 이내',
    responseTime: '평균 6시간',
    email: 'seojoon@gomun.kr',
    phone: '010-3456-7890',
    website: 'https://ops.gomun.kr',
  },
  {
    id: 4,
    name: '최가람',
    title: '글로벌 전략 고문',
    region: '서울',
    rating: 4.8,
    keywords: ['전략', 'IR', '컴플라이언스'],
    avatar: '/images/av4.svg',
    years: 24,
    focus: 'Cross-border JV·미국 법인 전략 자문',
    availability: '48시간 이내',
    responseTime: '평균 5시간',
    email: 'garam@gomun.kr',
    phone: '010-9876-5432',
    website: 'https://global.gomun.kr',
  },
  {
    id: 5,
    name: '윤서진',
    title: 'HR 트랜스포메이션 리드',
    region: '대전',
    rating: 4.6,
    keywords: ['HR', '조직개편', '성과분석'],
    avatar: '/images/av5.svg',
    years: 17,
    focus: '4.5일제 정착, OKR 리빌드, 리더십 코칭',
    availability: '즉시 투입',
    responseTime: '평균 2시간',
    email: 'seojin@gomun.kr',
    phone: '010-7654-3210',
    website: 'https://people.gomun.kr',
  },
]

const emailToId = new Map<string, number>()
experts.forEach((ex) => {
  if (ex.email) emailToId.set(ex.email, ex.id)
})

let nextExpertId = Math.max(...experts.map((ex) => ex.id)) + 1

export function registerDynamicExpert(data: Omit<Expert, 'id'>): Expert {
  if (data.email && emailToId.has(data.email)) {
    const target = experts.find((ex) => ex.email === data.email)
    if (target) {
      Object.assign(target, data)
      return target
    }
  }
  const expert: Expert = {
    id: nextExpertId++,
    ...data,
  }
  experts.push(expert)
  if (expert.email) emailToId.set(expert.email, expert.id)
  return expert
}
