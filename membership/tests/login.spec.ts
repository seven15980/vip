import { test, expect } from '@playwright/test';

test('用户可以正常登录并跳转到 dashboard', async ({ page }) => {
  await page.goto('http://localhost:3000');

  // 输入邮箱和密码
  await page.getByPlaceholder('请输入邮箱').fill('test@example.com');
  await page.getByPlaceholder('请输入密码').fill('123456');

  // 点击登录
  await page.getByRole('button', { name: '登录' }).click();

  // 跳转到 dashboard
  await expect(page).toHaveURL(/dashboard/);
  // 你可以加更多断言，比如检查页面内容
}); 