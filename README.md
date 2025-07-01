# vip 项目 | VIP Project

本项目为会员管理系统，包含前后端代码，支持会员卡、通知、后台管理等功能。

This project is a membership management system, including frontend and backend code, supporting membership cards, notifications, admin dashboard, and more.

## 目录结构 | Directory Structure
- backend/         后端 mock API | Backend mock API
- membership/      前端 Next.js 会员管理页面 | Frontend Next.js membership pages
- output/          后端 Python FastAPI 代码及相关脚本 | Backend Python FastAPI code and scripts
- 文档/            项目开发文档 | Project documentation

## 快速开始 | Quick Start

### 前端 | Frontend
```bash
cd membership
pnpm install
pnpm dev
```

### 后端 | Backend
```bash
cd output
# 建议使用虚拟环境 | It is recommended to use a virtual environment
pip install -r requirements.txt
python src/openapi_server/main.py
```

## 贡献 | Contribution
欢迎提交 issue 和 PR。
Feel free to submit issues and pull requests.

## License
MIT 