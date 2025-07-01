好的，下面为您设计基于FastAPI的API接口，数据库以SQLite为例。  
接口分为用户端和后台管理端，采用RESTful风格，接口返回JSON。

---

## 一、用户端 API

### 1. 注册与登录

- **POST /api/register**  
  用户注册  
  请求参数：`email`, `password`  
  返回：注册结果

- **POST /api/login**  
  用户登录  
  请求参数：`email`, `password`  
  返回：登录token

---

### 2. 会员信息

- **GET /api/membership**  
  获取当前用户会员信息  
  需登录  
  返回：本地会员、在线会员状态、到期时间、剩余空间等

---

### 3. 卡密充值

- **POST /api/redeem**  
  卡密兑换/续费  
  请求参数：`code`  
  返回：兑换结果（如续费成功、空间增加等）

---

### 4. 个人信息

- **GET /api/profile**  
  获取个人信息  
  需登录

- **PUT /api/profile**  
  修改个人信息（如密码）

---

### 5. 系统通知

- **GET /api/notifications**  
  获取系统通知列表  
  需登录

- **PUT /api/notifications/{id}/read**  
  标记通知为已读

---

## 二、后台管理 API

### 1. 管理员登录

- **POST /api/admin/login**  
  管理员登录  
  请求参数：`username`, `password`  
  返回：token

---

### 2. 卡密管理

- **POST /api/admin/card-codes**  
  批量生成卡密  
  请求参数：`count`, `type`, `value`  
  返回：生成的卡密列表

- **GET /api/admin/card-codes**  
  查询卡密列表（支持筛选、分页）

- **GET /api/admin/card-codes/{code}/logs**  
  查询某个卡密的使用记录

---

### 3. 会员管理

- **GET /api/admin/memberships**  
  查询会员列表（支持筛选、分页）

- **GET /api/admin/memberships/{user_id}**  
  查询某个用户的会员详情

- **POST /api/admin/memberships/{user_id}/renew**  
  管理员手动为用户续费/调整会员

---

### 4. 数据统计

- **GET /api/admin/statistics**  
  获取数据统计（会员数量、卡密使用情况等）

---

### 5. 通知管理

- **GET /api/admin/notifications**  
  查询通知列表

---

## 三、接口安全

- 用户端接口需登录token（JWT等）认证
- 管理端接口需管理员token认证

---

如需详细的某个接口参数、返回示例或FastAPI代码示例，请告知！  
如果有接口需要增删改动，也请随时指出。