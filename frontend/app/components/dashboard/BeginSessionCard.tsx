import { Play, Clock, Zap, Target } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/app/components/ui/card"
import { Button } from "@/app/components/ui/button"
import { Badge } from "@/app/components/ui/badge"
import Link from "next/link"


export function BeginSessionCard() {
  return (
    <Card className="relative overflow-hidden group hover:shadow-xl hover:shadow-blue-100/50 border border-blue-200 hover:border-blue-300 transition-all duration-300 bg-white hover:-translate-y-1 h-full flex flex-col">
      <CardHeader className="relative p-8">
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="text-3xl font-bold text-blue-500 mb-3">Ready for Your Session?</CardTitle>
            <CardDescription className="text-lg text-blue-600">
              Start your personalized AI-guided therapy session
            </CardDescription>
          </div>
          <Badge variant="secondary" className="bg-blue-100 text-blue-600 border-blue-200 shadow-sm text-sm px-5 py-2">
            <Zap className="h-4 w-4 mr-2" />
            AI Powered
          </Badge>
        </div>
      </CardHeader>
      <CardContent className="relative p-8 flex-1 flex flex-col justify-center">

        <Link href="/session" className="block">
          <Button 
            variant="hero" 
            size="xl" 
            className="w-full h-16 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:scale-[1.02] active:scale-[0.98] text-2xl font-bold rounded-2xl"
          >
            <Play className="h-8 w-8 mr-3" />
            Begin Session
          </Button>
        </Link>

      </CardContent>
    </Card>
  )
}
