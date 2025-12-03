/**
 * Build Configuration Tests
 *
 * TDD tests for verifying build output configuration
 * follows Docusaurus defaults for zero-config deployment.
 */

import * as fs from 'fs';
import * as path from 'path';

describe('Build Configuration (US1: One-Click Repository Import)', () => {
  // T011 [P] [US1] - Build output directory is build/ (Docusaurus default)
  describe('Build output directory', () => {
    it('should have docusaurus.config.ts that does not override output directory', () => {
      // Docusaurus default output is 'build/'
      // We verify the config doesn't override this
      const configPath = path.resolve(__dirname, '../../docusaurus.config.ts');
      expect(fs.existsSync(configPath)).toBe(true);

      const configContent = fs.readFileSync(configPath, 'utf-8');
      // Should NOT have custom outDir that differs from default
      // If outDir is specified, it should be 'build'
      if (configContent.includes('outDir')) {
        expect(configContent).toMatch(/outDir\s*:\s*['"]build['"]/);
      }
      // If no outDir specified, Docusaurus uses 'build/' by default - this is fine
    });

    it('should use Docusaurus default build directory (build/)', () => {
      // Verify by checking that no custom output directory is configured
      // that would break platform auto-detection
      const configPath = path.resolve(__dirname, '../../docusaurus.config.ts');
      const configContent = fs.readFileSync(configPath, 'utf-8');

      // Common non-standard output directories that would break zero-config
      const nonStandardDirs = ['dist/', 'public/', 'out/', '_site/'];
      for (const dir of nonStandardDirs) {
        const pattern = new RegExp(`outDir\\s*:\\s*['"]${dir.replace('/', '')}['"]`);
        expect(configContent).not.toMatch(pattern);
      }
    });
  });

  describe('Docusaurus configuration file exists', () => {
    it('should have docusaurus.config.ts file', () => {
      const configPath = path.resolve(__dirname, '../../docusaurus.config.ts');
      expect(fs.existsSync(configPath)).toBe(true);
    });
  });
});
