import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  experimental: {
    optimizePackageImports: ["react-icons"],
  },
  images: {
    localPatterns: [
      { pathname: "/gemuese/**" },
      { pathname: "/officesupplies/**" },
      { pathname: "/fruits/**" },
      { pathname: "/grains/**" },
      { pathname: "/img/**" },
    ],
  },
};

export default nextConfig;
