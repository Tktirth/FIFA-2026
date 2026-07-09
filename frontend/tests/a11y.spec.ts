import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Accessibility (WCAG 2.2 AA)', () => {
  test('Dashboard operations page should not have any automatically detectable accessibility issues', async ({ page }) => {
    await page.goto('/login');
    await page.getByRole('button', { name: /Operations/i }).click({ force: true });
    await page.getByRole('button', { name: /Enter Platform/i }).click();
    await page.waitForURL('/');
    await page.waitForTimeout(2000); // Wait for framer-motion animations to complete

    const accessibilityScanResults = await new AxeBuilder({ page })
      .disableRules(['region'])
      .analyze();
    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test('Login page should not have any automatically detectable accessibility issues', async ({ page }) => {
    await page.goto('/login');
    await page.waitForTimeout(2000); // Wait for framer-motion animations to complete
    const accessibilityScanResults = await new AxeBuilder({ page })
      .disableRules(['region'])
      .analyze();
    expect(accessibilityScanResults.violations).toEqual([]);
  });
});
