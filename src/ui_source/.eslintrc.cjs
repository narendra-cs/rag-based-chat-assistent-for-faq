module.exports = {
  root: true,
  env: {
    browser: true,
    es2021: true,
    node: true,
  },
  extends: [
    'eslint:recommended',
    'plugin:react/recommended',
    'plugin:react-hooks/recommended',
    'plugin:react/jsx-runtime',
  ],
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: 'latest',
    sourceType: 'module',
  },
  plugins: ['react', 'react-hooks', 'react-refresh'],
  settings: {
    react: {
      version: 'detect',
    },
  },
  rules: {
    // General rules
    'no-unused-vars': ['warn', { argsIgnorePattern: '^_' }],
    'no-console': 'warn',
    'no-debugger': 'warn',
    'prefer-const': 'error',
    'no-var': 'error',
    'object-shorthand': 'warn',
    'quote-props': ['warn', 'as-needed'],
    'no-extra-semi': 'warn',
    'prefer-arrow-callback': 'warn',
    'no-undef': 'error',

    // React rules
    'react/prop-types': 'off', // If using TypeScript, you might want to enable this
    'react/react-in-jsx-scope': 'off', // Not needed with new JSX transform
    'react/jsx-uses-react': 'off', // Not needed with new JSX transform
    'react/no-unescaped-entities': ['error', { forbid: ['>', '}'] }],
    'react/self-closing-comp': 'warn',
    'react/jsx-sort-props': ['warn', {
      callbacksLast: true,
      shorthandFirst: true,
      reservedFirst: true,
    }],

    // React Hooks rules
    'react-hooks/rules-of-hooks': 'error',
    'react-hooks/exhaustive-deps': 'warn',

    // React Refresh
    'react-refresh/only-export-components': [
      'warn',
      { allowConstantExport: true },
    ],
  },
  overrides: [
    {
      files: ['*.js', '*.jsx'],
      rules: {
        // Add any JavaScript-specific rules here
      },
    },
  ],
};
