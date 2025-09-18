// start/layout.tsx
import { BodyPartProvider } from "@/app/utils/BodyPartContext";
import { auth } from "@/auth";
import { redirect } from "next/navigation";

export default async function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    const session = await auth();
    const email = session?.user?.email;

    if (!email) {
        // this shouldn't happen due to the path being restricted, but just in case
        redirect("/login");
    }

    // POST request to check if user is already set up, redirect to /dashboard if so
    const response = await fetch(`${process.env.API_URL}/is-user-setup`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${email}`,
        },
        body: JSON.stringify({ email }),
    });

    if (response.status === 404) {
        console.error("User not found, redirecting to /");
        redirect("/");
    } else if ((await response.json()).is_setup) {
        console.log("User is already set up, redirecting to /app/dashboard");
        redirect("/app/dashboard");
    }

    return (
        <div>
            <BodyPartProvider>{children}</BodyPartProvider>
        </div>
    );
}
