"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { ArrowLeft, Users, Search, Settings, Calendar } from "lucide-react"
import Link from "next/link"
import { getApiUrl } from "@/lib/utils"

interface Membership {
  user_id: number
  email: string
  local_expire: string | null
  online_expire: string | null
  storage_total: number | null
  last_login: string | null
}

export default function AdminMembersPage() {
  const [members, setMembers] = useState<Membership[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedMember, setSelectedMember] = useState<Membership | null>(null)
  const [renewForm, setRenewForm] = useState({
    type: "online",
    months: 1,
    storage: 10,
  })
  const [page, setPage] = useState(1)
  const [pageSize] = useState(10)
  const [total, setTotal] = useState(0)

  useEffect(() => {
    fetchMembers()
  }, [page])

  const fetchMembers = async () => {
    try {
      const token = localStorage.getItem("adminToken")
      const response = await fetch(getApiUrl(`/api/admin/memberships?page=${page}&page_size=${pageSize}`), {
        headers: { Authorization: `Bearer ${token}` },
      })

      if (response.ok) {
        const result = await response.json()
        // 兼容分页结构
        const memberList = Array.isArray(result.data) ? result.data : (result.data?.data || [])
        setMembers(memberList)
        setTotal(result.data?.total || 0)
      }
    } catch (error) {
      console.error("获取会员列表失败:", error)
    } finally {
      setLoading(false)
    }
  }

  const handleRenew = async () => {
    if (!selectedMember) return

    try {
      const token = localStorage.getItem("adminToken")
      const response = await fetch(getApiUrl(`/api/admin/memberships/${selectedMember.user_id}/renew`), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(renewForm),
      })

      if (response.ok) {
        alert("续费成功")
        fetchMembers()
        setSelectedMember(null)
      }
    } catch (error) {
      alert("续费失败，请稍后重试")
    }
  }

  const isExpired = (dateString: string | null) => {
    if (!dateString) return true;
    const d = new Date(dateString)
    return isNaN(d.getTime()) || d < new Date()
  }

  const getStatusBadge = (localExpire: string | null, onlineExpire: string | null) => {
    const localExpired = isExpired(localExpire)
    const onlineExpired = isExpired(onlineExpire)
    if (!localExpired && !onlineExpired) {
      return <Badge className="bg-green-100 text-green-800">双重会员</Badge>
    } else if (!localExpired) {
      return <Badge className="bg-yellow-100 text-yellow-800">本地会员</Badge>
    } else if (!onlineExpired) {
      return <Badge className="bg-blue-100 text-blue-800">在线会员</Badge>
    } else {
      return <Badge variant="secondary">已过期</Badge>
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
            <h1 className="text-xl font-semibold text-gray-900">会员管理</h1>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Card className="border-0 shadow-lg">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle className="flex items-center gap-2">
                  <Users className="h-5 w-5" />
                  会员列表
                </CardTitle>
                <CardDescription>查看和管理所有用户的会员信息</CardDescription>
              </div>
              <Button variant="outline" size="sm">
                <Search className="h-4 w-4 mr-2" />
                搜索用户
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            <div className="rounded-md border">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>用户ID</TableHead>
                    <TableHead>邮箱</TableHead>
                    <TableHead>会员状态</TableHead>
                    <TableHead>本地到期</TableHead>
                    <TableHead>在线到期</TableHead>
                    <TableHead>存储空间</TableHead>
                    <TableHead>最后登录</TableHead>
                    <TableHead>操作</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {members.map((member, idx) => (
                    <TableRow key={member.user_id + '-' + (member.email || idx)}>
                      <TableCell>{member.user_id}</TableCell>
                      <TableCell>{member.email || '-'}</TableCell>
                      <TableCell>{getStatusBadge(member.local_expire, member.online_expire)}</TableCell>
                      <TableCell>
                        <span className={isExpired(member.local_expire) ? "text-red-600" : "text-green-600"}>
                          {member.local_expire && typeof member.local_expire === 'string' && !isNaN(new Date(member.local_expire).getTime()) ? new Date(member.local_expire).toLocaleDateString("zh-CN") : '-'}
                        </span>
                      </TableCell>
                      <TableCell>
                        <span className={isExpired(member.online_expire) ? "text-red-600" : "text-green-600"}>
                          {member.online_expire && typeof member.online_expire === 'string' && !isNaN(new Date(member.online_expire).getTime()) ? new Date(member.online_expire).toLocaleDateString("zh-CN") : '-'}
                        </span>
                      </TableCell>
                      <TableCell>{member.storage_total != null ? member.storage_total + 'GB' : '-'}</TableCell>
                      <TableCell>{member.last_login && typeof member.last_login === 'string' && !isNaN(new Date(member.last_login).getTime()) ? new Date(member.last_login).toLocaleDateString("zh-CN") : '-'}</TableCell>
                      <TableCell>
                        <Dialog>
                          <DialogTrigger asChild>
                            <Button variant="outline" size="sm" onClick={() => setSelectedMember(member)}>
                              <Settings className="h-4 w-4 mr-1" />
                              管理
                            </Button>
                          </DialogTrigger>
                          <DialogContent>
                            <DialogHeader>
                              <DialogTitle>会员管理</DialogTitle>
                              <DialogDescription>为用户 {member.email} 续费或调整会员权限</DialogDescription>
                            </DialogHeader>
                            <div className="space-y-4">
                              <div className="space-y-2">
                                <Label>续费类型</Label>
                                <Select
                                  value={renewForm.type}
                                  onValueChange={(value) => setRenewForm({ ...renewForm, type: value })}
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
                                <Label>续费月数</Label>
                                <Input
                                  type="number"
                                  min="1"
                                  max="36"
                                  value={renewForm.months}
                                  onChange={(e) =>
                                    setRenewForm({ ...renewForm, months: Number.parseInt(e.target.value) })
                                  }
                                />
                              </div>
                              {(renewForm.type === "online" || renewForm.type === "both") && (
                                <div className="space-y-2">
                                  <Label>存储空间 (GB)</Label>
                                  <Input
                                    type="number"
                                    min="5"
                                    max="1000"
                                    value={renewForm.storage}
                                    onChange={(e) =>
                                      setRenewForm({ ...renewForm, storage: Number.parseInt(e.target.value) })
                                    }
                                  />
                                </div>
                              )}
                              <Button onClick={handleRenew} className="w-full">
                                <Calendar className="h-4 w-4 mr-2" />
                                确认续费
                              </Button>
                            </div>
                          </DialogContent>
                        </Dialog>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
              {/* 分页控件 */}
              <div className="flex justify-end items-center gap-2 p-4">
                <Button
                  variant="outline"
                  size="sm"
                  disabled={page === 1}
                  onClick={() => setPage(page - 1)}
                >上一页</Button>
                <span>第 {page} / {Math.max(1, Math.ceil(total / pageSize))} 页</span>
                <Button
                  variant="outline"
                  size="sm"
                  disabled={page >= Math.ceil(total / pageSize)}
                  onClick={() => setPage(page + 1)}
                >下一页</Button>
                <span>共 {total} 条</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
