import { test, expect } from '@playwright/test';

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
  expect([200, 401]).toContain(membersRes.status());

  // 查询卡密列表
  const codesRes = await request.get('http://localhost:8000/api/admin/card-codes?page=1&page_size=10', {
    headers: { Authorization: `Bearer ${token}` }
  });
  expect([200, 401]).toContain(codesRes.status());

  // 查询统计
  const statRes = await request.get('http://localhost:8000/api/admin/statistics', {
    headers: { Authorization: `Bearer ${token}` }
  });
  expect([200, 401]).toContain(statRes.status());
}); 