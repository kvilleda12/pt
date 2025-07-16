import "../globals.css";
import Navbar from "@/app/ui-components/navbar";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
      <div >
        <Navbar />
        {children}
      </div>
  );
}
