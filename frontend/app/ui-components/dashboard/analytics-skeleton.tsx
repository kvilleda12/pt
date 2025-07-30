'use client';

import { useState, useEffect } from 'react';

interface ChartData {
  labels: string[];
  datasets: {
    label: string;
    data: number[];
    borderColor: string;
    backgroundColor: string;
    tension: number;
  }[];
}

export function AnalyticsSkeleton() {
  const [isLoading, setIsLoading] = useState(true);
  const [chartData, setChartData] = useState<ChartData | null>(null);

  useEffect(() => {
    // Simulate loading analytics data
    const timer = setTimeout(() => {
      setChartData({
        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        datasets: [
          {
            label: 'Workout Duration',
            data: [45, 60, 30, 75, 50, 90, 40],
            borderColor: 'rgb(59, 130, 246)',
            backgroundColor: 'rgba(59, 130, 246, 0.1)',
            tension: 0.4
          },
          {
            label: 'Calories Burned',
            data: [300, 400, 200, 500, 350, 600, 280],
            borderColor: 'rgb(34, 197, 94)',
            backgroundColor: 'rgba(34, 197, 94, 0.1)',
            tension: 0.4
          }
        ]
      });
      setIsLoading(false);
    }, 2500);

    return () => clearTimeout(timer);
  }, []);

  if (isLoading) {
    return (
      <div className="space-y-6">
        {/* Chart skeleton */}
        <div className="bg-gray-100 rounded-xl p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="h-6 bg-gray-200 rounded w-1/3 animate-pulse"></div>
            <div className="h-4 bg-gray-200 rounded w-1/4 animate-pulse"></div>
          </div>
          
          {/* Chart area skeleton */}
          <div className="h-64 bg-gray-200 rounded-lg animate-pulse relative">
            <div className="absolute inset-0 flex items-end justify-between px-4 pb-4">
              {[...Array(7)].map((_, i) => (
                <div key={i} className="w-8 bg-gray-300 rounded-t animate-pulse" style={{ height: `${Math.random() * 60 + 20}%` }}></div>
              ))}
            </div>
          </div>
          
          {/* Legend skeleton */}
          <div className="flex items-center space-x-4 mt-4">
            {[...Array(2)].map((_, i) => (
              <div key={i} className="flex items-center space-x-2">
                <div className="w-4 h-4 bg-gray-200 rounded animate-pulse"></div>
                <div className="h-4 bg-gray-200 rounded w-16 animate-pulse"></div>
              </div>
            ))}
          </div>
        </div>

        {/* Metrics skeleton */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="bg-gray-100 rounded-xl p-4">
              <div className="h-4 bg-gray-200 rounded w-1/2 animate-pulse mb-2"></div>
              <div className="h-8 bg-gray-200 rounded w-1/3 animate-pulse"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Chart */}
      <div className="relative bg-gradient-to-br from-white/10 to-white/5 backdrop-blur-xl rounded-3xl p-6 border border-white/20 shadow-2xl overflow-hidden">
        {/* Glow effect */}
        <div className="absolute inset-0 rounded-3xl blur-xl opacity-20 bg-gradient-to-br from-blue-400/20 via-purple-400/20 to-pink-400/20"></div>
        
        <div className="relative z-10">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-xl font-bold text-white drop-shadow-lg">Weekly Progress</h3>
            <span className="text-white/70 text-sm bg-white/10 px-3 py-1 rounded-full backdrop-blur-sm">Last 7 days</span>
          </div>
          
          {/* Simple chart visualization */}
          <div className="h-64 relative">
            <div className="absolute inset-0 flex items-end justify-between px-4 pb-4">
              {chartData?.datasets[0].data.map((value, index) => (
                <div key={index} className="flex flex-col items-center space-y-3">
                  <div 
                    className="w-10 bg-gradient-to-t from-blue-500 to-blue-400 rounded-t-lg transition-all duration-700 shadow-lg hover:shadow-blue-500/50"
                    style={{ height: `${(value / 90) * 100}%` }}
                  ></div>
                  <span className="text-xs text-white/80 font-medium">{chartData.labels[index]}</span>
                </div>
              ))}
            </div>
          </div>
          
          {/* Legend */}
          <div className="flex items-center space-x-6 mt-6">
            <div className="flex items-center space-x-2">
              <div className="w-4 h-4 bg-gradient-to-r from-blue-500 to-blue-400 rounded shadow-lg"></div>
              <span className="text-sm text-white/90 font-medium">Workout Duration (min)</span>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-4 h-4 bg-gradient-to-r from-emerald-500 to-emerald-400 rounded shadow-lg"></div>
              <span className="text-sm text-white/90 font-medium">Calories Burned</span>
            </div>
          </div>
        </div>
      </div>

      {/* Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="relative bg-gradient-to-br from-white/10 to-white/5 backdrop-blur-xl rounded-2xl p-5 border border-white/20 shadow-xl hover:shadow-2xl transition-all duration-300 hover:scale-105 overflow-hidden">
          <div className="absolute inset-0 rounded-2xl blur-xl opacity-20 bg-gradient-to-br from-blue-400/20 to-purple-400/20"></div>
          <div className="relative z-10">
            <p className="text-sm text-white/70 font-medium">Average Duration</p>
            <p className="text-3xl font-bold text-white drop-shadow-lg">52 min</p>
          </div>
        </div>
        <div className="relative bg-gradient-to-br from-white/10 to-white/5 backdrop-blur-xl rounded-2xl p-5 border border-white/20 shadow-xl hover:shadow-2xl transition-all duration-300 hover:scale-105 overflow-hidden">
          <div className="absolute inset-0 rounded-2xl blur-xl opacity-20 bg-gradient-to-br from-emerald-400/20 to-blue-400/20"></div>
          <div className="relative z-10">
            <p className="text-sm text-white/70 font-medium">Total Calories</p>
            <p className="text-3xl font-bold text-white drop-shadow-lg">2,630</p>
          </div>
        </div>
        <div className="relative bg-gradient-to-br from-white/10 to-white/5 backdrop-blur-xl rounded-2xl p-5 border border-white/20 shadow-xl hover:shadow-2xl transition-all duration-300 hover:scale-105 overflow-hidden">
          <div className="absolute inset-0 rounded-2xl blur-xl opacity-20 bg-gradient-to-br from-purple-400/20 to-pink-400/20"></div>
          <div className="relative z-10">
            <p className="text-sm text-white/70 font-medium">Sessions This Week</p>
            <p className="text-3xl font-bold text-white drop-shadow-lg">7</p>
          </div>
        </div>
      </div>
    </div>
  );
} 