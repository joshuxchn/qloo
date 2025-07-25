import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Try static export for AWS Amplify
  output: 'export',
  trailingSlash: true,
  poweredByHeader: false,
  // Critical: Disable image optimization for static export
  images: {
    unoptimized: true,
  },
  // Fix potential hydration issues
  reactStrictMode: false,
};

export default nextConfig;
