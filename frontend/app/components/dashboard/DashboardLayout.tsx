'use client'
import { SidebarProvider, SidebarTrigger, SidebarInset } from "@/app/components/ui/sidebar"
import { DashboardSidebar } from "./DashboardSidebar"
import { ProfileDropdown } from "./ProfileDropdown"

interface DashboardLayoutProps {
  username: string,
  email: string,
  children: React.ReactNode
}

export function DashboardLayout({ username, email, children }: DashboardLayoutProps) {
  return (
    <SidebarProvider>
      <div className="min-h-screen flex w-full">
        <DashboardSidebar />
        <SidebarInset className="flex flex-col md:peer-data-[state=expanded]:pl-4 lg:peer-data-[state=expanded]:pl-6">
          {/* Header */}
          <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
            <div className="flex h-14 items-center justify-between px-6">
              <div className="flex items-center gap-4">
                <SidebarTrigger />
              </div>
              <ProfileDropdown username={username} email={email} />
            </div>
          </header>
          
          {/* Main Content */}
          <main className="flex-1 p-6">
            {children}
          </main>
        </SidebarInset>
      </div>
    </SidebarProvider>
  )
}