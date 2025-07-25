import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // AWS Amplify compatibility fixes
  trailingSlash: false,
  poweredByHeader: false,
  // Critical: Disable image optimization for Amplify
  images: {
    unoptimized: true,
  },
  // Ensure static files are properly handled
  assetPrefix: undefined,
  // Fix potential hydration issues
  reactStrictMode: false,
};

export default nextConfig;
