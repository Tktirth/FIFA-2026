const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  // Navigate to localhost:3000
  await page.goto('http://localhost:3000');
  
  // Wait for the bell icon button to be visible
  await page.waitForSelector('button[aria-label="Notifications"]');
  
  // Take screenshot before click
  await page.screenshot({ path: 'before_click.png' });
  
  // Click the bell icon
  await page.click('button[aria-label="Notifications"]');
  
  // Wait a moment for any animation
  await page.waitForTimeout(500);
  
  // Take screenshot after click
  await page.screenshot({ path: 'after_click.png' });
  
  // Check if dropdown text is visible
  const isDropdownVisible = await page.isVisible('text="Notifications"');
  console.log("Dropdown visible after click:", isDropdownVisible);
  
  await browser.close();
})();
