"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Users, CreditCard, Bell, LogOut, TrendingUp, Calendar, DollarSign, Activity } from "lucide-react"
import { useRouter } from "next/navigation"
import Link from "next/link"
import { getApiUrl } from "@/lib/utils"
import { useAdminAuth } from "../AdminAuthContext"
import { useApiDiff } from "../../../tools/schema-diff/useApiDiff"
import { z } from "zod"

// 定义和后端实际返回一致的 schema
const adminStatisticsSchema = z.object({
  user_count: z.number(),
  membership_count: z.number(),
  card_code_used_count: z.number(),
});

function AdminDashboardInner() {
  const [stats, setStats] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const router = useRouter()
  const { adminToken, logout } = useAdminAuth()

  useApiDiff(adminStatisticsSchema, stats, "/api/admin/statistics");

  useEffect(() => {
    if (!adminToken) {
      router.push("/admin")
      return
    }
    fetchStatistics()
    // eslint-disable-next-line
  }, [adminToken])

  const fetchStatistics = async () => {
    try {
      if (!adminToken) {
        router.push("/admin")
        return
      }
      const response = await fetch(getApiUrl("/api/admin/statistics"), {
        headers: { Authorization: `Bearer ${adminToken}` },
      })
      if (response.ok) {
        const data = await response.json()
        setStats(data.data) // 只存data字段内容
      } else {
        router.push("/admin")
      }
    } catch (error) {
      console.error("获取统计数据失败:", error)
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    logout()
    router.push("/admin")
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-slate-600 mx-auto"></div>
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
              <div className="w-8 h-8 bg-gradient-to-r from-slate-600 to-slate-800 rounded-lg"></div>
              <h1 className="text-xl font-semibold text-gray-900">管理后台</h1>
            </div>
            <div className="flex items-center space-x-4">
              <Button variant="ghost" size="sm" onClick={handleLogout}>
                <LogOut className="h-4 w-4 mr-2" />
                退出登录
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* 统计卡片 */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card className="border-0 shadow-lg">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">用户总数</CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats?.user_count || 0}</div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-lg">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">会员总数</CardTitle>
              <TrendingUp className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats?.membership_count || 0}</div>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-lg">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">卡密使用数</CardTitle>
              <CreditCard className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats?.card_code_used_count || 0}</div>
            </CardContent>
          </Card>
        </div>

        {/* 管理功能 */}
        <Tabs defaultValue="overview" className="space-y-4">
          <TabsList>
            <TabsTrigger value="overview">概览</TabsTrigger>
            <TabsTrigger value="cards">卡密管理</TabsTrigger>
            <TabsTrigger value="members">会员管理</TabsTrigger>
            <TabsTrigger value="notifications">通知管理</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-4">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card className="border-0 shadow-lg">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Activity className="h-5 w-5" />
                    系统状态
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm">服务器状态</span>
                    <Badge className="bg-green-100 text-green-800">正常</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm">数据库连接</span>
                    <Badge className="bg-green-100 text-green-800">正常</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm">API响应时间</span>
                    <Badge className="bg-blue-100 text-blue-800">125ms</Badge>
                  </div>
                </CardContent>
              </Card>

              <Card className="border-0 shadow-lg">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Calendar className="h-5 w-5" />
                    最近活动
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3 text-sm">
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                      <span>新用户注册: user@example.com</span>
                      <span className="text-gray-500 ml-auto">2分钟前</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                      <span>卡密兑换成功: ABCD1234</span>
                      <span className="text-gray-500 ml-auto">5分钟前</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-2 h-2 bg-yellow-500 rounded-full"></div>
                      <span>会员即将到期提醒已发送</span>
                      <span className="text-gray-500 ml-auto">10分钟前</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="cards">
            <Card className="border-0 shadow-lg">
              <CardHeader>
                <CardTitle>卡密管理</CardTitle>
                <CardDescription>生成、查看和管理卡密</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <Link href="/admin/cards">
                    <Button className="w-full justify-start">
                      <CreditCard className="h-4 w-4 mr-2" />
                      进入卡密管理
                    </Button>
                  </Link>
                  <p className="text-sm text-gray-600">
                    在卡密管理页面，您可以批量生成卡密、查看使用记录、管理卡密状态等。
                  </p>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="members">
            <Card className="border-0 shadow-lg">
              <CardHeader>
                <CardTitle>会员管理</CardTitle>
                <CardDescription>查看和管理用户会员信息</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <Link href="/admin/members">
                    <Button className="w-full justify-start">
                      <Users className="h-4 w-4 mr-2" />
                      进入会员管理
                    </Button>
                  </Link>
                  <p className="text-sm text-gray-600">
                    在会员管理页面，您可以查看所有用户的会员状态、手动续费、调整会员权限等。
                  </p>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="notifications">
            <Card className="border-0 shadow-lg">
              <CardHeader>
                <CardTitle>通知管理</CardTitle>
                <CardDescription>发送和管理系统通知</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <Link href="/admin/notifications">
                    <Button className="w-full justify-start">
                      <Bell className="h-4 w-4 mr-2" />
                      进入通知管理
                    </Button>
                  </Link>
                  <p className="text-sm text-gray-600">
                    在通知管理页面，您可以向用户发送系统通知、查看通知历史、管理通知模板等。
                  </p>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}

export default AdminDashboardInner
