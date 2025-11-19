import { useState, useEffect } from 'react'
import { motion, useScroll, useMotionValueEvent } from 'framer-motion'
import { Link, useLocation } from 'react-router-dom'
import { Menu } from 'lucide-react'
import NavLinks from './NavLinks'
import LanguageToggle from './LanguageToggle'
import ThemeToggle from './ThemeToggle'
import ProfileMenu from './ProfileMenu'
import MobileMenu from './MobileMenu'
import { useLanguage } from '../../context/LanguageContext'

export default function Header() {
  const [isScrolled, setIsScrolled] = useState(false)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [scrollProgress, setScrollProgress] = useState(0)
  const { scrollY } = useScroll()
  const { t } = useLanguage()
  const location = useLocation()

  useMotionValueEvent(scrollY, 'change', (latest) => {
    setIsScrolled(latest > 20)
    const maxScroll = document.documentElement.scrollHeight - window.innerHeight
    setScrollProgress(Math.min(latest / maxScroll || 0, 1))
  })

  // Close mobile menu on route change
  useEffect(() => {
    setMobileMenuOpen(false)
  }, [location.pathname])

  return (
    <>
      <motion.header
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        transition={{ duration: 0.5, type: 'spring' }}
        className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
          isScrolled
            ? 'bg-white/80 dark:bg-neutral-900/80 backdrop-blur-md shadow-sm border-b border-gray-200/50 dark:border-gray-700/50'
            : 'bg-white/70 dark:bg-neutral-900/50 backdrop-blur-md'
        }`}
      >
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between h-20">
            {/* Logo Section */}
            <motion.div
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="flex items-center gap-3"
            >
              <Link to="/" className="flex items-center gap-3 group">
                <motion.div
                  className="w-12 h-12 rounded-xl bg-gradient-to-br from-green-500 to-emerald-600 flex items-center justify-center shadow-lg group-hover:shadow-xl transition-shadow"
                  whileHover={{ rotate: 360 }}
                  transition={{ duration: 0.6 }}
                >
                  <span className="text-2xl">🌱</span>
                </motion.div>
                <div>
                  <h1 className="text-xl font-bold text-gray-900 dark:text-white group-hover:text-green-600 dark:group-hover:text-green-400 transition-colors tracking-tight">
                    SmartFarm AI
                  </h1>
                  <p className="text-xs text-gray-600 dark:text-gray-400 font-medium">
                    {t('header.subtitle')}
                  </p>
                </div>
              </Link>
            </motion.div>

            {/* Desktop Navigation */}
            <div className="hidden lg:flex items-center gap-8">
              <NavLinks />
              
              {/* Right Side Actions - 32px spacing from nav */}
              <div className="flex items-center gap-3">
                <LanguageToggle />
                <ThemeToggle />
                <ProfileMenu />
              </div>
            </div>

            {/* Mobile Menu Button */}
            <div className="flex items-center gap-3 lg:hidden">
              <LanguageToggle />
              <ThemeToggle />
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                className="p-2 rounded-xl border border-gray-300 dark:border-gray-600 bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm hover:bg-white dark:hover:bg-gray-700 transition-all duration-300"
                aria-label="Toggle Menu"
              >
                <Menu size={20} className="text-gray-700 dark:text-gray-300" />
              </motion.button>
            </div>
          </div>
        </div>

        {/* Scroll Progress Indicator */}
        <motion.div
          className="absolute bottom-0 left-0 h-0.5 bg-gradient-to-r from-green-500 to-emerald-600 origin-left"
          style={{ width: '100%' }}
          animate={{
            scaleX: scrollProgress
          }}
          transition={{ duration: 0.1 }}
        />
      </motion.header>

      {/* Mobile Menu */}
      <MobileMenu isOpen={mobileMenuOpen} onClose={() => setMobileMenuOpen(false)} />

      {/* Spacer for fixed header */}
      <div className="h-20" />
    </>
  )
}
