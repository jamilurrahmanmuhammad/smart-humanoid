/** @type {import('ts-jest').JestConfigWithTsJest} */
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  testMatch: ['**/tests/config/**/*.test.ts'],
  moduleFileExtensions: ['ts', 'js'],
  clearMocks: true,
  collectCoverageFrom: ['<rootDir>/config-helpers.ts'],
  coverageDirectory: 'coverage',
  verbose: true,
};
