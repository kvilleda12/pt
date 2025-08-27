import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/app/components/ui/card"
import { Badge } from "@/app/components/ui/badge"
import { CheckCircle, Clock, Target } from "lucide-react"

interface Session {
  id: string
  date: string
  duration: number
  score: number
  exercisesCompleted: number
  totalExercises: number
  status: 'completed' | 'in-progress' | 'missed'
}

const recentSessions: Session[] = [
  {
    id: '1',
    date: '2 days ago',
    duration: 25,
    score: 92,
    exercisesCompleted: 8,
    totalExercises: 8,
    status: 'completed'
  },
  {
    id: '2',
    date: '5 days ago',
    duration: 18,
    score: 85,
    exercisesCompleted: 6,
    totalExercises: 7,
    status: 'completed'
  },
  {
    id: '3',
    date: '1 week ago',
    duration: 30,
    score: 88,
    exercisesCompleted: 9,
    totalExercises: 9,
    status: 'completed'
  }
]

export function RecentSessions() {
  const getStatusBadge = (status: Session['status']) => {
    switch (status) {
      case 'completed':
        return <Badge variant="secondary" className="bg-success/10 text-success border-success/20">Completed</Badge>
      case 'in-progress':
        return <Badge variant="secondary" className="bg-warning/10 text-warning border-warning/20">In Progress</Badge>
      case 'missed':
        return <Badge variant="destructive">Missed</Badge>
      default:
        return null
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Recent Sessions</CardTitle>
        <CardDescription>Your latest therapy progress</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {recentSessions.map((session) => (
          <div key={session.id} className="flex items-center justify-between p-3 border rounded-lg hover:bg-muted/50 transition-colors">
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <CheckCircle className="h-4 w-4 text-success" />
                <span className="font-medium">{session.date}</span>
                {getStatusBadge(session.status)}
              </div>
              <div className="flex items-center gap-4 text-sm text-muted-foreground">
                <div className="flex items-center gap-1">
                  <Clock className="h-3 w-3" />
                  <span>{session.duration} min</span>
                </div>
                <div className="flex items-center gap-1">
                  <Target className="h-3 w-3" />
                  <span>{session.exercisesCompleted}/{session.totalExercises} exercises</span>
                </div>
              </div>
            </div>
            <div className="text-right">
              <div className="text-lg font-bold text-primary">{session.score}%</div>
              <div className="text-xs text-muted-foreground">Score</div>
            </div>
          </div>
        ))}
      </CardContent>
    </Card>
  )
}