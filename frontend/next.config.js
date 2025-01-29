/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  transpilePackages: ["@adalace/react"],
  webpack: (config, { isServer }) => {
    // Add resolve.symlinks configuration
    config.resolve.symlinks = true;
    return config;
  },
};

module.exports = nextConfig;
