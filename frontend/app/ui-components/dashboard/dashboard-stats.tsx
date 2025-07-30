'use client';

import { useState, useEffect } from 'react';

interface StatCardProps {
  title: string;
  value: string | number;
  change: string;
  isPositive: boolean;
  icon: string;
  color: string;
}

function StatCard({ title, value, change, isPositive, icon, color }: StatCardProps) {
  return (
    <div className="group relative bg-gradient-to-br from-white/10 to-white/5 backdrop-blur-xl rounded-3xl p-6 border border-white/20 shadow-2xl hover:shadow-3xl transition-all duration-500 hover:scale-105 overflow-hidden">
      {/* Animated background gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-white/0 via-white/5 to-white/0 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
      
      {/* Glow effect */}
      <div className="absolute inset-0 rounded-3xl blur-xl opacity-20 bg-gradient-to-br from-blue-400/20 via-purple-400/20 to-pink-400/20"></div>
      
      <div className="relative z-10 flex items-center justify-between">
        <div className="space-y-3">
          <p className="text-white/80 text-sm font-medium tracking-wide uppercase">{title}</p>
          <p className="text-4xl font-bold text-white drop-shadow-lg">{value}</p>
          <div className="flex items-center space-x-2">
            <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-semibold ${
              isPositive 
                ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' 
                : 'bg-red-500/20 text-red-300 border border-red-500/30'
            }`}>
              <span className="mr-1">{isPositive ? '↗' : '↘'}</span>
              {change}
            </span>
            <span className="text-white/60 text-xs">vs last week</span>
          </div>
        </div>
        <div className={`relative w-16 h-16 rounded-2xl flex items-center justify-center text-3xl shadow-lg ${color} backdrop-blur-sm border border-white/20`}>
          {icon}
          {/* Icon glow */}
          <div className="absolute inset-0 rounded-2xl blur-md opacity-30 bg-gradient-to-br from-white/20 to-transparent"></div>
        </div>
      </div>
    </div>
  );
}

export function DashboardStats() {
  const [stats, setStats] = useState([
    {
      title: 'Total Sessions',
      value: '0',
      change: '0%',
      isPositive: true,
      icon: '🏃‍♂️',
      color: 'bg-blue-100 text-blue-600'
    },
    {
      title: 'Active Time',
      value: '0h 0m',
      change: '0%',
      isPositive: true,
      icon: '⏱️',
      color: 'bg-green-100 text-green-600'
    },
    {
      title: 'Progress Score',
      value: '0%',
      change: '0%',
      isPositive: true,
      icon: '📈',
      color: 'bg-purple-100 text-purple-600'
    },
    {
      title: 'Streak Days',
      value: '0',
      change: '0%',
      isPositive: true,
      icon: '🔥',
      color: 'bg-orange-100 text-orange-600'
    }
  ]);

  // Simulate loading stats
  useEffect(() => {
    const timer = setTimeout(() => {
      setStats([
        {
          title: 'Total Sessions',
          value: '24',
          change: '+12%',
          isPositive: true,
          icon: '🏃‍♂️',
          color: 'bg-blue-100 text-blue-600'
        },
        {
          title: 'Active Time',
          value: '18h 32m',
          change: '+8%',
          isPositive: true,
          icon: '⏱️',
          color: 'bg-green-100 text-green-600'
        },
        {
          title: 'Progress Score',
          value: '87%',
          change: '+5%',
          isPositive: true,
          icon: '📈',
          color: 'bg-purple-100 text-purple-600'
        },
        {
          title: 'Streak Days',
          value: '7',
          change: '+2',
          isPositive: true,
          icon: '🔥',
          color: 'bg-orange-100 text-orange-600'
        }
      ]);
    }, 2000);

    return () => clearTimeout(timer);
  }, []);

  return (
    <>
      {stats.map((stat, index) => (
        <StatCard key={index} {...stat} />
      ))}
    </>
  );
} 