'use client';
import { DashboardLayout } from '@/app/components/dashboard/DashboardLayout';
import { useSession } from "next-auth/react"
import { useRouter } from 'next/navigation';

// Fetch user session on the server side and pass down to the rendered client component.
export default function AppLayout({ children }: { children: React.ReactNode }) {
  const { data: session, status } = useSession();
  const { replace } = useRouter();
  if (status === 'unauthenticated') {
    replace('/login');
  }

  const username = session?.user?.name || 'User';
  const email = session?.user?.email || 'n/a';

  return (
    <DashboardLayout username={username} email={email}>
      {children}
    </DashboardLayout>
  )
}