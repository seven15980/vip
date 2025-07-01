import { create } from 'zustand'

interface UserInfo {
  email: string
  userId: string
  // 可根据实际需求扩展字段
}

interface UserState {
  token: string | null
  user: UserInfo | null
  login: (token: string, user: UserInfo) => void
  logout: () => void
  restore: () => void
}

export const useUserStore = create<UserState>((set: (partial: Partial<UserState>) => void) => ({
  token: typeof window !== 'undefined' ? localStorage.getItem('token') : null,
  user: typeof window !== 'undefined' ? (() => {
    const userStr = localStorage.getItem('user')
    return userStr ? JSON.parse(userStr) as UserInfo : null
  })() : null,
  login: (token: string, user: UserInfo) => {
    set({ token, user })
    localStorage.setItem('token', token)
    localStorage.setItem('user', JSON.stringify(user))
  },
  logout: () => {
    set({ token: null, user: null })
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  },
  restore: () => {
    const token = localStorage.getItem('token')
    const userStr = localStorage.getItem('user')
    set({
      token: token || null,
      user: userStr ? JSON.parse(userStr) as UserInfo : null
    })
  }
})) 