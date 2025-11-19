import { motion } from 'framer-motion'
import { Sun, Moon } from 'lucide-react'
import { useTheme } from '../../context/ThemeContext'

export default function ThemeToggle() {
  const { theme, toggleTheme } = useTheme()

  return (
    <motion.button
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      onClick={toggleTheme}
      className="flex items-center justify-center w-10 h-10 rounded-xl border border-gray-300 dark:border-gray-600 bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm hover:bg-white dark:hover:bg-gray-700 transition-all duration-300 group"
      aria-label="Toggle Theme"
    >
      <motion.div
        animate={{ rotate: theme === 'dark' ? 180 : 0 }}
        transition={{ duration: 0.4 }}
      >
        {theme === 'dark' ? (
          <Moon
            size={18}
            className="text-gray-700 dark:text-gray-300 group-hover:text-yellow-500 transition-colors"
          />
        ) : (
          <Sun
            size={18}
            className="text-gray-700 dark:text-gray-300 group-hover:text-yellow-500 transition-colors"
          />
        )}
      </motion.div>
    </motion.button>
  )
}
