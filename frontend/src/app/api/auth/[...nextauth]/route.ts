import NextAuth from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";
import axios from "axios";
import qs from "qs";
import { signOut } from "next-auth/react";
import { User } from "next-auth";

export const authOptions = {
    providers: [
      CredentialsProvider({
        name: "Credentials",
        credentials: {
          username: { label: "Username", type: "text" },
          password: { label: "Password", type: "password" },
        },
        async authorize(credentials): Promise<User | null> {
          try {
            const res = await axios.post(
              `${process.env.BACKEND_URL}/token`,
              qs.stringify({
                username: credentials?.username,
                password: credentials?.password,
              }),
              {
                headers: {
                  "Content-Type": "application/x-www-form-urlencoded",
                },
              }
            );
  
            if (res.data.access_token) {
              return { id: credentials!.username };
            } else {
              console.log("Invalid credentials");
              throw new Error("Invalid credentials");
            }
          } catch (error) {
            console.error("Error in authorize:", error);
            // Return null for any other errors (e.g., network issues)
            return null;
          }
        },
      }),
    ],
    secret: process.env.NEXTAUTH_SECRET,
    session: {
      strategy: "jwt",
      maxAge: 24 * 60 * 60,
    } as { strategy: "jwt"; maxAge: number },
    pages: {
      signIn: "dashboard",
      signOut: "auth",
    },
  };

const handler = NextAuth(authOptions);
export { handler as GET, handler as POST };
