import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'standalone',
  experimental: {
    outputFileTracingRoot: undefined,
  },
  // Optimize for production
  swcMinify: true,
  poweredByHeader: false,
  // Handle trailing slashes
  trailingSlash: false,
};

export default nextConfig;
