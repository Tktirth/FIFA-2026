import { test, expect } from '@playwright/test';

test.describe('Voice Assistant Interactions', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
    await page.getByRole('button', { name: /Operations/i }).click();
    await page.waitForURL(/.*dashboard\/operations/);
  });

  test('can open and close the Gemini Live Assistant', async ({ page }) => {
    await page.locator('button').filter({ hasText: /^$/ }).last(); // The Floating button (Sparkles icon) usually is the last button or can be targeted by aria-label.
    // Let's assume the button doesn't have an exact aria-label yet, we should fix that in Phase 7.
    // Wait for the panel to be hidden
    await expect(page.getByText('Nexova AI')).not.toBeVisible();
    
    // In our component it's an SVG. We can target it via class.
    await page.locator('.fixed.bottom-6.right-6').click();
    
    // Panel should appear
    await expect(page.getByText('Nexova AI')).toBeVisible();

    // Close panel
    await page.getByRole('button', { name: /Close Assistant/i }).click();
    await expect(page.getByText('Nexova AI')).not.toBeVisible();
  });

  test('can submit a query to the assistant', async ({ page }) => {
    await page.locator('.fixed.bottom-6.right-6').click();
    
    const input = page.getByRole('textbox', { name: /Query input/i });
    await input.fill('What is the current crowd density?');
    await page.getByRole('button', { name: /Send query/i }).click();

    // Verify user message appears
    await expect(page.getByText('What is the current crowd density?')).toBeVisible();

    // Verify AI response appears (mocked with timeout in component)
    await expect(page.getByText(/Analyzing real-time data/)).toBeVisible({ timeout: 5000 });
  });
});
