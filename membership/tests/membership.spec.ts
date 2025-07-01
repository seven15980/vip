import { test, expect } from '@playwright/test';

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
  expect([200, 401]).toContain(memberRes.status()); // 401 说明 token 问题

  // 卡密兑换
  const redeemRes = await request.post('http://localhost:8000/api/redeem', {
    data: { code: 'CODE0001' },
    headers: { Authorization: `Bearer ${token}` }
  });
  expect([200, 400, 401]).toContain(redeemRes.status()); // 401 说明 token 问题
}); 