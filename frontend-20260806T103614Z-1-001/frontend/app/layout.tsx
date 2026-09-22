import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "TokyIA - Assistente de Dados Corporativo",
  description: "Seu assistente virtual de inteligência artificial para dados corporativos.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR">
      <body className={`${inter.className} bg-tokyBg bg-toky-pattern bg-[length:150%_150%] animate-wave-pan bg-no-repeat bg-fixed text-white antialiased`}>
        {children}
      </body>
    </html>
  );
}
