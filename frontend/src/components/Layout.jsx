import { Outlet, useLocation } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import Header from './header/Header'
import { LogOut } from 'lucide-react'
import { useLanguage } from '../context/LanguageContext'

export default function Layout() {
  const location = useLocation()
  const { user, logout } = useAuthStore()
  const { t } = useLanguage()

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-300">
      {/* New Header */}
      <Header />

      {/* User Info Bar - Hidden on home page */}
      {location.pathname !== '/' && user && (
        <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm border-b border-gray-200 dark:border-gray-700 sticky top-20 z-40">
          <div className="container mx-auto px-4 py-2">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                {user?.full_name || user?.username}
              </span>
              <button
                onClick={logout}
                className="flex items-center gap-2 px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-lg transition-colors text-sm font-medium"
              >
                <LogOut size={16} />
                <span>{t('common.logout')}</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Main Content */}
      <main className={`${location.pathname === '/' ? 'p-0' : 'p-6'}`}>
        <Outlet />
      </main>
    </div>
  )
}
