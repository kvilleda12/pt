'use client';

import { useState, useEffect } from 'react';

interface ActivityItem {
  id: number;
  type: 'session' | 'goal' | 'achievement' | 'reminder';
  title: string;
  description: string;
  time: string;
  icon: string;
  color: string;
}

export function RecentActivity() {
  const [activities, setActivities] = useState<ActivityItem[]>([]);

  useEffect(() => {
    // Simulate loading activities
    const timer = setTimeout(() => {
      setActivities([
        {
          id: 1,
          type: 'session',
          title: 'Morning Workout',
          description: 'Completed 45-minute strength training session',
          time: '2 hours ago',
          icon: '💪',
          color: 'bg-blue-100 text-blue-600'
        },
        {
          id: 2,
          type: 'goal',
          title: 'Weekly Goal Achieved',
          description: 'Reached 5 workout sessions this week',
          time: '1 day ago',
          icon: '🎯',
          color: 'bg-green-100 text-green-600'
        },
        {
          id: 3,
          type: 'achievement',
          title: 'New Personal Record',
          description: 'Set new record for bench press: 185 lbs',
          time: '2 days ago',
          icon: '🏆',
          color: 'bg-yellow-100 text-yellow-600'
        },
        {
          id: 4,
          type: 'reminder',
          title: 'Rest Day Reminder',
          description: 'Remember to take a rest day tomorrow',
          time: '3 days ago',
          icon: '😴',
          color: 'bg-purple-100 text-purple-600'
        },
        {
          id: 5,
          type: 'session',
          title: 'Cardio Session',
          description: 'Completed 30-minute HIIT workout',
          time: '4 days ago',
          icon: '❤️',
          color: 'bg-red-100 text-red-600'
        }
      ]);
    }, 1500);

    return () => clearTimeout(timer);
  }, []);

  if (activities.length === 0) {
    return (
      <div className="space-y-4">
        {[...Array(5)].map((_, i) => (
          <div key={i} className="flex items-start space-x-3">
            <div className="w-8 h-8 bg-gray-200 rounded-full animate-pulse"></div>
            <div className="flex-1 space-y-2">
              <div className="h-4 bg-gray-200 rounded w-3/4 animate-pulse"></div>
              <div className="h-3 bg-gray-200 rounded w-1/2 animate-pulse"></div>
              <div className="h-3 bg-gray-200 rounded w-1/4 animate-pulse"></div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {activities.map((activity, index) => (
        <div key={activity.id} className="flex items-start space-x-4 group">
          {/* Timeline dot */}
          <div className="relative">
            <div className={`relative w-10 h-10 rounded-full flex items-center justify-center text-lg shadow-lg backdrop-blur-sm border border-white/20 ${activity.color}`}>
              {activity.icon}
              {/* Icon glow */}
              <div className="absolute inset-0 rounded-full blur-md opacity-30 bg-gradient-to-br from-white/20 to-transparent"></div>
            </div>
            {index < activities.length - 1 && (
              <div className="absolute top-10 left-1/2 transform -translate-x-1/2 w-0.5 h-8 bg-gradient-to-b from-white/30 to-transparent"></div>
            )}
          </div>
          
          {/* Activity content */}
          <div className="flex-1 min-w-0">
            <div className="flex items-center justify-between">
              <h4 className="text-sm font-semibold text-white group-hover:text-blue-300 transition-colors drop-shadow-sm">
                {activity.title}
              </h4>
              <span className="text-xs text-white/60 bg-white/10 px-2 py-1 rounded-full backdrop-blur-sm">{activity.time}</span>
            </div>
            <p className="text-sm text-white/80 mt-2 leading-relaxed">{activity.description}</p>
          </div>
        </div>
      ))}
      
      {/* View all button */}
      <div className="pt-6 border-t border-white/20">
        <button className="w-full text-sm text-white/90 hover:text-white font-medium transition-colors bg-white/10 hover:bg-white/20 px-4 py-2 rounded-xl backdrop-blur-sm border border-white/20 hover:border-white/30">
          View all activity →
        </button>
      </div>
    </div>
  );
} 