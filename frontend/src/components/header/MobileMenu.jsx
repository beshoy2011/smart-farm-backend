import { motion, AnimatePresence } from 'framer-motion'
import { Link, useLocation } from 'react-router-dom'
import { X } from 'lucide-react'
import { useEffect } from 'react'
import { 
  Brain, 
  Droplets, 
  Sprout, 
  Bug, 
  BarChart3 
} from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'
import LanguageToggle from './LanguageToggle'
import ThemeToggle from './ThemeToggle'
import ProfileMenu from './ProfileMenu'

const navItems = [
  {
    path: '/ai-plant-analysis',
    translationKey: 'header.nav.aiPlantAnalysis',
    icon: Brain,
    gradient: 'from-purple-500 to-pink-500'
  },
  {
    path: '/smart-water-optimization',
    translationKey: 'header.nav.smartWaterOptimization',
    icon: Droplets,
    gradient: 'from-blue-500 to-cyan-500'
  },
  {
    path: '/soil-health-detection',
    translationKey: 'header.nav.soilHealthDetection',
    icon: Sprout,
    gradient: 'from-green-500 to-emerald-500'
  },
  {
    path: '/fertilizer-pest-diagnosis',
    translationKey: 'header.nav.fertilizerPestDiagnosis',
    icon: Bug,
    gradient: 'from-orange-500 to-red-500'
  },
  {
    path: '/dashboard',
    translationKey: 'header.nav.dashboard',
    icon: BarChart3,
    gradient: 'from-indigo-500 to-purple-500'
  }
]

export default function MobileMenu({ isOpen, onClose }) {
  const location = useLocation()
  const { language, t } = useLanguage()

  // Close menu on route change
  useEffect(() => {
    if (isOpen) {
      onClose()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [location.pathname])

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40 lg:hidden"
          />

          {/* Menu Drawer */}
          <motion.div
            initial={{ x: language === 'ar' ? '-100%' : '100%' }}
            animate={{ x: 0 }}
            exit={{ x: language === 'ar' ? '-100%' : '100%' }}
            transition={{ type: 'spring', damping: 25, stiffness: 200 }}
            className="fixed top-0 right-0 h-full w-80 max-w-[85vw] bg-white dark:bg-gray-900 shadow-2xl z-50 lg:hidden flex flex-col"
            style={{ direction: language === 'ar' ? 'rtl' : 'ltr' }}
          >
            {/* Header */}
            <div className="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700">
              <h2 className="text-xl font-bold text-gray-900 dark:text-white">
                {t('header.menu')}
              </h2>
              <motion.button
                whileHover={{ rotate: 90 }}
                whileTap={{ scale: 0.9 }}
                onClick={onClose}
                className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
              >
                <X size={24} className="text-gray-700 dark:text-gray-300" />
              </motion.button>
            </div>

            {/* Navigation Items */}
            <nav className="flex-1 overflow-y-auto p-4 space-y-2">
              {navItems.map((item, index) => {
                const Icon = item.icon
                const isActive = location.pathname === item.path

                return (
                  <motion.div
                    key={item.path}
                    initial={{ opacity: 0, x: language === 'ar' ? -20 : 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                  >
                    <Link
                      to={item.path}
                      onClick={onClose}
                      className={`group relative flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 ${
                        isActive
                          ? 'bg-gradient-to-r ' + item.gradient + ' text-white shadow-md'
                          : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
                      }`}
                    >
                      <Icon size={20} />
                      <span className="font-medium text-[15px]">
                        {t(item.translationKey)}
                      </span>
                    </Link>
                  </motion.div>
                )
              })}
            </nav>

            {/* Actions Section */}
            <div className="mt-auto p-6 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/50">
              <div className="flex items-center justify-center gap-3">
                <LanguageToggle />
                <ThemeToggle />
                <ProfileMenu />
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}
