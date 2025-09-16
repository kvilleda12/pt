'use client';
import { DashboardLayout } from "@/app/components/dashboard/DashboardLayout"
import { BeginSessionCard } from "@/app/components/dashboard/BeginSessionCard"
import { AnalyticsCard } from "@/app/components/dashboard/AnalyticsCard"
import { RecentSessions } from "@/app/components/dashboard/RecentSessions"
import "@/app/globals.css"
import { getUserSession } from '@/app/services/actions';
import GradientText from '@/app/components/reactbits/GradientText'


type Session = Awaited<ReturnType<typeof getUserSession>>;

export default function DashboardLayoutPage({ session }: { session: Session }) {
  const username = session?.user?.name || 'User';
  const email = session?.user?.email || 'n/a';

  return (
    <DashboardLayout username={username} email={email}>
      <div className="space-y-8 max-w-7xl mx-auto px-4">
        {/* Header */}
        <div className="text-center">
          <GradientText
            colors={["#40ffaa", "#4079ff", "#40ffaa", "#4079ff", "#40ffaa"]}
            animationSpeed={7}
            showBorder={false}
            className="text-5xl leading-tight font-bold"
          >
            Welcome back, {username}!
          </GradientText>
          <p className="text-muted-foreground mt-1 text-center py-2">
            Ready to continue your physical therapy journey?
          </p>
        </div>

        {/* Main Dashboard Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 w-full">
          {/* Begin Session - Takes half width on lg+ */}
          <div className="w-full h-full">
            <BeginSessionCard />
          </div>

          {/* Analytics - Takes half width on lg+ */}
          <div className="w-full h-full">
            <AnalyticsCard />
          </div>
        </div>

        {/* Recent Sessions */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 justify-items-center">
          <div className="lg:col-span-2 w-full">
            <RecentSessions />
          </div>

          {/* Future components */}
          <div className="lg:col-span-1 w-full max-w-md">
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
