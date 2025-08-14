'use client';
import { useState } from 'react';
import styles from './dashboard.module.css';
import { Chart } from '@/app/components/dashboard/Chart'


export default function DashboardPage() {

  return (
    <div className={styles.dashboardContainer}>
      <Chart/>
    </div>
  );
}
