"use client"
import {
  Calendar,
  Settings,
  Users,
  FileText,
  DollarSign,
  Bot,
  Phone,
  Headset,
  ChevronDown,
  User2,
  ChevronUp,
  MoreHorizontal,
  LayoutDashboard,
  Clock,
  Briefcase,
} from "lucide-react"
import { usePathname } from "next/navigation"
import Link from "next/link"

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarSeparator,
  useSidebar,
} from "@/components/ui/sidebar"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible"
import { Button } from "@/components/ui/button"

// Define menu items
const mainNavigation = [
  {
    title: "Dashboard",
    href: "/",
    icon: LayoutDashboard,
  },
  {
    title: "Calendar",
    href: "/calendar",
    icon: Calendar,
  },
  {
    title: "Invoices",
    href: "/invoices",
    icon: FileText,
  },
  {
    title: "Customers",
    href: "/customers",
    icon: Users,
  },
  {
    title: "Appointments",
    href: "/appointments",
    icon: Clock,
  },
  {
    title: "Pricing",
    href: "/pricing",
    icon: DollarSign,
  },
]

const aiTools = [
  {
    title: "AI Chat",
    href: "/ai-chat",
    icon: Bot,
  },
  {
    title: "Voice Calls",
    href: "/voice-calls",
    icon: Phone,
  },
  {
    title: "Call Center",
    href: "/call-center",
    icon: Headset,
  },
]

const projectManagement = [
  {
    title: "Project Management",
    href: "/project-management",
    icon: Briefcase,
  },
]

export function AppSidebar() {
  const pathname = usePathname()
  const { state } = useSidebar() // Get sidebar state for conditional rendering

  // Placeholder for user info and Google Sheets status
  const userName = "John Doe" // Replace with actual user data
  const userRole = "Admin" // Replace with actual user data
  const lastLogin = "2025-08-08 10:00 AM" // Replace with actual user data
  const gsheetsConnected = true // Replace with actual status
  const gsheetsClientEmail = "john.doe@example.com" // Replace with actual data
  const gsheetsProjectId = "my-business-suite" // Replace with actual data

  return (
    <Sidebar>
      <SidebarHeader>
        <div className="flex items-center justify-between w-full">
          <div className="flex items-center gap-2">
            <span className="text-xl font-bold">🏢 Business Suite</span>
          </div>
          {state === "expanded" && (
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="icon" className="h-7 w-7">
                  <MoreHorizontal className="h-4 w-4" />
                  <span className="sr-only">More options</span>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-48">
                <DropdownMenuItem>Settings</DropdownMenuItem>
                <DropdownMenuItem>Help</DropdownMenuItem>
                <DropdownMenuItem>Logout</DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          )}
        </div>
        <SidebarSeparator />
        <div className="user-header">
          <h3 className="text-lg font-semibold">👋 Welcome, {userName}!</h3>
          <p className="text-xs text-sidebar-foreground/70">Last login: {lastLogin}</p>
        </div>
      </SidebarHeader>

      <SidebarContent>
        {/* Google Sheets Status */}
        <SidebarGroup>
          <SidebarGroupLabel>📊 Google Sheets Status</SidebarGroupLabel>
          <SidebarGroupContent>
            {gsheetsConnected ? (
              <>
                <p className="text-sm text-green-500 flex items-center gap-1">
                  <span className="text-lg">✅</span> Connected
                </p>
                <p className="text-xs text-sidebar-foreground/70 truncate">📧 {gsheetsClientEmail}</p>
                <p className="text-xs text-sidebar-foreground/70">🏗️ Project: {gsheetsProjectId}</p>
                <div className="flex gap-2 mt-2">
                  <Button variant="outline" size="sm" className="flex-1 bg-transparent">
                    🧪 Test
                  </Button>
                  <Button variant="outline" size="sm" className="flex-1 bg-transparent">
                    🔄 Refresh
                  </Button>
                </div>
              </>
            ) : (
              <p className="text-sm text-orange-500 flex items-center gap-1">
                <span className="text-lg">⚠️</span> Not Configured
              </p>
            )}
          </SidebarGroupContent>
        </SidebarGroup>

        <SidebarSeparator />

        {/* Main Navigation */}
        <SidebarGroup>
          <SidebarGroupLabel>🧭 Navigation</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {mainNavigation.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton asChild isActive={pathname === item.href}>
                    <Link href={item.href}>
                      <item.icon />
                      <span>{item.title}</span>
                    </Link>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>

        <SidebarSeparator />

        {/* AI Tools */}
        <Collapsible defaultOpen className="group/collapsible">
          <SidebarGroup>
            <SidebarGroupLabel asChild>
              <CollapsibleTrigger className="w-full flex items-center justify-between">
                <span>🤖 AI Tools</span>
                <ChevronDown className="ml-auto transition-transform group-data-[state=open]/collapsible:rotate-180" />
              </CollapsibleTrigger>
            </SidebarGroupLabel>
            <CollapsibleContent>
              <SidebarGroupContent>
                <SidebarMenu>
                  {aiTools.map((item) => (
                    <SidebarMenuItem key={item.title}>
                      <SidebarMenuButton asChild isActive={pathname === item.href}>
                        <Link href={item.href}>
                          <item.icon />
                          <span>{item.title}</span>
                        </Link>
                      </SidebarMenuButton>
                    </SidebarMenuItem>
                  ))}
                </SidebarMenu>
              </SidebarGroupContent>
            </CollapsibleContent>
          </SidebarGroup>
        </Collapsible>

        <SidebarSeparator />

        {/* Project Management */}
        <SidebarGroup>
          <SidebarGroupLabel>⚙️ Other Modules</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {projectManagement.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton asChild isActive={pathname === item.href}>
                    <Link href={item.href}>
                      <item.icon />
                      <span>{item.title}</span>
                    </Link>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>

      <SidebarFooter>
        <SidebarSeparator />
        {/* User Account Dropdown */}
        <SidebarMenu>
          <SidebarMenuItem>
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <SidebarMenuButton>
                  <User2 /> {userName}
                  <ChevronUp className="ml-auto" />
                </SidebarMenuButton>
              </DropdownMenuTrigger>
              <DropdownMenuContent side="top" className="w-[--radix-popper-anchor-width]">
                <DropdownMenuItem>
                  <span>Account</span>
                </DropdownMenuItem>
                <DropdownMenuItem>
                  <span>Billing</span>
                </DropdownMenuItem>
                <DropdownMenuItem>
                  <span>Sign out</span>
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </SidebarMenuItem>
        </SidebarMenu>

        {/* Quick Actions */}
        <div className="flex gap-2 p-2">
          <Button variant="outline" className="flex-1 bg-transparent">
            🔄 Refresh App
          </Button>
          <Button variant="outline" className="flex-1 bg-transparent">
            🚪 Logout
          </Button>
        </div>

        {/* Settings Button */}
        <div className="p-2">
          <SidebarMenuButton asChild isActive={pathname === "/settings"}>
            <Link href="/settings">
              <Settings />
              <span>Settings</span>
            </Link>
          </SidebarMenuButton>
        </div>

        <SidebarSeparator />

        {/* Session Info & Footer */}
        <div className="p-2 text-xs text-sidebar-foreground/70">
          <p>👤 User: {userName}</p>
          <p>🎭 Role: {userRole}</p>
          <p>🕐 Login: {lastLogin}</p>
          <div className="mt-4 p-2 bg-sidebar-accent rounded-md border border-sidebar-border">
            <strong>🏢 Business Suite</strong>
            <br />
            <strong>Version:</strong> 2.1.0
            <br />
            <strong>Build:</strong> {new Date().toLocaleDateString()}
            <br />
            <strong>Support:</strong> help@business.com
          </div>
        </div>
      </SidebarFooter>
    </Sidebar>
  )
}
