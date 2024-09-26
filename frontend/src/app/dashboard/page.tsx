"use client"

import { useEffect } from "react"
import { signOut } from "next-auth/react";
import { useSession } from "next-auth/react";
import { useRouter } from "next/navigation";  
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { LogOut } from "lucide-react"


export default function Component() {
  const { data: session, status } = useSession();
  const router = useRouter();
  

  // Redirect effect
  useEffect(() => {
    if (status === "unauthenticated") {
      router.push("/auth");
    }
  }, [status, router]);

  if (status === "loading") {
    return <p>Loading...</p>;
  }
  return (
    <div className="flex flex-col h-screen">
      <header className="flex items-center justify-between px-6 py-4 bg-primary text-primary-foreground">
        <h1 className="text-2xl font-bold">Library Management Dashboard</h1>
        <Input 
          className="w-1/3 bg-primary-foreground text-primary" 
          placeholder="Search..." 
          type="search"
        />
        <LogoutButton />
      </header>
      <main className="flex-grow p-6 bg-muted/40 overflow-auto">
        
      </main>
    </div>
  )
}



const LogoutButton = () => {
  const router = useRouter();

  const handleLogout = async () => {
    const confirmation = window.confirm("Are you sure you want to log out?");
    
    if (confirmation) {
      await signOut({
        redirect: false, 
      });
      router.push("/auth/signin");
    }
  };

  return (
    <Button onClick={handleLogout}>
      <LogOut className="mr-2 h-4 w-4" /> Logout
    </Button>
  );
};

