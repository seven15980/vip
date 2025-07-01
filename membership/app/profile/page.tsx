"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { ArrowLeft, User, Mail, Lock, Eye, EyeOff, CheckCircle } from "lucide-react"
import Link from "next/link"
import { getApiUrl } from "@/lib/utils"
import { useUserStore } from "../store/userStore"
import { zodSchemaToTree } from "../../tools/schema-diff/zod2tree";
import { jsonToTree } from "../../tools/schema-diff/json2tree";
import { compareTrees } from "../../tools/schema-diff/compare";
import { z } from "zod";

interface UserProfile {
  email: string
  created_at: string
  last_login: string
}

// 定义zod schema（可根据实际情况调整）
const userProfileSchema = z.object({
  email: z.string(),
  created_at: z.string(),
  last_login: z.string(),
});

export default function ProfilePage() {
  const [profile, setProfile] = useState<UserProfile | null>(null)
  const [loading, setLoading] = useState(true)
  const [isChangingPassword, setIsChangingPassword] = useState(false)
  const [showPassword, setShowPassword] = useState(false)
  const [passwordData, setPasswordData] = useState({
    currentPassword: "",
    newPassword: "",
    confirmPassword: "",
  })
  const [result, setResult] = useState<{ success: boolean; message: string } | null>(null)
  const router = require('next/navigation').useRouter();
  const { token } = useUserStore()

  useEffect(() => {
    if (!token) {
      router.push("/")
      return
    }
    fetchProfile()
    // eslint-disable-next-line
  }, [token])

  const fetchProfile = async () => {
    try {
      if (!token) {
        router.push("/")
        return
      }
      const response = await fetch(getApiUrl("/api/profile"), {
        headers: { Authorization: `Bearer ${token}` },
      })
      if (response.ok) {
        const result = await response.json()
        setProfile(result.data)
        // 自动diff
        try {
          userProfileSchema.parse(result.data)
        } catch (e) {
          console.error("zod校验失败:", e)
        }
        const expectedTree = zodSchemaToTree(userProfileSchema)
        const actualTree = jsonToTree(result.data)
        const diffs = compareTrees(expectedTree, actualTree)
        console.log("【自动化diff】/api/profile")
        console.table(diffs)
      }
    } catch (error) {
      console.error("获取个人信息失败:", error)
    } finally {
      setLoading(false)
    }
  }

  const handlePasswordChange = async (e: React.FormEvent) => {
    e.preventDefault()
    if (passwordData.newPassword !== passwordData.confirmPassword) {
      setResult({ success: false, message: "新密码确认不匹配" })
      return
    }
    if (passwordData.newPassword.length < 6) {
      setResult({ success: false, message: "新密码长度至少6位" })
      return
    }
    setIsChangingPassword(true)
    setResult(null)
    try {
      if (!token) {
        router.push("/")
        return
      }
      const response = await fetch(getApiUrl("/api/profile"), {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          currentPassword: passwordData.currentPassword,
          password: passwordData.newPassword,
        }),
      })
      if (response.ok) {
        setResult({ success: true, message: "密码修改成功" })
        setPasswordData({ currentPassword: "", newPassword: "", confirmPassword: "" })
      } else {
        const data = await response.json()
        setResult({ success: false, message: data.message || "密码修改失败" })
      }
    } catch (error) {
      setResult({ success: false, message: "网络错误，请稍后重试" })
    } finally {
      setIsChangingPassword(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">加载中...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center h-16">
            <Link href="/dashboard">
              <Button variant="ghost" size="sm" className="mr-4">
                <ArrowLeft className="h-4 w-4 mr-2" />
                返回
              </Button>
            </Link>
            <h1 className="text-xl font-semibold text-gray-900">个人信息</h1>
          </div>
        </div>
      </header>

      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
        {/* 基本信息卡片 */}
        <Card className="border-0 shadow-lg">
          <CardHeader>
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-full flex items-center justify-center">
                <User className="h-8 w-8 text-white" />
              </div>
              <div>
                <CardTitle className="text-xl">基本信息</CardTitle>
                <CardDescription>查看您的账户基本信息</CardDescription>
              </div>
            </div>
          </CardHeader>

          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label className="text-sm font-medium text-gray-700">邮箱地址</Label>
                <div className="flex items-center gap-2 p-3 bg-gray-50 rounded-lg">
                  <Mail className="h-4 w-4 text-gray-500" />
                  <span className="text-sm">{profile?.email}</span>
                </div>
              </div>

              <div className="space-y-2">
                <Label className="text-sm font-medium text-gray-700">注册时间</Label>
                <div className="p-3 bg-gray-50 rounded-lg">
                  <span className="text-sm">
                    {profile?.created_at ? new Date(profile.created_at).toLocaleDateString("zh-CN") : "-"}
                  </span>
                </div>
              </div>

              <div className="space-y-2 md:col-span-2">
                <Label className="text-sm font-medium text-gray-700">最后登录</Label>
                <div className="p-3 bg-gray-50 rounded-lg">
                  <span className="text-sm">
                    {profile?.last_login ? new Date(profile.last_login).toLocaleString("zh-CN") : "-"}
                  </span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* 密码修改卡片 */}
        <Card className="border-0 shadow-lg">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Lock className="h-5 w-5" />
              修改密码
            </CardTitle>
            <CardDescription>为了账户安全，建议定期更换密码</CardDescription>
          </CardHeader>

          <CardContent>
            {result && (
              <Alert className={`mb-4 ${result.success ? "border-green-200 bg-green-50" : "border-red-200 bg-red-50"}`}>
                <div className="flex items-center gap-2">
                  {result.success && <CheckCircle className="h-4 w-4 text-green-600" />}
                  <AlertDescription className={result.success ? "text-green-800" : "text-red-800"}>
                    {result.message}
                  </AlertDescription>
                </div>
              </Alert>
            )}

            <form onSubmit={handlePasswordChange} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="current-password">当前密码</Label>
                <div className="relative">
                  <Input
                    id="current-password"
                    type={showPassword ? "text" : "password"}
                    placeholder="请输入当前密码"
                    value={passwordData.currentPassword}
                    onChange={(e) => setPasswordData({ ...passwordData, currentPassword: e.target.value })}
                    required
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="new-password">新密码</Label>
                <div className="relative">
                  <Input
                    id="new-password"
                    type={showPassword ? "text" : "password"}
                    placeholder="请输入新密码（至少6位）"
                    value={passwordData.newPassword}
                    onChange={(e) => setPasswordData({ ...passwordData, newPassword: e.target.value })}
                    required
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="confirm-password">确认新密码</Label>
                <div className="relative">
                  <Input
                    id="confirm-password"
                    type={showPassword ? "text" : "password"}
                    placeholder="请再次输入新密码"
                    value={passwordData.confirmPassword}
                    onChange={(e) => setPasswordData({ ...passwordData, confirmPassword: e.target.value })}
                    required
                  />
                  <button
                    type="button"
                    className="absolute right-3 top-3 text-gray-400 hover:text-gray-600"
                    onClick={() => setShowPassword(!showPassword)}
                  >
                    {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </button>
                </div>
              </div>

              <Button type="submit" className="w-full" disabled={isChangingPassword}>
                {isChangingPassword ? "修改中..." : "修改密码"}
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* 安全提示 */}
        <Card className="border-0 shadow-lg bg-blue-50 border-blue-200">
          <CardContent className="pt-6">
            <h4 className="font-medium text-blue-900 mb-2">安全提示</h4>
            <ul className="text-sm text-blue-800 space-y-1">
              <li>• 密码长度建议8位以上，包含字母和数字</li>
              <li>• 不要使用过于简单或常见的密码</li>
              <li>• 定期更换密码，保护账户安全</li>
              <li>• 不要在公共场所或设备上登录账户</li>
            </ul>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
