import { test, expect } from '@playwright/test';

/**
 * Navigation E2E Tests - User Story 2
 *
 * Tests for the navbar with menu items for different content areas.
 * Following TDD: These tests are written FIRST and must FAIL before implementation.
 */

test.describe('Navigation - User Story 2', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  // T033: Navbar displays "Learn Free" menu item linking to /docs/intro
  test('should display "Learn Free" menu item linking to docs', async ({ page }) => {
    const learnFreeLink = page.getByRole('link', { name: /learn free/i });
    await expect(learnFreeLink).toBeVisible();

    // Verify it links to docs
    const href = await learnFreeLink.getAttribute('href');
    expect(href).toContain('/docs');
  });

  // T034: Navbar displays "Labs" menu item (disabled placeholder)
  test('should display "Labs" menu item as disabled placeholder', async ({ page }) => {
    const labsItem = page.locator('[aria-label*="Labs"]').first();
    await expect(labsItem).toBeVisible();

    // Should be disabled (aria-disabled="true" or has disabled class)
    const isDisabled = await labsItem.evaluate((el) => {
      return (
        el.getAttribute('aria-disabled') === 'true' ||
        el.classList.contains('navbar__link--disabled') ||
        el.getAttribute('title')?.includes('Coming Soon')
      );
    });
    expect(isDisabled).toBe(true);
  });

  // T035: Navbar displays "Personalize" menu item (disabled placeholder)
  test('should display "Personalize" menu item as disabled placeholder', async ({ page }) => {
    const personalizeItem = page.locator('[aria-label*="Personalize"]').first();
    await expect(personalizeItem).toBeVisible();

    // Should be disabled (aria-disabled="true" or has disabled class)
    const isDisabled = await personalizeItem.evaluate((el) => {
      return (
        el.getAttribute('aria-disabled') === 'true' ||
        el.classList.contains('navbar__link--disabled') ||
        el.getAttribute('title')?.includes('Coming Soon')
      );
    });
    expect(isDisabled).toBe(true);
  });

  // T036: Navbar displays search box placeholder on right side
  test('should display search box placeholder on right side of navbar', async ({ page }) => {
    // Set desktop viewport
    await page.setViewportSize({ width: 1920, height: 1080 });

    // Look for search placeholder in navbar
    const searchBox = page.locator('[aria-label*="Search"], [class*="search-placeholder"]').first();
    await expect(searchBox).toBeVisible();

    // Verify it's on the right side (x position > 50% of viewport)
    const box = await searchBox.boundingBox();
    expect(box).not.toBeNull();
    if (box) {
      expect(box.x).toBeGreaterThan(1920 * 0.5);
    }
  });

  // T037: Navbar displays GitHub repository link icon on far right
  test('should display GitHub repository link on far right', async ({ page }) => {
    // Set desktop viewport
    await page.setViewportSize({ width: 1920, height: 1080 });

    // Scope to navbar to avoid footer GitHub link
    const navbar = page.locator('nav.navbar, [class*="navbar"]').first();
    const githubLink = navbar.getByRole('link', { name: /github/i });
    await expect(githubLink).toBeVisible();

    // Verify it links to the correct repository
    const href = await githubLink.getAttribute('href');
    expect(href).toContain('github.com/jamilurrahmanmuhammad/smart-humanoid');

    // Verify it's on the far right
    const box = await githubLink.boundingBox();
    expect(box).not.toBeNull();
    if (box) {
      expect(box.x).toBeGreaterThan(1920 * 0.7);
    }
  });

  // T038: Navbar is transparent over dark background
  test('should have transparent navbar background', async ({ page }) => {
    const navbar = page.locator('nav.navbar, [class*="navbar"]').first();
    await expect(navbar).toBeVisible();

    const backgroundColor = await navbar.evaluate((el) => {
      return window.getComputedStyle(el).backgroundColor;
    });

    // Should be transparent or semi-transparent (rgba with alpha < 1)
    const isTransparent =
      backgroundColor === 'transparent' ||
      backgroundColor === 'rgba(0, 0, 0, 0)' ||
      backgroundColor.includes('rgba') && parseFloat(backgroundColor.split(',')[3]) < 1;

    expect(isTransparent).toBe(true);
  });

  // T039: Menu items show hover feedback
  test('should show hover feedback on menu items', async ({ page }) => {
    // Scope to navbar
    const navbar = page.locator('nav.navbar').first();
    const learnFreeLink = navbar.getByRole('link', { name: /learn free/i });
    await expect(learnFreeLink).toBeVisible();

    // Get initial color
    const initialColor = await learnFreeLink.evaluate((el) => {
      return window.getComputedStyle(el).color;
    });

    // Hover over the link
    await learnFreeLink.hover();

    // Wait for transition
    await page.waitForTimeout(300);

    // Get color after hover
    const hoverColor = await learnFreeLink.evaluate((el) => {
      return window.getComputedStyle(el).color;
    });

    // Color should change on hover (to cyan accent) or have CSS transition defined
    const hasHoverFeedback =
      initialColor !== hoverColor ||
      hoverColor.includes('78, 207, 254'); // cyan color

    expect(hasHoverFeedback).toBe(true);
  });
});
