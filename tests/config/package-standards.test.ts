/**
 * Package.json Standards Tests
 *
 * TDD tests for verifying package.json follows industry standards
 * for zero-config platform deployment.
 */

import * as fs from 'fs';
import * as path from 'path';

describe('Package.json Standards (US4: Framework Configuration Discovery)', () => {
  let packageJson: {
    engines?: { node?: string };
    scripts?: { build?: string; start?: string };
  };

  beforeAll(() => {
    const packagePath = path.resolve(__dirname, '../../package.json');
    const packageContent = fs.readFileSync(packagePath, 'utf-8');
    packageJson = JSON.parse(packageContent);
  });

  // T006 [P] [US4] - package.json has engines.node >= 20
  describe('engines.node field', () => {
    it('should have engines field defined', () => {
      expect(packageJson.engines).toBeDefined();
    });

    it('should have engines.node field defined', () => {
      expect(packageJson.engines?.node).toBeDefined();
    });

    it('should specify Node.js version >= 20', () => {
      const nodeVersion = packageJson.engines?.node;
      expect(nodeVersion).toBeDefined();
      // Should contain "20" or higher in the version specification
      // Common patterns: ">=20.0", ">=20", "^20", "20.x"
      expect(nodeVersion).toMatch(/20|21|22/);
    });
  });

  // T007 [P] [US4] - package.json has scripts.build = "docusaurus build"
  describe('scripts.build field', () => {
    it('should have scripts field defined', () => {
      expect(packageJson.scripts).toBeDefined();
    });

    it('should have scripts.build field defined', () => {
      expect(packageJson.scripts?.build).toBeDefined();
    });

    it('should have build script set to "docusaurus build"', () => {
      expect(packageJson.scripts?.build).toBe('docusaurus build');
    });
  });

  // T008 [P] [US4] - package.json has scripts.start = "docusaurus start"
  describe('scripts.start field', () => {
    it('should have scripts.start field defined', () => {
      expect(packageJson.scripts?.start).toBeDefined();
    });

    it('should have start script set to "docusaurus start"', () => {
      expect(packageJson.scripts?.start).toBe('docusaurus start');
    });
  });
});
