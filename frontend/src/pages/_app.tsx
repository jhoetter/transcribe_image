import * as React from "react";
import { initAdalace } from "@adalace/react";
import type { AppProps } from "next/app";
import { ThemeProvider } from "next-themes";
import "@/styles/globals.css";

initAdalace(React as any);

export default function App({ Component, pageProps }: AppProps) {
  return (
    <ThemeProvider attribute="class" enableSystem={true} defaultTheme="system">
      <Component {...pageProps} />
    </ThemeProvider>
  );
}
