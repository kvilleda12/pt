'use client';

import { useState } from 'react';
import { StartSessionButton } from '@/app/ui-components/dashboard/start-session-button';
import { AnalyticsSkeleton } from '@/app/ui-components/dashboard/analytics-skeleton';
import { WelcomeMessage } from '@/app/ui-components/dashboard/welcome-message';
import { DashboardStats } from '@/app/ui-components/dashboard/dashboard-stats';
import { RecentActivity } from '@/app/ui-components/dashboard/recent-activity';
import styles from './dashboard.module.css';

export default function DashboardPage() {
  const [isSessionActive, setIsSessionActive] = useState(false);

  const handleSessionStart = () => {
    setIsSessionActive(true);
    // Here you would typically start the actual session
    console.log('Session started!');
  };

  const handleSessionEnd = () => {
    setIsSessionActive(false);
    // Here you would typically end the session
    console.log('Session ended!');
  };

  return (
    <div className={styles.dashboardContainer}>
      {/* Header Section */}
      <div className={styles.header}>
        <WelcomeMessage />
        <StartSessionButton 
          isActive={isSessionActive}
          onStart={handleSessionStart}
          onEnd={handleSessionEnd}
        />
      </div>

      {/* Stats Cards */}
      <div className={styles.statsGrid}>
        <DashboardStats />
      </div>

      {/* Main Content Grid */}
      <div className={styles.contentGrid}>
        {/* Analytics Section */}
        <div className={styles.analyticsSection}>
          <h2 className={styles.sectionTitle}>Analytics Overview</h2>
          <AnalyticsSkeleton />
        </div>

        {/* Recent Activity */}
        <div className={styles.activitySection}>
          <h2 className={styles.sectionTitle}>Recent Activity</h2>
          <RecentActivity />
        </div>
      </div>
    </div>
  );
}
