/**
 * CI Detection Tests
 *
 * TDD tests for CI environment detection functionality.
 * Tests verify that the isCI() function correctly detects CI/CD environments
 * using the industry-standard CI=true environment variable.
 */

import { isCI } from '../../config-helpers';

describe('CI Detection (US2: Environment Auto-Detection)', () => {
  // Store original env values
  const originalEnv = process.env;

  beforeEach(() => {
    // Reset env before each test
    jest.resetModules();
    process.env = { ...originalEnv };
    delete process.env.CI;
  });

  afterAll(() => {
    // Restore original env
    process.env = originalEnv;
  });

  // T003 [P] [US2] - isCI() returns true when CI=true
  describe('isCI() returns true when CI=true', () => {
    it('should return true when CI environment variable is set to "true"', () => {
      process.env.CI = 'true';
      expect(isCI()).toBe(true);
    });

    it('should return true when CI is set to "TRUE" (case insensitive)', () => {
      process.env.CI = 'TRUE';
      expect(isCI()).toBe(true);
    });

    it('should return true when CI is set to "True"', () => {
      process.env.CI = 'True';
      expect(isCI()).toBe(true);
    });
  });

  // T004 [P] [US2] - isCI() returns false when CI not set
  describe('isCI() returns false when CI not set', () => {
    it('should return false when CI environment variable is not set', () => {
      delete process.env.CI;
      expect(isCI()).toBe(false);
    });

    it('should return false when CI is undefined', () => {
      process.env.CI = undefined as unknown as string;
      expect(isCI()).toBe(false);
    });
  });

  // T005 [P] [US2] - isCI() returns false when CI=false
  describe('isCI() returns false when CI=false', () => {
    it('should return false when CI is set to "false"', () => {
      process.env.CI = 'false';
      expect(isCI()).toBe(false);
    });

    it('should return false when CI is set to empty string', () => {
      process.env.CI = '';
      expect(isCI()).toBe(false);
    });

    it('should return false when CI is set to "0"', () => {
      process.env.CI = '0';
      expect(isCI()).toBe(false);
    });
  });

  // T010 [P] [US3] - Config works with no CI var set (local mode)
  describe('Local mode without CI variable', () => {
    it('should work in local mode when CI is not set', () => {
      delete process.env.CI;
      expect(() => isCI()).not.toThrow();
      expect(isCI()).toBe(false);
    });
  });
});
