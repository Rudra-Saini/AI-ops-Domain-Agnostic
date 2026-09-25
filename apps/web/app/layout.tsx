import React from "react";

export const metadata = {
  title: "AIOps Developer Cockpit & Store",
  description: "Autonomous Self-Healing E-Commerce Platform",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body style={{ margin: 0, fontFamily: "system-ui, -apple-system, sans-serif", backgroundColor: "#0b0f19", color: "#f3f4f6" }}>
        {children}
      </body>
    </html>
  );
}
