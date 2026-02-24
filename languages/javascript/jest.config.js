module.exports = {
  testEnvironment: 'node',
  coverageDirectory: 'coverage',
  collectCoverageFrom: [
    'solutions/**/*.js',
    '!solutions/**/*.test.js',
  ],
  testMatch: [
    '**/tests/**/*.test.js',
  ],
  verbose: true,
};
