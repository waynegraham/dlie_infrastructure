
import NextAuth from "next-auth"
import GoogleProvider from "next-auth/providers/google"

// No `export const authOptions`—we pass options directly into NextAuth
const handler = NextAuth({
  // You can also add `pages: { signIn: '/auth/signin' }` etc. here
  providers: [
    GoogleProvider({
      clientId:     process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
  ],
  secret: process.env.NEXTAUTH_SECRET,
  session: {
    strategy: "jwt",
  },
})

export { handler as GET, handler as POST }