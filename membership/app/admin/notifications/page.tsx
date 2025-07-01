"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { ArrowLeft, Bell, Send, Plus } from "lucide-react"
import Link from "next/link"

interface NotificationForm {
  title: string
  content: string
  type: "info" | "warning" | "success"
  target: "all" | "members" | "expired"
}

const API_BASE = process.env.NEXT_PUBLIC_API_BASE

export default function AdminNotificationsPage() {
  const [form, setForm] = useState<NotificationForm>({
    title: "",
    content: "",
    type: "info",
    target: "all",
  })
  const [sending, setSending] = useState(false)
  const [historyNotifications, setHistoryNotifications] = useState<any[]>([])

  // 拉取历史通知
  const fetchHistory = async () => {
    const token = localStorage.getItem("adminToken")
    if (!token) return
    const res = await fetch(`${API_BASE}/api/admin/notifications/history`, {
      headers: { "Authorization": `Bearer ${token}` }
    })
    const data = await res.json()
    if (res.ok && Array.isArray(data.data)) {
      setHistoryNotifications(data.data)
    }
  }

  useEffect(() => {
    fetchHistory()
  }, [])

  // target映射：前端到后端
  const mapTarget = (target: string) => {
    switch (target) {
      case "all":
        return "all"
      case "members":
        return "online" // 只发给在线会员
      case "expired":
        return "local" // 只发给本地会员
      default:
        return "all"
    }
  }

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault()
    setSending(true)

    try {
      const token = localStorage.getItem("adminToken")
      if (!token) {
        alert("请先登录管理员账号")
        setSending(false)
        return
      }
      const res = await fetch(`${API_BASE}/api/admin/notifications`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify({
          title: form.title,
          content: form.content,
          type: form.type,
          target: mapTarget(form.target),
        }),
      })
      const data = await res.json()
      if (res.ok && data?.data?.user_count) {
        alert(`通知已发送给${data.data.user_count}个用户`)
        setForm({ title: "", content: "", type: "info", target: "all" })
        await fetchHistory() // 发送成功后立即刷新历史通知
      } else {
        alert(data?.msg || "发送失败")
      }
    } catch (err) {
      alert("网络错误，发送失败")
    }
    setSending(false)
  }

  const getTargetText = (target: string) => {
    switch (target) {
      case "all":
        return "所有"
      case "members":
        return "会员"
      case "expired":
        return "过期会员"
      default:
        return "未知"
    }
  }

  const getTypeBadge = (type: string) => {
    switch (type) {
      case "success":
        return <Badge className="bg-green-100 text-green-800">成功</Badge>
      case "warning":
        return <Badge className="bg-yellow-100 text-yellow-800">警告</Badge>
      default:
        return <Badge className="bg-blue-100 text-blue-800">信息</Badge>
    }
  }

  const getTargetBadge = (target: string) => {
    switch (target) {
      case "all":
        return <Badge variant="outline">所有用户</Badge>
      case "members":
        return <Badge className="bg-purple-100 text-purple-800">会员用户</Badge>
      case "expired":
        return <Badge className="bg-red-100 text-red-800">过期用户</Badge>
      default:
        return <Badge variant="outline">{target}</Badge>
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center h-16">
            <Link href="/admin/dashboard">
              <Button variant="ghost" size="sm" className="mr-4">
                <ArrowLeft className="h-4 w-4 mr-2" />
                返回
              </Button>
            </Link>
            <h1 className="text-xl font-semibold text-gray-900">通知管理</h1>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
        {/* 发送通知 */}
        <Card className="border-0 shadow-lg">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Plus className="h-5 w-5" />
              发送新通知
            </CardTitle>
            <CardDescription>向用户发送系统通知</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSend} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="title">通知标题</Label>
                  <Input
                    id="title"
                    placeholder="请输入通知标题"
                    value={form.title}
                    onChange={(e) => setForm({ ...form, title: e.target.value })}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="type">通知类型</Label>
                  <Select value={form.type} onValueChange={(value: any) => setForm({ ...form, type: value })}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="info">信息通知</SelectItem>
                      <SelectItem value="warning">警告通知</SelectItem>
                      <SelectItem value="success">成功通知</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="target">发送对象</Label>
                <Select value={form.target} onValueChange={(value: any) => setForm({ ...form, target: value })}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">所有用户</SelectItem>
                    <SelectItem value="members">会员用户</SelectItem>
                    <SelectItem value="expired">过期会员用户</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="content">通知内容</Label>
                <Textarea
                  id="content"
                  placeholder="请输入通知内容..."
                  rows={4}
                  value={form.content}
                  onChange={(e) => setForm({ ...form, content: e.target.value })}
                  required
                />
              </div>

              <Button type="submit" disabled={sending} className="w-full">
                <Send className="h-4 w-4 mr-2" />
                {sending ? "发送中..." : "发送通知"}
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* 历史通知 */}
        <Card className="border-0 shadow-lg">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Bell className="h-5 w-5" />
              历史通知
            </CardTitle>
            <CardDescription>查看已发送的通知记录</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="rounded-md border">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>标题</TableHead>
                    <TableHead>类型</TableHead>
                    <TableHead>发送对象</TableHead>
                    <TableHead>发送数量</TableHead>
                    <TableHead>发送时间</TableHead>
                    <TableHead>状态</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {historyNotifications.map((notification) => (
                    <TableRow key={notification.id}>
                      <TableCell className="font-medium">{notification.title}</TableCell>
                      <TableCell>{getTypeBadge(notification.type)}</TableCell>
                      <TableCell>{getTargetBadge(notification.target)}</TableCell>
                      <TableCell>{notification.sent_count}</TableCell>
                      <TableCell>{new Date(notification.created_at).toLocaleString("zh-CN")}</TableCell>
                      <TableCell>
                        <Badge className="bg-green-100 text-green-800">已发送</Badge>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
