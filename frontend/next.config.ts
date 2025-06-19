import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  reactStrictMode: true,
  eslint: {
    // WARNING: this will let *all* lint errors pass during `next build`
    ignoreDuringBuilds: true,
  },
};

export default nextConfig;
