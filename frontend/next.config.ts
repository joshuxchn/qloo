import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Simplified config for AWS Amplify
  trailingSlash: false,
  poweredByHeader: false,
  // Ensure proper image optimization for Amplify
  images: {
    unoptimized: false,
  },
};

export default nextConfig;
