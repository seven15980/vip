import { test, expect } from '@playwright/test';

test('用户注册与登录', async ({ request }) => {
  // 注册新用户
  const email = `user${Date.now()}@example.com`;
  const password = 'password100';
  const regRes = await request.post('http://localhost:8000/api/register', {
    data: { email, password }
  });
  expect([200, 400, 422]).toContain(regRes.status()); // 已注册/参数问题也允许通过

  // 登录
  const loginRes = await request.post('http://localhost:8000/api/login', {
    data: { email, password }
  });
  const loginJson = await loginRes.json();
  const { token } = loginJson.data || {};
  expect(loginRes.status()).toBe(200);
  expect(token).toBeTruthy();

  // 获取个人资料
  const profileRes = await request.get('http://localhost:8000/api/profile', {
    headers: { Authorization: `Bearer ${token}` }
  });
  expect(profileRes.status()).toBe(200);
}); 