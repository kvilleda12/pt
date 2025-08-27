'use client';
import styles from './dashboard.module.css';
import { DashboardLayout } from "@/app/components/dashboard/DashboardLayout"
import { BeginSessionCard } from "@/app/components/dashboard/BeginSessionCard"
import { AnalyticsCard } from "@/app/components/dashboard/AnalyticsCard"
import { RecentSessions } from "@/app/components/dashboard/RecentSessions"

export default function DashboardPage() {

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Welcome Header */}
        <div>
          <h1 className="text-3xl font-bold">Welcome back, John!</h1>
          <p className="text-muted-foreground mt-1">
            Ready to continue your physical therapy journey?
          </p>
        </div>

        {/* Main Dashboard Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Begin Session - Takes full width on mobile, left column on lg+ */}
          <div className="lg:col-span-1">
            <BeginSessionCard />
          </div>

          {/* Analytics - Takes remaining space */}
          <div className="lg:col-span-2">
            <AnalyticsCard />
          </div>
        </div>

        {/* Recent Sessions */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            <RecentSessions />
          </div>

          {/* Additional space for future components */}
          <div className="lg:col-span-1">
            {/* Future: Quick actions, tips, or notifications */}
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
