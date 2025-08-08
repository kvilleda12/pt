// start/layout.tsx
import { BodyPartProvider } from "@/app/contexts/BodyPartContext";

export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div>
            <BodyPartProvider>
                {children}
            </BodyPartProvider>
        </div>
    );
}