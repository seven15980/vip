"use client"

import React, { createContext, useContext, useState, useEffect, ReactNode } from "react"

interface AdminAuthContextType {
  adminToken: string | null
  login: (token: string) => void
  logout: () => void
}

const AdminAuthContext = createContext<AdminAuthContextType | undefined>(undefined)

export const AdminAuthProvider = ({ children }: { children: ReactNode }) => {
  const [adminToken, setAdminToken] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem("adminToken")
    setAdminToken(token)
    setIsLoading(false)
  }, [])

  const login = (token: string) => {
    setAdminToken(token)
    localStorage.setItem("adminToken", token)
  }

  const logout = () => {
    setAdminToken(null)
    localStorage.removeItem("adminToken")
  }

  if (isLoading) {
    return null // 或可返回 loading 组件
  }

  return (
    <AdminAuthContext.Provider value={{ adminToken, login, logout }}>
      {children}
    </AdminAuthContext.Provider>
  )
}

export const useAdminAuth = () => {
  const context = useContext(AdminAuthContext)
  if (!context) {
    throw new Error("useAdminAuth 必须在 AdminAuthProvider 内使用")
  }
  return context
} 