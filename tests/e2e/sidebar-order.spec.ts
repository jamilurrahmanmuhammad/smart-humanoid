import { test, expect } from '@playwright/test';

/**
 * Sidebar Navigation Order E2E Tests - Feature 007
 *
 * TDD RED Phase: These tests validate that Module 1 sidebar displays chapters
 * in the correct sequential order: Ch1 variants → Ch2 variants → Ch3 variants.
 *
 * Expected sidebar order (by sidebar_position):
 * 1. Module 1 index (position 1)
 * 2. Chapter 1 Explorer (position 2)
 * 3. Chapter 1 Builder (position 3)
 * 4. Chapter 1 Engineer (position 4)
 * 5. Chapter 2 Explorer (position 5)
 * 6. Chapter 2 Builder (position 6)
 * 7. Chapter 2 Engineer (position 7)
 * 8. Chapter 3 Explorer (position 8)
 * 9. Chapter 3 Builder (position 9)
 * 10. Chapter 3 Engineer (position 10)
 */

test.describe('Sidebar Navigation Order - Feature 007', () => {
  // T001: Verify Module 1 sidebar displays chapters in correct sequential order
  test('should display chapters in correct order: Ch1 → Ch2 → Ch3', async ({ page }) => {
    // Navigate to docs intro page
    await page.goto('docs/intro', { waitUntil: 'networkidle' });

    // Get sidebar navigation
    const sidebar = page.getByRole('navigation', { name: /docs sidebar/i });
    await expect(sidebar).toBeVisible();

    // Click on Module 1 to expand it and navigate to its content
    const module1Link = sidebar.getByText('Module 1: The Robotic Nervous System');
    await expect(module1Link).toBeVisible();
    await module1Link.click();

    // Wait for navigation to complete
    await page.waitForURL(/module-1-robotic-nervous-system/);

    // Get all links in the sidebar
    const sidebarLinks = sidebar.locator('a');

    // Get all link texts in order
    const linkTexts = await sidebarLinks.allTextContents();

    // Extract chapter numbers from the link texts
    // Sidebar uses "Ch 1: Physical AI" for Ch1 and "Chapter 2/3: ..." for Ch2/Ch3
    const chapterSequence: number[] = [];
    for (const text of linkTexts) {
      if (text.includes('Ch 1:') || text.includes('Chapter 1:')) {
        chapterSequence.push(1);
      } else if (text.includes('Chapter 2:')) {
        chapterSequence.push(2);
      } else if (text.includes('Chapter 3:')) {
        chapterSequence.push(3);
      }
    }

    // Verify no interleaving: chapter numbers should only increase or stay the same
    let lastChapter = 0;
    for (const chapterNum of chapterSequence) {
      // Chapter number should only increase or stay the same, never decrease
      expect(chapterNum).toBeGreaterThanOrEqual(lastChapter);
      lastChapter = chapterNum;
    }

    // Verify we have all 9 chapter variants (3 chapters × 3 variants)
    expect(chapterSequence.length).toBeGreaterThanOrEqual(9);
  });

  // Verify Chapter 1 variants are consecutive
  test('should display all Chapter 1 variants before Chapter 2', async ({ page }) => {
    await page.goto('docs/intro', { waitUntil: 'networkidle' });

    const sidebar = page.getByRole('navigation', { name: /docs sidebar/i });
    await expect(sidebar).toBeVisible();

    // Click on Module 1 to expand it
    const module1Link = sidebar.getByText('Module 1: The Robotic Nervous System');
    await module1Link.click();
    await page.waitForURL(/module-1-robotic-nervous-system/);

    const sidebarLinks = sidebar.locator('a');
    const linkTexts = await sidebarLinks.allTextContents();

    // Find positions of chapter markers
    let foundChapter2 = false;
    let chapter1AfterChapter2 = false;

    for (const text of linkTexts) {
      if (text.includes('Chapter 2:')) {
        foundChapter2 = true;
      }
      if (foundChapter2 && (text.includes('Ch 1:') || text.includes('Chapter 1:'))) {
        chapter1AfterChapter2 = true;
        break;
      }
    }

    // No Chapter 1 content should appear after Chapter 2 content
    expect(chapter1AfterChapter2).toBe(false);
  });

  // Verify Chapter 2 variants are consecutive
  test('should display all Chapter 2 variants before Chapter 3', async ({ page }) => {
    await page.goto('docs/intro', { waitUntil: 'networkidle' });

    const sidebar = page.getByRole('navigation', { name: /docs sidebar/i });
    await expect(sidebar).toBeVisible();

    // Click on Module 1 to expand it
    const module1Link = sidebar.getByText('Module 1: The Robotic Nervous System');
    await module1Link.click();
    await page.waitForURL(/module-1-robotic-nervous-system/);

    const sidebarLinks = sidebar.locator('a');
    const linkTexts = await sidebarLinks.allTextContents();

    // Find positions of chapter markers
    let foundChapter3 = false;
    let chapter2AfterChapter3 = false;

    for (const text of linkTexts) {
      if (text.includes('Chapter 3:')) {
        foundChapter3 = true;
      }
      if (foundChapter3 && text.includes('Chapter 2:')) {
        chapter2AfterChapter3 = true;
        break;
      }
    }

    // No Chapter 2 content should appear after Chapter 3 content
    expect(chapter2AfterChapter3).toBe(false);
  });

  // Verify each chapter has exactly 3 variants (Explorer, Builder, Engineer)
  test('should have exactly 3 variants per chapter', async ({ page }) => {
    await page.goto('docs/intro', { waitUntil: 'networkidle' });

    const sidebar = page.getByRole('navigation', { name: /docs sidebar/i });
    await expect(sidebar).toBeVisible();

    // Click on Module 1 to expand it
    const module1Link = sidebar.getByText('Module 1: The Robotic Nervous System');
    await module1Link.click();
    await page.waitForURL(/module-1-robotic-nervous-system/);

    const sidebarLinks = sidebar.locator('a');
    const linkTexts = await sidebarLinks.allTextContents();

    // Count variants per chapter
    // Chapter 1 uses "Ch 1:" format, Chapter 2/3 use "Chapter X:" format
    let chapter1Count = 0;
    let chapter2Count = 0;
    let chapter3Count = 0;

    for (const text of linkTexts) {
      if (text.includes('Ch 1:') || text.includes('Chapter 1:')) {
        chapter1Count++;
      }
      if (text.includes('Chapter 2:')) {
        chapter2Count++;
      }
      if (text.includes('Chapter 3:')) {
        chapter3Count++;
      }
    }

    // Each chapter should have 3 variants
    expect(chapter1Count).toBe(3);
    expect(chapter2Count).toBe(3);
    expect(chapter3Count).toBe(3);
  });
});
