import { test, expect } from '@playwright/test';

const ROUTES = [
  { name: 'Dashboard', path: '/' },
  { name: 'Navigation', path: '/navigation' },
  { name: 'Crowd Status', path: '/crowd' },
  { name: 'Incidents', path: '/incidents' },
  { name: 'Volunteers', path: '/volunteers' },
  { name: 'Pulse', path: '/pulse' },
  { name: 'Settings', path: '/settings' },
];

test.describe('Sidebar Routing Architecture', () => {
  for (const route of ROUTES) {
    test(`Sidebar link for ${route.name} navigates successfully without 404`, async ({ page }) => {
      // Start at dashboard
      await page.goto('/');
      
      // Check if sidebar link exists
      const link = page.getByRole('link', { name: route.name, exact: true });
      await expect(link).toBeVisible();
      
      // Click link
      await link.click();
      
      // Verify URL changes
      await page.waitForURL(`**${route.path}`);
      
      // Ensure there's no 404 indicator text
      const bodyText = await page.locator('body').innerText();
      expect(bodyText).not.toContain('This page could not be found');
      expect(bodyText).not.toContain('404');
      
      // Verify page is loaded successfully by checking for generic Next.js root error element
      const errorBoundary = page.locator('#__next_error__');
      await expect(errorBoundary).not.toBeAttached();
    });
  }
});
