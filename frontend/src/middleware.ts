import { withAuth } from 'next-auth/middleware'

export default withAuth(
  function middleware(req) {
    // ここで追加のミドルウェア処理を行うことができます
  },
  {
    callbacks: {
      authorized: ({ token }) => !!token
    },
  }
)

export const config = {
  matcher: ['/dashboard/:path*', '/profile/:path*']
} 