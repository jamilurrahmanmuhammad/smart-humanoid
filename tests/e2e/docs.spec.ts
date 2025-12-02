import { test, expect } from '@playwright/test';

/**
 * Documentation Structure E2E Tests - User Story 3
 *
 * Tests for the pre-configured documentation folder structure.
 * Following TDD: These tests are written FIRST and must FAIL before implementation.
 */

test.describe('Documentation Structure - User Story 3', () => {
  // T052: /docs route loads intro page successfully
  test('should load intro page at /docs route', async ({ page }) => {
    // Navigate to docs intro page and wait for load
    const response = await page.goto('docs/intro', { waitUntil: 'networkidle' });

    // Check response status
    expect(response?.status()).toBe(200);

    // Page should load successfully
    await expect(page).toHaveURL(/\/docs\/intro/);

    // Should have a heading
    const heading = page.getByRole('heading', { level: 1 });
    await expect(heading).toBeVisible();
  });

  // T053: Sidebar displays with auto-generated hierarchy
  test('should display sidebar with navigation hierarchy', async ({ page }) => {
    await page.goto('docs/intro');

    // Sidebar should be visible (Docusaurus uses nav with "Docs sidebar" aria-label)
    const sidebar = page.getByRole('navigation', { name: /docs sidebar/i });
    await expect(sidebar).toBeVisible();

    // Should have navigation links
    const navLinks = sidebar.locator('a');
    const linkCount = await navLinks.count();
    expect(linkCount).toBeGreaterThan(0);
  });

  // T054: Sidebar shows all 4 module categories (hierarchical structure)
  test('should display all 4 module categories in sidebar', async ({ page }) => {
    await page.goto('docs/intro');

    const sidebar = page.getByRole('navigation', { name: /docs sidebar/i });

    // Verify all 4 modules are visible in sidebar
    await expect(sidebar.getByText('Module 1: The Robotic Nervous System')).toBeVisible();
    await expect(sidebar.getByText('Module 2: Digital Twin Technology')).toBeVisible();
    await expect(sidebar.getByText('Module 3: AI Robot Brain')).toBeVisible();
    await expect(sidebar.getByText('Module 4: Vision-Language-Action')).toBeVisible();
  });

  // T055: Module links navigate to module landing pages
  test('should navigate to module landing page when clicking module', async ({ page }) => {
    await page.goto('docs/intro');

    const sidebar = page.getByRole('navigation', { name: /docs sidebar/i });

    // Click on Module 1 and verify navigation
    await sidebar.getByText('Module 1: The Robotic Nervous System').click();
    await expect(page).toHaveURL(/module-1-robotic-nervous-system/);

    // Verify module landing page content
    const heading = page.getByRole('heading', { level: 1 });
    await expect(heading).toContainText('Module 1');
  });
});
