"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Crown, Calendar, HardDrive, Bell, User, CreditCard, LogOut } from "lucide-react"
import { useRouter } from "next/navigation"
import Link from "next/link"
import { getApiUrl } from "@/lib/utils"
import { useUserStore } from "../store/userStore"
import { useApiDiff } from "../../tools/schema-diff/useApiDiff"
import { z } from "zod"

interface MembershipInfo {
  local: {
    expire_at: string
  }
  online: {
    expire_at: string
    storage_total: number
  }
}

// 定义zod schema（可根据实际情况调整）
const membershipSchema = z.object({
  local: z.object({
    expire_at: z.string(),
  }),
  online: z.object({
    expire_at: z.string(),
    storage_total: z.number(),
  }),
});

export default function Dashboard() {
  const [membership, setMembership] = useState<MembershipInfo | null>(null)
  const [loading, setLoading] = useState(true)
  const router = useRouter()
  const { token, logout } = useUserStore()

  useEffect(() => {
    if (!token) {
      router.push("/")
      return
    }
    fetchMembership()
    // eslint-disable-next-line
  }, [token])

  const fetchMembership = async () => {
    try {
      if (!token) {
        router.push("/")
        return
      }
      const response = await fetch(getApiUrl("/api/membership"), {
        headers: { Authorization: `Bearer ${token}` },
      })
      if (response.ok) {
        const data = await response.json()
        setMembership(data.data)
      } else {
        router.push("/")
      }
    } catch (error) {
      console.error("获取会员信息失败:", error)
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    logout()
    router.push("/")
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("zh-CN")
  }

  const isExpired = (dateString: string) => {
    return new Date(dateString) < new Date()
  }

  useApiDiff(membershipSchema, membership, "/api/membership");

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
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-4">
              <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-lg"></div>
              <h1 className="text-xl font-semibold text-gray-900">会员中心</h1>
            </div>
            <div className="flex items-center space-x-4">
              <Link href="/notifications">
                <Button variant="ghost" size="sm">
                  <Bell className="h-4 w-4" />
                </Button>
              </Link>
              <Link href="/profile">
                <Button variant="ghost" size="sm">
                  <User className="h-4 w-4" />
                </Button>
              </Link>
              <Button variant="ghost" size="sm" onClick={handleLogout}>
                <LogOut className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* 本地会员卡片 */}
          <Card className="border-0 shadow-lg">
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <CardTitle className="text-lg flex items-center gap-2">
                  <Crown className="h-5 w-5 text-yellow-500" />
                  本地会员
                </CardTitle>
                <Badge variant={isExpired(membership?.local?.expire_at || "") ? "destructive" : "default"}>
                  {isExpired(membership?.local?.expire_at || "") ? "已过期" : "有效"}
                </Badge>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex items-center gap-2 text-sm text-gray-600">
                  <Calendar className="h-4 w-4" />
                  到期时间: {formatDate(membership?.local?.expire_at || "")}
                </div>
                <div className="text-xs text-gray-500">本地会员可享受离线功能和本地存储服务</div>
              </div>
            </CardContent>
          </Card>

          {/* 在线会员卡片 */}
          <Card className="border-0 shadow-lg">
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <CardTitle className="text-lg flex items-center gap-2">
                  <Crown className="h-5 w-5 text-blue-500" />
                  在线会员
                </CardTitle>
                <Badge variant={isExpired(membership?.online?.expire_at || "") ? "destructive" : "default"}>
                  {isExpired(membership?.online?.expire_at || "") ? "已过期" : "有效"}
                </Badge>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex items-center gap-2 text-sm text-gray-600">
                  <Calendar className="h-4 w-4" />
                  到期时间: {formatDate(membership?.online?.expire_at || "")}
                </div>
                <div className="flex items-center gap-2 text-sm text-gray-600">
                  <HardDrive className="h-4 w-4" />
                  存储空间: {membership?.online?.storage_total || 0} GB
                </div>
                <Progress value={65} className="h-2" />
                <div className="text-xs text-gray-500">在线会员可享受云端同步和扩展存储</div>
              </div>
            </CardContent>
          </Card>

          {/* 快捷操作卡片 */}
          <Card className="border-0 shadow-lg">
            <CardHeader className="pb-3">
              <CardTitle className="text-lg">快捷操作</CardTitle>
              <CardDescription>管理您的账户和会员服务</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <Link href="/redeem" className="block">
                  <Button className="w-full justify-start" variant="outline">
                    <CreditCard className="h-4 w-4 mr-2" />
                    卡密充值
                  </Button>
                </Link>
                <Link href="/profile" className="block">
                  <Button className="w-full justify-start" variant="outline">
                    <User className="h-4 w-4 mr-2" />
                    个人信息
                  </Button>
                </Link>
                <Link href="/notifications" className="block">
                  <Button className="w-full justify-start" variant="outline">
                    <Bell className="h-4 w-4 mr-2" />
                    系统通知
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* 会员特权说明 */}
        <Card className="mt-8 border-0 shadow-lg">
          <CardHeader>
            <CardTitle>会员特权</CardTitle>
            <CardDescription>了解不同会员等级的专属权益</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-3">
                <h4 className="font-medium text-yellow-600 flex items-center gap-2">
                  <Crown className="h-4 w-4" />
                  本地会员特权
                </h4>
                <ul className="space-y-1 text-sm text-gray-600">
                  <li>• 离线功能使用权限</li>
                  <li>• 本地数据存储</li>
                  <li>• 基础功能无限制使用</li>
                  <li>• 优先技术支持</li>
                </ul>
              </div>
              <div className="space-y-3">
                <h4 className="font-medium text-blue-600 flex items-center gap-2">
                  <Crown className="h-4 w-4" />
                  在线会员特权
                </h4>
                <ul className="space-y-1 text-sm text-gray-600">
                  <li>• 云端数据同步</li>
                  <li>• 扩展存储空间</li>
                  <li>• 多设备数据共享</li>
                  <li>• 高级功能解锁</li>
                  <li>• 24/7 专属客服</li>
                </ul>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
