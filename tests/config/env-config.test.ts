/**
 * Environment Configuration Tests
 *
 * TDD tests for Docusaurus environment variable configuration.
 * These tests verify that SITE_URL and BASE_URL environment variables
 * are properly read and validated.
 */

import {
  getConfig,
  validateUrl,
  validateBaseUrl,
} from '../../config-helpers';

describe('Environment Configuration', () => {
  // Store original env values
  const originalEnv = process.env;

  beforeEach(() => {
    // Reset env before each test
    jest.resetModules();
    process.env = { ...originalEnv };
    delete process.env.SITE_URL;
    delete process.env.BASE_URL;
  });

  afterAll(() => {
    // Restore original env
    process.env = originalEnv;
  });

  // T004 [US1] - Default SITE_URL when env var not set
  describe('SITE_URL defaults', () => {
    it('should use http://localhost:3000 as default when SITE_URL is not set', () => {
      const config = getConfig();
      expect(config.url).toBe('http://localhost:3000');
    });
  });

  // T005 [US2] - Default BASE_URL when env var not set
  describe('BASE_URL defaults', () => {
    it('should use / as default when BASE_URL is not set', () => {
      const config = getConfig();
      expect(config.baseUrl).toBe('/');
    });
  });

  // T006 [US1] - SITE_URL env var overrides default
  describe('SITE_URL override', () => {
    it('should use SITE_URL env var value when set', () => {
      process.env.SITE_URL = 'https://docs.example.com';
      const config = getConfig();
      expect(config.url).toBe('https://docs.example.com');
    });
  });

  // T007 [US2] - BASE_URL env var overrides default
  describe('BASE_URL override', () => {
    it('should use BASE_URL env var value when set', () => {
      process.env.BASE_URL = '/docs/';
      const config = getConfig();
      expect(config.baseUrl).toBe('/docs/');
    });
  });

  // T008 [US1] - SITE_URL without protocol throws error
  describe('SITE_URL validation', () => {
    it('should throw error when SITE_URL does not start with http:// or https://', () => {
      expect(() => validateUrl('example.com')).toThrow(
        'Invalid SITE_URL: must start with http:// or https://'
      );
    });

    it('should accept valid http:// URL', () => {
      expect(validateUrl('http://localhost:3000')).toBe('http://localhost:3000');
    });

    it('should accept valid https:// URL', () => {
      expect(validateUrl('https://docs.example.com')).toBe('https://docs.example.com');
    });
  });

  // T009 [US2] - BASE_URL without leading slash throws error
  describe('BASE_URL validation - leading slash', () => {
    it('should throw error when BASE_URL does not start with /', () => {
      expect(() => validateBaseUrl('docs/')).toThrow(
        'Invalid BASE_URL: must start with /'
      );
    });

    it('should accept BASE_URL starting with /', () => {
      expect(validateBaseUrl('/docs/')).toBe('/docs/');
    });
  });

  // T010 [US2] - BASE_URL trailing slash normalization
  describe('BASE_URL validation - trailing slash', () => {
    it('should normalize BASE_URL to have trailing slash', () => {
      expect(validateBaseUrl('/docs')).toBe('/docs/');
    });

    it('should keep existing trailing slash', () => {
      expect(validateBaseUrl('/docs/')).toBe('/docs/');
    });

    it('should handle root path correctly', () => {
      expect(validateBaseUrl('/')).toBe('/');
    });
  });

  // T011 [US4] - Config loads without any env vars set
  describe('Local development defaults', () => {
    it('should load config without errors when no env vars are set', () => {
      expect(() => getConfig()).not.toThrow();
    });

    it('should return valid url and baseUrl when no env vars are set', () => {
      const config = getConfig();
      expect(config.url).toBeDefined();
      expect(config.baseUrl).toBeDefined();
      expect(typeof config.url).toBe('string');
      expect(typeof config.baseUrl).toBe('string');
    });
  });

  // T012 [US4] - Integration test placeholder for npm start
  describe('Development server compatibility', () => {
    it('should return defaults compatible with dev server', () => {
      const config = getConfig();
      // Dev server should work with localhost URL and root base path
      expect(config.url).toContain('localhost');
      expect(config.baseUrl).toBe('/');
    });
  });
});
