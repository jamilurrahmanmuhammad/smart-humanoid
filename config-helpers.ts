/**
 * Configuration Helpers for Docusaurus Environment Variables
 *
 * This module provides validation and configuration functions for
 * SITE_URL and BASE_URL environment variables, plus CI environment detection.
 */

/**
 * Detect if running in a CI/CD environment.
 *
 * Uses the industry-standard CI=true environment variable which is set
 * automatically by virtually all CI/CD platforms including:
 * - GitHub Actions
 * - GitLab CI
 * - CircleCI
 * - Travis CI
 * - Jenkins
 * - Vercel
 * - Netlify
 * - Cloudflare Pages
 *
 * @returns true if CI environment variable is set to 'true' (case-insensitive)
 */
export function isCI(): boolean {
  const ciValue = process.env.CI;
  if (!ciValue) {
    return false;
  }
  return ciValue.toLowerCase() === 'true';
}

/**
 * Validate and return the site URL.
 * @param url - The URL to validate
 * @returns The validated URL
 * @throws Error if URL doesn't start with http:// or https://
 */
export function validateUrl(url: string): string {
  if (!url.startsWith('http://') && !url.startsWith('https://')) {
    throw new Error('Invalid SITE_URL: must start with http:// or https://');
  }
  return url;
}

/**
 * Validate and normalize the base URL.
 * @param baseUrl - The base URL to validate
 * @returns The validated and normalized base URL (with trailing slash)
 * @throws Error if base URL doesn't start with /
 */
export function validateBaseUrl(baseUrl: string): string {
  if (!baseUrl.startsWith('/')) {
    throw new Error('Invalid BASE_URL: must start with /');
  }
  // Normalize to have trailing slash (unless it's just "/")
  if (baseUrl !== '/' && !baseUrl.endsWith('/')) {
    return `${baseUrl}/`;
  }
  return baseUrl;
}

/**
 * Configuration interface for Docusaurus URL settings
 */
export interface UrlConfig {
  url: string;
  baseUrl: string;
}

/**
 * Get configuration from environment variables with defaults.
 * @returns Configuration object with url and baseUrl
 */
export function getConfig(): UrlConfig {
  const rawUrl = process.env.SITE_URL || 'http://localhost:3000';
  const rawBaseUrl = process.env.BASE_URL || '/';

  return {
    url: validateUrl(rawUrl),
    baseUrl: validateBaseUrl(rawBaseUrl),
  };
}
