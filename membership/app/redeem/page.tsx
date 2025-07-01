"use client"

import type React from "react"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { ArrowLeft, CreditCard, CheckCircle, XCircle } from "lucide-react"
import Link from "next/link"
import { getApiUrl } from "@/lib/utils"
import { useApiDiff } from "../../tools/schema-diff/useApiDiff"
import { zodSchemaToTree } from "../../tools/schema-diff/zod2tree"
import { jsonToTree } from "../../tools/schema-diff/json2tree"
import { compareTrees } from "../../tools/schema-diff/compare"
import { z } from "zod"

// 定义zod schema（请根据实际接口返回结构调整）
const redeemSchema = z.object({
  message: z.string(),
  // 你可以根据实际返回结构补充更多字段
})

export default function RedeemPage() {
  const [code, setCode] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [result, setResult] = useState<{ success: boolean; message: string } | null>(null)
  const [redeemData, setRedeemData] = useState<any>(null)

  const handleRedeem = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!code.trim()) return

    setIsLoading(true)
    setResult(null)

    try {
      const token = localStorage.getItem("token")
      const response = await fetch(getApiUrl("/api/redeem"), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ code: code.trim() }),
      })

      const data = await response.json()
      setRedeemData(data)
      // 自动diff
      try {
        redeemSchema.parse(data)
      } catch (e) {
        console.error("/api/redeem zod校验失败:", e)
      }
      const expectedTree = zodSchemaToTree(redeemSchema)
      const actualTree = jsonToTree(data)
      const diffs = compareTrees(expectedTree, actualTree)
      console.log("【自动化diff】/api/redeem")
      console.table(diffs)

      if (response.ok) {
        setResult({ success: true, message: data.message || "兑换成功！" })
        setCode("")
      } else {
        setResult({ success: false, message: data.message || "兑换失败，请检查卡密是否正确" })
      }
    } catch (error) {
      setResult({ success: false, message: "网络错误，请稍后重试" })
    } finally {
      setIsLoading(false)
    }
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
            <h1 className="text-xl font-semibold text-gray-900">卡密充值</h1>
          </div>
        </div>
      </header>

      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Card className="border-0 shadow-lg">
          <CardHeader className="text-center">
            <div className="w-16 h-16 bg-gradient-to-r from-green-500 to-emerald-600 rounded-2xl mx-auto mb-4 flex items-center justify-center">
              <CreditCard className="h-8 w-8 text-white" />
            </div>
            <CardTitle className="text-2xl">卡密兑换</CardTitle>
            <CardDescription>输入您的卡密代码来延长会员服务或激活新的会员权益</CardDescription>
          </CardHeader>

          <CardContent className="space-y-6">
            {result && (
              <Alert className={result.success ? "border-green-200 bg-green-50" : "border-red-200 bg-red-50"}>
                <div className="flex items-center gap-2">
                  {result.success ? (
                    <CheckCircle className="h-4 w-4 text-green-600" />
                  ) : (
                    <XCircle className="h-4 w-4 text-red-600" />
                  )}
                  <AlertDescription className={result.success ? "text-green-800" : "text-red-800"}>
                    {result.message}
                  </AlertDescription>
                </div>
              </Alert>
            )}

            <form onSubmit={handleRedeem} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="code">卡密代码</Label>
                <Input
                  id="code"
                  type="text"
                  placeholder="请输入卡密代码，如：ABCD1234"
                  value={code}
                  onChange={(e) => setCode(e.target.value.toUpperCase())}
                  className="text-center text-lg font-mono tracking-wider"
                  maxLength={20}
                  required
                />
                <p className="text-xs text-gray-500 text-center">卡密代码通常为8-20位字母数字组合</p>
              </div>

              <Button type="submit" className="w-full" disabled={isLoading || !code.trim()}>
                {isLoading ? "兑换中..." : "立即兑换"}
              </Button>
            </form>

            {/* 使用说明 */}
            <div className="bg-blue-50 rounded-lg p-4 space-y-3">
              <h4 className="font-medium text-blue-900">使用说明</h4>
              <ul className="text-sm text-blue-800 space-y-1">
                <li>• 每个卡密只能使用一次</li>
                <li>• 卡密有效期请以购买时说明为准</li>
                <li>• 兑换成功后会员时间将自动延长</li>
                <li>• 如遇问题请联系客服处理</li>
              </ul>
            </div>

            {/* 购买提示 */}
            <div className="bg-gray-50 rounded-lg p-4 text-center">
              <p className="text-sm text-gray-600 mb-2">还没有卡密？</p>
              <Button variant="outline" size="sm">
                前往购买
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
