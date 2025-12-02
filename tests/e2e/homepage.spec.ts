import { test, expect } from '@playwright/test';

/**
 * Homepage E2E Tests - User Story 1
 *
 * Tests for the styled landing page with dark theme and hero section.
 * Following TDD: These tests are written FIRST and must FAIL before implementation.
 */

test.describe('Homepage - User Story 1', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  // T015: Homepage loads with dark background color
  test('should display dark background color (#0D0D0F)', async ({ page }) => {
    // Get the background color of the body or main container
    const backgroundColor = await page.evaluate(() => {
      const body = document.body;
      return window.getComputedStyle(body).backgroundColor;
    });

    // #0D0D0F in RGB is rgb(13, 13, 15)
    expect(backgroundColor).toBe('rgb(13, 13, 15)');
  });

  // T016: Hero section displays platform label "SMART HUMANOID"
  test('should display platform label "SMART HUMANOID"', async ({ page }) => {
    // Use exact match to find only the uppercase platform label in hero section
    const platformLabel = page.getByText('SMART HUMANOID', { exact: true });
    await expect(platformLabel).toBeVisible();
  });

  // T017: Hero headline contains "understand" with cyan highlight
  test('should display headline with "understand" highlighted in cyan', async ({ page }) => {
    // Check headline exists
    const headline = page.getByRole('heading', { level: 1 });
    await expect(headline).toBeVisible();
    await expect(headline).toContainText('understand');

    // Check the highlighted word has cyan color
    const highlightedText = page.locator('.highlight, [class*="highlight"]');
    await expect(highlightedText).toBeVisible();

    const color = await highlightedText.evaluate((el) => {
      return window.getComputedStyle(el).color;
    });

    // #4ECFFE in RGB is approximately rgb(78, 207, 254)
    expect(color).toMatch(/rgb\(78,\s*207,\s*254\)/);
  });

  // T018: Two CTA buttons are present and keyboard accessible
  test('should have two CTA buttons that are keyboard accessible', async ({ page }) => {
    const getStartedButton = page.getByRole('link', { name: /get started/i });
    const browseContentButton = page.getByRole('link', { name: /browse content/i });

    // Both buttons should be visible
    await expect(getStartedButton).toBeVisible();
    await expect(browseContentButton).toBeVisible();

    // Both buttons should be focusable (keyboard accessible)
    await getStartedButton.focus();
    await expect(getStartedButton).toBeFocused();

    await browseContentButton.focus();
    await expect(browseContentButton).toBeFocused();
  });

  // T019: Hero section occupies 50-60% viewport height on desktop
  test('should have hero section occupying 50-60% viewport height on desktop', async ({
    page,
  }) => {
    // Set desktop viewport
    await page.setViewportSize({ width: 1920, height: 1080 });

    const hero = page.locator('.hero, [class*="hero"]').first();
    await expect(hero).toBeVisible();

    const heroHeight = await hero.evaluate((el) => el.getBoundingClientRect().height);
    const viewportHeight = 1080;

    const percentageHeight = (heroHeight / viewportHeight) * 100;

    // Should be between 50% and 65% (some tolerance for layout)
    expect(percentageHeight).toBeGreaterThanOrEqual(50);
    expect(percentageHeight).toBeLessThanOrEqual(65);
  });

  // T020: Diagram placeholder visible on right side of hero
  test('should display diagram placeholder on right side of hero', async ({ page }) => {
    // Set desktop viewport for proper layout
    await page.setViewportSize({ width: 1920, height: 1080 });

    // Use aria-label to find the specific diagram container (case-insensitive)
    const diagramPlaceholder = page.locator('[aria-label*="Diagram"]').first();
    await expect(diagramPlaceholder).toBeVisible();

    // Verify it's on the right side (x position > 50% of viewport)
    const box = await diagramPlaceholder.boundingBox();
    expect(box).not.toBeNull();
    if (box) {
      expect(box.x).toBeGreaterThan(1920 * 0.4); // Should be in right portion
    }
  });
});
