收到！
接下来将推进“管理后台”相关 API 的实现，严格按 openapi.yaml 和文档规范，分阶段开发与测试。
本阶段优先实现管理员登录与卡密管理相关接口，具体包括：
管理员登录
POST /api/admin/login
校验账号密码，生成管理员 JWT，返回 token
批量生成卡密
POST /api/admin/card-codes
校验管理员权限，生成指定数量/类型/面值的卡密，批量插入，返回卡密列表
查询卡密列表
GET /api/admin/card-codes
校验管理员权限，分页查询卡密表，返回卡密信息
查询卡密使用记录
GET /api/admin/card-codes/{code}/logs
校验管理员权限，查询指定卡密的使用记录
开发步骤
路由文件：output/src/openapi_server/api/admin.py
测试文件：output/tests/test_api_admin.py
涉及管理员鉴权、卡密生成工具、批量插入、分页、日志查询等
请稍等，马上为你实现第一步：管理员登录接口。