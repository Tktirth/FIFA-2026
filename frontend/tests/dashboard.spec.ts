import { test, expect } from '@playwright/test';

test.describe('Dashboard Navigation & Layout', () => {
  test.beforeEach(async ({ page }) => {
    // Login as Operations
    await page.goto('/login');
    await page.getByRole('button', { name: /Operations/i }).click();
    await page.waitForURL(/.*dashboard\/operations/);
  });

  test('renders key metrics on Operations dashboard', async ({ page }) => {
    await expect(page.getByText(/Current Attendance/i)).toBeVisible();
    await expect(page.getByText(/Active Incidents/i)).toBeVisible();
    await expect(page.getByText(/System Health Score/i)).toBeVisible();
  });

  test('renders Live Crowd Chart', async ({ page }) => {
    const chartContainer = page.locator('.recharts-responsive-container').first();
    await expect(chartContainer).toBeVisible();
  });

  test('renders Incident Distribution Chart', async ({ page }) => {
    const chartContainer = page.locator('.recharts-responsive-container').nth(1);
    await expect(chartContainer).toBeVisible();
  });

  test('renders the Interactive Stadium Map', async ({ page }) => {
    const map = page.locator('.leaflet-container');
    await expect(map).toBeVisible();
  });
});
