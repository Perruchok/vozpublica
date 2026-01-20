/** @type {import('next').NextConfig} */
const path = require('path');

const nextConfig = {
  reactStrictMode: false, // Disable for better compatibility with development
  
  // Webpack configuration for path aliases
  webpack: (config) => {
    config.resolve.alias = {
      ...config.resolve.alias,
      '@': path.resolve(__dirname),
    };
    return config;
  },
  
  // Environment variables - use NEXT_PUBLIC_API_URL if set, otherwise localhost
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  },
};

module.exports = nextConfig;
