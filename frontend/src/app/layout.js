import { Montserrat } from "next/font/google";
import "./global.css";
import Navbar from "@/components/navbar";
import { AuthProvider  } from "@/components/AuthContext";

const montserrat = Montserrat({
  variable: "--font-montserrat",
  subsets: ["latin"],
  weight: ['400', '500', '600', '700', '800'],
});

export const metadata = {
  title: "Heater - Sports Prediction Competition Without the Risk",
  description: "Test your sports knowledge and compete with friends through free predictions. Join leagues, track your performance, and prove you know ball - no gambling required.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={`${montserrat.variable} antialiased`} style={{ fontFamily: 'var(--font-montserrat)' }}>
        <AuthProvider>
          <Navbar />
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}