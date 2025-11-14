import type { Role } from '../services/auth'

export type NotificationAudience = Role | 'guest'

export type NotificationItem = {
  id: string
  title: string
  message: string
  time?: string
  createdAt?: string
  read?: boolean
  tag?: string
  actionLabel?: string
  actionRoute?: string
  from?: string
}

type NotificationSeed = Record<NotificationAudience, NotificationItem[]>

export const notificationSeed: NotificationSeed = {
  guest: [
    {
      id: 'guest-1',
      title: 'GOMUN을 둘러보세요',
      message: '로그인하면 전문가 매칭, 요청 진행 현황 등 더 많은 정보를 확인할 수 있어요.',
      time: '방금 전',
      tag: '시작하기',
      actionLabel: '로그인하기',
      actionRoute: '/',
    },
    {
      id: 'guest-2',
      title: 'Zero-Gap 매칭 소개',
      message: '기업 공백을 메워드리는 긴급 투입 프로세스를 확인해 보세요.',
      time: '1시간 전',
      tag: '소개',
    },
  ],
  expert: [],
  company: [],
}

export function cloneNotificationSeed(): NotificationSeed {
  return JSON.parse(JSON.stringify(notificationSeed))
}
