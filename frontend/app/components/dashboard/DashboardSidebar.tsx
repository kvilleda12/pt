import { 
  Activity, 
  BarChart3, 
  Calendar, 
  FileText, 
  Home, 
  Settings, 
  User,
  Zap
} from "lucide-react"
import Link from "next/link";

import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/app/components/ui/sidebar"

import { usePathname } from "next/navigation";

const mainItems = [
  { title: "Dashboard", url: "/", icon: Home },
  { title: "Sessions", url: "/sessions", icon: Activity },
  { title: "Analytics", url: "/analytics", icon: BarChart3 },
  { title: "Calendar", url: "/calendar", icon: Calendar },
  { title: "Reports", url: "/reports", icon: FileText },
]

const settingsItems = [
  { title: "Profile", url: "/profile", icon: User },
  { title: "Settings", url: "/settings", icon: Settings },
]

export function DashboardSidebar() {
  const currentPath = usePathname();

  const isActive = (path: string) => currentPath === path
  const getNavCls = ({ isActive }: { isActive: boolean }) =>
    isActive ? "bg-accent text-accent-foreground font-medium" : "hover:bg-muted/50"

  return (
    <Sidebar className="text-blue-600 border-r border-blue-100 [--sidebar-width:18rem]">
      <SidebarContent className="p-0">
        {/* Header */}
        <div className="p-6 border-b border-blue-100">
          <Link href="/" className="flex items-center gap-4 hover:opacity-80 transition-opacity duration-200 cursor-pointer">
            <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-3 shadow-lg">
              <Zap className="h-7 w-7 text-white" />
            </div>
            <div>
              <h2 className="font-bold text-xl text-blue-600">PTI</h2>
              <p className="text-sm text-blue-500 font-medium">Physical Therapy Intelligence</p>
            </div>
          </Link>
        </div>

        {/* Main Navigation */}
        <div className="flex-1 p-4">
          <SidebarGroup className="mb-8">
            <SidebarGroupLabel className="text-blue-600 font-semibold text-sm uppercase tracking-wider mb-4 px-2">Main</SidebarGroupLabel>
            <SidebarGroupContent>
              <SidebarMenu className="space-y-2">
                {mainItems.map((item) => (
                  <SidebarMenuItem key={item.title}>
                    <SidebarMenuButton asChild className="h-12 px-4 rounded-xl hover:bg-blue-50 hover:text-blue-700 transition-all duration-200 group">
                      <Link href={item.url} className="flex items-center gap-3 w-full">
                        <item.icon className="h-5 w-5 text-blue-600 group-hover:text-blue-700" />
                        <span className="text-blue-600 font-medium group-hover:text-blue-700">{item.title}</span>
                      </Link>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                ))}
              </SidebarMenu>
            </SidebarGroupContent>
          </SidebarGroup>

          {/* Settings Navigation */}
          <SidebarGroup>
            <SidebarGroupLabel className="text-blue-600 font-semibold text-sm uppercase tracking-wider mb-4 px-2">Account</SidebarGroupLabel>
            <SidebarGroupContent>
              <SidebarMenu className="space-y-2">
                {settingsItems.map((item) => (
                  <SidebarMenuItem key={item.title}>
                    <SidebarMenuButton asChild className="h-12 px-4 rounded-xl hover:bg-blue-50 hover:text-blue-700 transition-all duration-200 group">
                      <Link href={item.url} className="flex items-center gap-3 w-full">
                        <item.icon className="h-5 w-5 text-blue-600 group-hover:text-blue-700" />
                        <span className="text-blue-600 font-medium group-hover:text-blue-700">{item.title}</span>
                      </Link>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                ))}
              </SidebarMenu>
            </SidebarGroupContent>
          </SidebarGroup>
        </div>
      </SidebarContent>
    </Sidebar>
  )
}