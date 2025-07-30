'use client';

import { useState, useEffect } from 'react';

export function WelcomeMessage() {
  const [greeting, setGreeting] = useState('');
  const [timeOfDay, setTimeOfDay] = useState('');
  const [userName, setUserName] = useState('User');

  useEffect(() => {
    // Get current time to determine greeting
    const now = new Date();
    const hour = now.getHours();
    
    let timeGreeting = '';
    if (hour < 12) {
      timeGreeting = 'Good morning';
      setTimeOfDay('morning');
    } else if (hour < 17) {
      timeGreeting = 'Good afternoon';
      setTimeOfDay('afternoon');
    } else {
      timeGreeting = 'Good evening';
      setTimeOfDay('evening');
    }
    
    setGreeting(timeGreeting);
    
    // Simulate loading user data
    const timer = setTimeout(() => {
      setUserName('Alex'); // This would come from user context/auth
    }, 1000);

    return () => clearTimeout(timer);
  }, []);

  const getMotivationalMessage = () => {
    const messages = {
      morning: [
        "Ready to crush your fitness goals today? 💪",
        "Time to start your day with energy and purpose! 🌅",
        "Let's make today your best workout yet! 🔥"
      ],
      afternoon: [
        "Keep up the great work! You're doing amazing! 🎯",
        "Perfect time for a midday energy boost! ⚡",
        "Your consistency is inspiring! Keep going! 💯"
      ],
      evening: [
        "Great job today! Time to wind down and recover! 😌",
        "You've earned your rest! Tomorrow will be even better! 🌙",
        "Another day of progress in the books! 📚"
      ]
    };

    const timeMessages = messages[timeOfDay as keyof typeof messages] || messages.morning;
    return timeMessages[Math.floor(Math.random() * timeMessages.length)];
  };

  return (
    <div className="space-y-2">
      <div className="flex items-center space-x-3">
        <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white text-xl font-bold shadow-lg">
          {userName.charAt(0).toUpperCase()}
        </div>
        <div>
          <h1 className="text-3xl font-bold text-white drop-shadow-lg">
            {greeting}, {userName}!
          </h1>
          <p className="text-white/90 text-lg font-medium">
            {getMotivationalMessage()}
          </p>
        </div>
      </div>
      
      {/* Quick stats preview */}
      <div className="flex items-center space-x-6 mt-4">
        <div className="flex items-center space-x-2 text-white/80">
          <span className="text-lg">🔥</span>
          <span className="text-sm font-medium">7 day streak</span>
        </div>
        <div className="flex items-center space-x-2 text-white/80">
          <span className="text-lg">📊</span>
          <span className="text-sm font-medium">87% weekly goal</span>
        </div>
        <div className="flex items-center space-x-2 text-white/80">
          <span className="text-lg">🎯</span>
          <span className="text-sm font-medium">3 goals active</span>
        </div>
      </div>
    </div>
  );
} 