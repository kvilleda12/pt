import Link from "next/link"
import { User, Settings, LogOut, Bell, HelpCircle } from "lucide-react"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/app/components/ui/dropdown-menu"
import { Avatar, AvatarFallback, AvatarImage } from "@/app/components/ui/avatar"

export function ProfileDropdown({ username, email }: { username: string, email: string }) {

  const getInitals = (name: string) => {
    const names = name.split(' ');
    const initials = names.map(n => n.charAt(0).toUpperCase()).join('');
    return initials.slice(0, 2); // Limit to 2 characters
  }

  const initials = getInitals(username);

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Avatar className="h-8 w-8 cursor-pointer hover:ring-2 hover:ring-primary/20 transition-all">
          <AvatarImage src="/placeholder-user.jpg" alt="Profile" />
          <AvatarFallback className="bg-primary text-primary-foreground text-sm font-medium">
            {initials}
          </AvatarFallback>
        </Avatar>
      </DropdownMenuTrigger>
      <DropdownMenuContent className="w-56 bg-white text-blue-600" align="end">
        <DropdownMenuLabel>
          <div className="flex flex-col space-y-1">
            <p className="text-sm font-medium leading-none text-blue-700">{username}</p>
            <p className="text-xs leading-none text-blue-400">
              {email}
            </p>
          </div>
        </DropdownMenuLabel>
        <DropdownMenuSeparator />
        <DropdownMenuItem asChild className="text-blue-600 hover:bg-blue-50">
          <Link href="/profile">
            <User className="mr-2 h-4 w-4 text-blue-600" />
            <span>Profile</span>
          </Link>
        </DropdownMenuItem>
        <DropdownMenuItem asChild className="text-blue-600 hover:bg-blue-50">
          <Link href="/settings">
            <Settings className="mr-2 h-4 w-4 text-blue-600" />
            <span>Settings</span>
          </Link>
        </DropdownMenuItem>
        <DropdownMenuItem asChild className="text-blue-600 hover:bg-blue-50">
          <Link href="/notifications">
            <Bell className="mr-2 h-4 w-4 text-blue-600" />
            <span>Notifications</span>
          </Link>
        </DropdownMenuItem>
        <DropdownMenuItem asChild className="text-blue-600 hover:bg-blue-50">
          <Link href="/help">
            <HelpCircle className="mr-2 h-4 w-4 text-blue-600" />
            <span>Help & Support</span>
          </Link>
        </DropdownMenuItem>
        <DropdownMenuSeparator />
        <DropdownMenuItem asChild className="text-red-600 hover:bg-red-50">
          <Link href="/logout">
            <LogOut className="mr-2 h-4 w-4 text-red-600" />
            <span>Log out</span>
          </Link>
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}