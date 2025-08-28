import { Play, Clock, Zap, Target } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/app/components/ui/card"
import { Button } from "@/app/components/ui/button"
import { Badge } from "@/app/components/ui/badge"

export function BeginSessionCard() {
  const handleBeginSession = () => {
    // TODO: Navigate to session or start session logic
    console.log("Starting new therapy session...")
  }

  return (
    <Card className="relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-subtle opacity-50" />
      <CardHeader className="relative">
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="text-xl">Ready for Your Session?</CardTitle>
            <CardDescription className="mt-2">
              Start your personalized AI-guided therapy session
            </CardDescription>
          </div>
          <Badge variant="secondary" className="bg-primary/10 text-primary border-primary/20">
            <Zap className="h-3 w-3 mr-1" />
            AI Powered
          </Badge>
        </div>
      </CardHeader>
      <CardContent className="relative space-y-4">
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div className="flex items-center gap-2 text-muted-foreground">
            <Clock className="h-4 w-4" />
            <span>15-30 min session</span>
          </div>
          <div className="flex items-center gap-2 text-muted-foreground">
            <Target className="h-4 w-4" />
            <span>Personalized exercises</span>
          </div>
        </div>
        
        <Button 
          variant="hero" 
          size="xl" 
          className="w-full" 
          onClick={handleBeginSession}
        >
          <Play className="h-5 w-5 mr-2" />
          Begin Session
        </Button>
        
        <p className="text-xs text-center text-muted-foreground">
          Your last session was 2 days ago. Let's continue your progress!
        </p>
      </CardContent>
    </Card>
  )
}
