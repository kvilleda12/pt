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
      <Card className="col-span-2">
        <CardHeader>
          <CardTitle>Analytics Overview</CardTitle>
          <CardDescription>Your therapy progress summary</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="space-y-2">
                <div className="h-4 bg-muted rounded animate-pulse" />
                <div className="h-8 bg-muted rounded animate-pulse" />
                <div className="h-3 bg-muted rounded animate-pulse w-2/3" />
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
    <Card className="col-span-2">
      <CardHeader>
        <CardTitle>Analytics Overview</CardTitle>
        <CardDescription>Your therapy progress summary</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          {metrics.map((metric, index) => {
            const Icon = metric.icon
            return (
              <div key={metric.label} className="space-y-2">
                <div className="flex items-center gap-2">
                  <Icon className={`h-4 w-4 ${metric.color}`} />
                  <span className="text-sm text-muted-foreground">
                    {metric.label}
                  </span>
                </div>
                <div className={`text-2xl font-bold ${metric.isGoal ? 'text-sm font-medium' : ''}`}>
                  {metric.value}
                </div>
                {!metric.isGoal && (
                  <div className="text-xs text-muted-foreground">
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
