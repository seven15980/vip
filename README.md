# vip 项目

本项目为会员管理系统，包含前后端代码，支持会员卡、通知、后台管理等功能。

## 目录结构
- backend/         后端 mock API
- membership/      前端 Next.js 会员管理页面
- output/          后端 Python FastAPI 代码及相关脚本
- 文档/            项目开发文档

## 快速开始

### 前端
```bash
cd membership
pnpm install
pnpm dev
```

### 后端
```bash
cd output
# 建议使用虚拟环境
pip install -r requirements.txt
python src/openapi_server/main.py
```

## 贡献
欢迎提交 issue 和 PR。

## License
MIT 