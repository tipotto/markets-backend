module.exports = {
  root: true,
  env: {
    es2020: true,
    node: true,
  },
  extends: ['eslint:recommended', 'plugin:node/recommended'],
  plugins: ['json-format'],
  settings: {
    'json/sort-package-json': 'standard',
    'json/json-with-comments-files': ['.vscode/**'],
  },
  rules: {
    'spaced-comment': [
      'error',
      'always',
      {
        markers: ['/ <reference'],
      },
    ],
    'node/exports-style': ['error', 'module.exports'],
    'node/no-deprecated-api': 'error',
    'node/no-missing-require': 'error',
    'node/no-unsupported-features': 'error',
    'no-unused-vars': 'off',
    'no-console': 'error',
  },
};
