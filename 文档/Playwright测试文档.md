下面是专门为你的会员系统后端接口量身定制的 Playwright e2e 测试文档（含账号、典型流程、Playwright 脚本结构建议），适合前后端联调、自动化验收、CI/CD 场景。

---

# 会员系统 Playwright e2e 测试文档

## 一、准备工作

1. **测试账号**
   - 普通用户：`user001` / `password001`
   - 管理员：`admin` / `admin123`
   - 卡密示例：`CODE0001`
2. **Playwright 安装**
   ```bash
   npm install -D @playwright/test
   npx playwright install
   ```
   已经安装好，可以直接测试
3. **测试环境**
   - 前端启动于 `http://localhost:3000`
   - 后端 API 启动于 `http://localhost:8000`

---

## 二、Playwright 脚本结构建议

- `tests/`
  - `auth.spec.ts`         // 注册、登录、token 测试
  - `membership.spec.ts`   // 会员信息、续费
  - `redeem.spec.ts`       // 卡密兑换
  - `notification.spec.ts` // 通知中心
  - `admin.spec.ts`        // 管理后台

---

## 三、典型 Playwright 测试用例（伪代码+片段）

### 1. 用户注册与登录

```typescript
import { test, expect } from '@playwright/test';

test('用户注册与登录', async ({ request }) => {
  // 注册
  const regRes = await request.post('http://localhost:8000/api/register', {
    data: { username: 'user100', password: 'password100' }
  });
  expect(regRes.status()).toBe(200);

  // 登录
  const loginRes = await request.post('http://localhost:8000/api/login', {
    data: { username: 'user001', password: 'password001' }
  });
  expect(loginRes.status()).toBe(200);
  const { token } = await loginRes.json();
  expect(token).toBeTruthy();

  // 获取个人资料
  const profileRes = await request.get('http://localhost:8000/api/profile', {
    headers: { Authorization: `Bearer ${token}` }
  });
  expect(profileRes.status()).toBe(200);
});
```

---

### 2. 会员信息与卡密兑换

```typescript
test('会员信息与卡密兑换', async ({ request }) => {
  // 登录获取 token
  const loginRes = await request.post('http://localhost:8000/api/login', {
    data: { username: 'user001', password: 'password001' }
  });
  const { token } = await loginRes.json();

  // 查询会员信息
  const memberRes = await request.get('http://localhost:8000/api/membership', {
    headers: { Authorization: `Bearer ${token}` }
  });
  expect(memberRes.status()).toBe(200);

  // 卡密兑换
  const redeemRes = await request.post('http://localhost:8000/api/redeem', {
    data: { code: 'CODE0001' },
    headers: { Authorization: `Bearer ${token}` }
  });
  expect(redeemRes.status()).toBe(200);
});
```

---

### 3. 通知中心

```typescript
test('通知中心', async ({ request }) => {
  const loginRes = await request.post('http://localhost:8000/api/login', {
    data: { username: 'user001', password: 'password001' }
  });
  const { token } = await loginRes.json();

  // 查询通知
  const notiRes = await request.get('http://localhost:8000/api/notifications', {
    headers: { Authorization: `Bearer ${token}` }
  });
  expect(notiRes.status()).toBe(200);
  const notifications = await notiRes.json();
  if (notifications.length > 0) {
    // 标记已读
    const readRes = await request.post(
      `http://localhost:8000/api/notifications/${notifications[0].id}/read`,
      { headers: { Authorization: `Bearer ${token}` } }
    );
    expect(readRes.status()).toBe(200);
  }
});
```

---

### 4. 管理后台

```typescript
test('管理员功能', async ({ request }) => {
  // 管理员登录
  const loginRes = await request.post('http://localhost:8000/api/admin/login', {
    data: { username: 'admin', password: 'admin123' }
  });
  const { token } = await loginRes.json();

  // 查询会员列表
  const membersRes = await request.get('http://localhost:8000/api/admin/memberships?page=1&page_size=10', {
    headers: { Authorization: `Bearer ${token}` }
  });
  expect(membersRes.status()).toBe(200);

  // 查询卡密列表
  const codesRes = await request.get('http://localhost:8000/api/admin/card-codes?page=1&page_size=10', {
    headers: { Authorization: `Bearer ${token}` }
  });
  expect(codesRes.status()).toBe(200);

  // 查询统计
  const statRes = await request.get('http://localhost:8000/api/admin/statistics', {
    headers: { Authorization: `Bearer ${token}` }
  });
  expect(statRes.status()).toBe(200);
});
```

---

## 四、运行测试

1. 在项目根目录下新建 `playwright.config.ts`（如需自定义 baseURL、超时等）。
2. 在 `package.json` 添加脚本：
   ```json
   "scripts": {
     "test:e2e": "playwright test"
   }
   ```
3. 运行测试：
   ```bash
   npx playwright test
   ```

---

## 五、常见问题排查

- 401：检查 token 是否正确携带，格式为 `Bearer <token>`
- 500：检查数据库表结构、数据初始化
- 跨域：Playwright request API 直连后端，不受 CORS 限制

---

## 六、参考资料

- [Playwright 官方文档](https://playwright.dev/docs/test-intro)
- [FastAPI 接口文档](http://localhost:8000/docs)（需后端运行）

---

如需完整 Playwright 测试脚本模板或遇到具体报错，可随时贴出，我帮你补充！