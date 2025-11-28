import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/:path*",          // Frontend path
        destination: "http://localhost:8000/api/:path*", // Backend path
      },
    ];
  },
};

export default nextConfig;
