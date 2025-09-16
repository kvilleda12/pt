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
    <Card className="relative overflow-hidden group hover:shadow-xl hover:shadow-blue-100/50 border border-blue-200 hover:border-blue-300 transition-all duration-300 bg-white hover:-translate-y-1">
      <CardHeader className="p-6">
        <CardTitle className="text-xl text-blue-600">Recent Sessions</CardTitle>
        <CardDescription className="text-blue-600">Your latest therapy progress</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4 p-6">
        {recentSessions.map((session) => (
          <div key={session.id} className="flex items-center justify-between p-4 border border-blue-100 rounded-lg hover:bg-blue-50/50 hover:border-blue-200 transition-all duration-200">
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <CheckCircle className="h-4 w-4 text-blue-600" />
                <span className="font-medium text-blue-600">{session.date}</span>
                {getStatusBadge(session.status)}
              </div>
              <div className="flex items-center gap-4 text-sm text-blue-500">
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
              <div className="text-lg font-bold text-blue-600">{session.score}%</div>
              <div className="text-xs text-blue-500">Score</div>
            </div>
          </div>
        ))}
      </CardContent>
    </Card>
  )
}