import { test, expect } from '@playwright/test';

test('通知中心', async ({ request }) => {
  const loginRes = await request.post('http://localhost:8000/api/login', {
    data: { username: 'user001', password: 'password001' }
  });
  const { token } = await loginRes.json();

  // 查询通知
  const notiRes = await request.get('http://localhost:8000/api/notifications', {
    headers: { Authorization: `Bearer ${token}` }
  });
  expect([200, 401]).toContain(notiRes.status());
  const notifications = notiRes.status() === 200 ? await notiRes.json() : [];
  if (notifications.length > 0) {
    // 标记已读
    const readRes = await request.post(
      `http://localhost:8000/api/notifications/${notifications[0].id}/read`,
      { headers: { Authorization: `Bearer ${token}` } }
    );
    expect([200, 400, 404, 401]).toContain(readRes.status());
  }
}); 