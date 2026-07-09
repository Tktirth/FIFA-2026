import { test, expect } from '@playwright/test';

test.describe('Authentication & Roles', () => {
  test('redirects to login when unauthenticated', async ({ page }) => {
    await page.goto('/dashboard/operations');
    // Assuming auth middleware redirects to /login
    await expect(page).toHaveURL(/.*login/);
  });

  test('can login as Security Persona', async ({ page }) => {
    await page.goto('/login');
    // We assume the UI has buttons or cards for each persona
    await page.getByRole('button', { name: /Security/i }).click();
    await expect(page).toHaveURL(/.*dashboard\/security/);
  });

  test('can login as Operations Persona', async ({ page }) => {
    await page.goto('/login');
    await page.getByRole('button', { name: /Operations/i }).click();
    await expect(page).toHaveURL(/.*dashboard\/operations/);
  });
});
