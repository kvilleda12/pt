'use server';
import { redirect } from 'next/navigation';
import DashboardClientPage from './DashboardLayout'; // We will create this next
import { auth } from '@/auth';

export default async function DashboardPage() {
  let session;
  try {
    session = await auth();
  } catch (err) {
    console.error('Error fetching user session:', err);
    return null;
  }

  if (!session?.user) {
    redirect('/login');
  }

  return <DashboardClientPage session={session} />;
}