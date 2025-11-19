import { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { User, Settings, LogOut, Sprout } from 'lucide-react'
import { useAuthStore } from '../../store/authStore'
import { useLanguage } from '../../context/LanguageContext'
import { useNavigate } from 'react-router-dom'

export default function ProfileMenu() {
  const [isOpen, setIsOpen] = useState(false)
  const menuRef = useRef(null)
  const { user, logout } = useAuthStore()
  const navigate = useNavigate()

  // Close menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setIsOpen(false)
      }
    }

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside)
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [isOpen])

  const handleLogout = () => {
    logout()
    navigate('/login')
    setIsOpen(false)
  }

  const { t } = useLanguage()

  const menuItems = [
    {
      icon: User,
      label: t('header.profile.myProfile'),
      onClick: () => {
        setIsOpen(false)
        navigate('/profile')
      }
    },
    {
      icon: Sprout,
      label: t('header.profile.myFarms'),
      onClick: () => {
        setIsOpen(false)
        navigate('/dashboard')
      }
    },
    {
      icon: Settings,
      label: t('header.profile.settings'),
      onClick: () => {
        setIsOpen(false)
        navigate('/settings')
      }
    },
    {
      icon: LogOut,
      label: t('header.profile.logout'),
      onClick: handleLogout,
      isDanger: true
    }
  ]

  // Get user initials for avatar
  const getInitials = () => {
    if (user?.full_name) {
      return user.full_name
        .split(' ')
        .map(n => n[0])
        .join('')
        .toUpperCase()
        .slice(0, 2)
    }
    if (user?.username) {
      return user.username.slice(0, 2).toUpperCase()
    }
    return 'U'
  }

  return (
    <div className="relative" ref={menuRef}>
      {/* Profile Avatar Button */}
      <motion.button
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={() => setIsOpen(!isOpen)}
        className="relative w-10 h-10 rounded-full bg-gradient-to-br from-green-500 to-emerald-600 flex items-center justify-center shadow-md hover:shadow-lg transition-all duration-300 border-2 border-white dark:border-gray-800"
      >
        {user?.profile_picture ? (
          <img
            src={user.profile_picture}
            alt={user.full_name || user.username}
            className="w-full h-full rounded-full object-cover"
          />
        ) : (
          <span className="text-white font-semibold text-sm">
            {getInitials()}
          </span>
        )}
        
        {/* Active Indicator */}
        <motion.div
          className="absolute -bottom-0.5 -right-0.5 w-3 h-3 bg-green-500 rounded-full border-2 border-white dark:border-gray-800"
          animate={{ scale: isOpen ? [1, 1.2, 1] : 1 }}
          transition={{ duration: 0.3 }}
        />
      </motion.button>

      {/* Dropdown Menu */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: -10, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -10, scale: 0.95 }}
            transition={{ duration: 0.2 }}
            className="absolute right-0 top-14 w-56 bg-white dark:bg-gray-800 rounded-xl shadow-xl border border-gray-200 dark:border-gray-700 overflow-hidden z-50"
          >
            {/* User Info Header */}
            <div className="px-4 py-3 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/50">
              <p className="text-sm font-semibold text-gray-900 dark:text-white">
                {user?.full_name || user?.username || 'User'}
              </p>
              <p className="text-xs text-gray-500 dark:text-gray-400 truncate">
                {user?.email}
              </p>
            </div>

            {/* Menu Items */}
            <div className="py-2">
              {menuItems.map((item, index) => {
                const Icon = item.icon
                return (
                  <motion.button
                    key={index}
                    whileHover={{ x: 4 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={item.onClick}
                    className={`w-full flex items-center gap-3 px-4 py-2.5 text-left transition-colors ${
                      item.isDanger
                        ? 'text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20'
                        : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700/50'
                    }`}
                  >
                    <Icon size={18} />
                    <span className="text-sm font-medium">
                      {item.label}
                    </span>
                  </motion.button>
                )
              })}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

