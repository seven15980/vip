"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { ArrowLeft, Plus, Search, Download } from "lucide-react"
import Link from "next/link"
import { getApiUrl } from "@/lib/utils"

interface CardCode {
  code: string
  type: string
  value: number
  status: string
  created_at: string
  used_at: string | null
  used_by: string | null
}

export default function AdminCardsPage() {
  const [cards, setCards] = useState<CardCode[]>([])
  const [loading, setLoading] = useState(true)
  const [generating, setGenerating] = useState(false)
  const [generateForm, setGenerateForm] = useState({
    count: "10",
    type: "local",
    value: "30",
  })
  const [page, setPage] = useState(1)
  const [pageSize] = useState(10)
  const [total, setTotal] = useState(0)

  useEffect(() => {
    fetchCards(page)
  }, [page])

  const fetchCards = async (pageParam = page) => {
    setLoading(true)
    try {
      const token = localStorage.getItem("adminToken")
      const response = await fetch(getApiUrl(`/api/admin/card-codes?page=${pageParam}&page_size=${pageSize}`), {
        headers: { Authorization: `Bearer ${token}` },
      })

      if (response.ok) {
        const result = await response.json()
        const cardList = Array.isArray(result.data) ? result.data : (result.data?.data || [])
        setCards(cardList)
        setTotal(result.data?.total || 0)
      }
    } catch (error) {
      console.error("获取卡密列表失败:", error)
    } finally {
      setLoading(false)
    }
  }

  const handleGenerate = async () => {
    setGenerating(true)
    try {
      const token = localStorage.getItem("adminToken")
      const response = await fetch(getApiUrl("/api/admin/card-codes"), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          ...generateForm,
          count: Number.parseInt(generateForm.count),
          value: Number.parseInt(generateForm.value),
        }),
      })

      if (response.ok) {
        const data = await response.json()
        alert(`成功生成 ${generateForm.count} 个卡密`)
        fetchCards() // 重新获取列表
      }
    } catch (error) {
      alert("生成失败，请稍后重试")
    } finally {
      setGenerating(false)
    }
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "used":
        return <Badge variant="secondary">已使用</Badge>
      case "unused":
        return <Badge className="bg-green-100 text-green-800">未使用</Badge>
      default:
        return <Badge variant="outline">未知</Badge>
    }
  }

  const getTypeBadge = (type: string) => {
    switch (type) {
      case "local":
        return <Badge className="bg-yellow-100 text-yellow-800">本地</Badge>
      case "online":
        return <Badge className="bg-blue-100 text-blue-800">在线</Badge>
      case "both":
        return <Badge className="bg-purple-100 text-purple-800">本地+在线</Badge>
      default:
        return <Badge variant="outline">{type}</Badge>
    }
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
          <div className="flex items-center h-16">
            <Link href="/admin/dashboard">
              <Button variant="ghost" size="sm" className="mr-4">
                <ArrowLeft className="h-4 w-4 mr-2" />
                返回
              </Button>
            </Link>
            <h1 className="text-xl font-semibold text-gray-900">卡密管理</h1>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
        {/* 生成卡密 */}
        <Card className="border-0 shadow-lg">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Plus className="h-5 w-5" />
              批量生成卡密
            </CardTitle>
            <CardDescription>生成新的卡密用于用户充值</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="space-y-2">
                <Label htmlFor="count">生成数量</Label>
                <Input
                  id="count"
                  type="number"
                  min="1"
                  max="100"
                  value={generateForm.count}
                  onChange={(e) => {
                    setGenerateForm({ ...generateForm, count: e.target.value });
                  }}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="type">卡密类型</Label>
                <Select
                  value={generateForm.type}
                  onValueChange={(value) => setGenerateForm({ ...generateForm, type: value })}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="local">本地会员</SelectItem>
                    <SelectItem value="online">在线会员</SelectItem>
                    <SelectItem value="both">本地+在线会员</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label htmlFor="value">有效天数</Label>
                <Input
                  id="value"
                  type="number"
                  min="1"
                  max="3650"
                  value={generateForm.value}
                  onChange={(e) => {
                    setGenerateForm({ ...generateForm, value: e.target.value });
                  }}
                />
              </div>
              <div className="flex items-end">
                <Button onClick={handleGenerate} disabled={generating} className="w-full">
                  {generating ? "生成中..." : "生成卡密"}
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* 卡密列表 */}
        <Card className="border-0 shadow-lg">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>卡密列表</CardTitle>
                <CardDescription>查看和管理所有卡密</CardDescription>
              </div>
              <div className="flex items-center gap-2">
                <Button variant="outline" size="sm">
                  <Search className="h-4 w-4 mr-2" />
                  搜索
                </Button>
                <Button variant="outline" size="sm">
                  <Download className="h-4 w-4 mr-2" />
                  导出
                </Button>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div className="rounded-md border">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>卡密代码</TableHead>
                    <TableHead>类型</TableHead>
                    <TableHead>天数</TableHead>
                    <TableHead>状态</TableHead>
                    <TableHead>创建时间</TableHead>
                    <TableHead>使用时间</TableHead>
                    <TableHead>使用者</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {cards.map((card) => (
                    <TableRow key={card.code}>
                      <TableCell className="font-mono">{card.code}</TableCell>
                      <TableCell>{getTypeBadge(card.type)}</TableCell>
                      <TableCell>{card.value}天</TableCell>
                      <TableCell>{getStatusBadge(card.status)}</TableCell>
                      <TableCell>{new Date(card.created_at).toLocaleDateString("zh-CN")}</TableCell>
                      <TableCell>{card.used_at ? new Date(card.used_at).toLocaleDateString("zh-CN") : "-"}</TableCell>
                      <TableCell>{card.used_by || "-"}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
              <div className="flex justify-end items-center mt-4">
                <Button
                  variant="outline"
                  size="sm"
                  disabled={page === 1}
                  onClick={() => setPage(page - 1)}
                  className="mr-2"
                >
                  上一页
                </Button>
                <span>
                  第 {page} / {Math.max(1, Math.ceil(total / pageSize))} 页（共 {total} 条）
                </span>
                <Button
                  variant="outline"
                  size="sm"
                  disabled={page >= Math.ceil(total / pageSize)}
                  onClick={() => setPage(page + 1)}
                  className="ml-2"
                >
                  下一页
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
