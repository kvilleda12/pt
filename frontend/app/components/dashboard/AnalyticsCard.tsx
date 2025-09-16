import { useEffect, useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/app/components/ui/card"
import { TrendingUp, TrendingDown, Activity, Clock, Target, Award } from "lucide-react"

interface AnalyticsData {
  sessionsCompleted: number
  totalMinutes: number
  averageScore: number
  streakDays: number
  improvementRate: number
  nextGoal: string
}

// Mock API call
const fetchAnalyticsData = async (): Promise<AnalyticsData> => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 1000))
  
  return {
    sessionsCompleted: 12,
    totalMinutes: 180,
    averageScore: 87,
    streakDays: 5,
    improvementRate: 15.2,
    nextGoal: "Complete 15 sessions this month"
  }
}

export function AnalyticsCard() {
  const [data, setData] = useState<AnalyticsData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchAnalyticsData().then(result => {
      setData(result)
      setLoading(false)
    })
  }, [])

  if (loading) {
    return (
      <Card className="relative overflow-hidden group hover:shadow-xl hover:shadow-blue-100/50 border border-blue-200 hover:border-blue-300 transition-all duration-300 bg-white hover:-translate-y-1 h-full flex flex-col">
        <CardHeader className="p-6">
          <CardTitle className="text-xl text-blue-600">Analytics Overview</CardTitle>
          <CardDescription className="text-blue-600">Your therapy progress summary</CardDescription>
        </CardHeader>
        <CardContent className="p-6 flex-1">
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="space-y-2">
                <div className="h-4 bg-blue-100 rounded animate-pulse" />
                <div className="h-8 bg-blue-100 rounded animate-pulse" />
                <div className="h-3 bg-blue-100 rounded animate-pulse w-2/3" />
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    )
  }

  if (!data) return null

  const metrics = [
    {
      label: "Sessions Completed",
      value: data.sessionsCompleted,
      icon: Activity,
      color: "text-primary",
    },
    {
      label: "Total Minutes",
      value: data.totalMinutes,
      icon: Clock,
      color: "text-primary",
    },
    {
      label: "Average Score",
      value: `${data.averageScore}%`,
      icon: Target,
      color: "text-success",
    },
    {
      label: "Current Streak",
      value: `${data.streakDays} days`,
      icon: Award,
      color: "text-warning",
    },
    {
      label: "Improvement",
      value: `+${data.improvementRate}%`,
      icon: TrendingUp,
      color: "text-success",
    },
    {
      label: "Next Goal",
      value: data.nextGoal,
      icon: Target,
      color: "text-muted-foreground",
      isGoal: true,
    },
  ]

  return (
    <Card className="relative overflow-hidden group hover:shadow-xl hover:shadow-blue-100/50 border border-blue-200 hover:border-blue-300 transition-all duration-300 bg-white hover:-translate-y-1 h-full flex flex-col">
      <CardHeader className="p-6">
        <CardTitle className="text-xl text-blue-600">Analytics Overview</CardTitle>
        <CardDescription className="text-blue-600">Your therapy progress summary</CardDescription>
      </CardHeader>
      <CardContent className="p-6 flex-1">
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          {metrics.map((metric, index) => {
            const Icon = metric.icon
            return (
              <div key={metric.label} className="space-y-2 p-3 rounded-lg hover:bg-blue-50/50 transition-colors duration-200">
                <div className="flex items-center gap-2">
                  <Icon className="h-4 w-4 text-blue-600" />
                  <span className="text-sm text-blue-600">
                    {metric.label}
                  </span>
                </div>
                <div className={`text-2xl font-bold text-blue-600 ${metric.isGoal ? 'text-sm font-medium' : ''}`}>
                  {metric.value}
                </div>
                {!metric.isGoal && (
                  <div className="text-xs text-blue-500">
                    This month
                  </div>
                )}
              </div>
            )
          })}
        </div>
      </CardContent>
    </Card>
  )
}
