import { motion } from 'framer-motion'
import { Languages } from 'lucide-react'
import { useThemeStore } from '../../store/themeStore'

export default function LanguageSwitcher() {
  const { language, toggleLanguage } = useThemeStore()

  return (
    <motion.button
      whileHover={{ scale: 1.1 }}
      whileTap={{ scale: 0.95 }}
      onClick={toggleLanguage}
      className="relative p-2 rounded-lg bg-white/10 dark:bg-gray-800/50 backdrop-blur-sm border border-gray-200/50 dark:border-gray-700/50 hover:bg-white/20 dark:hover:bg-gray-700/50 transition-all duration-300 group"
      aria-label="Toggle Language"
    >
      <div className="flex items-center gap-2">
        <Languages 
          size={20} 
          className="text-gray-700 dark:text-gray-300 group-hover:text-green-600 dark:group-hover:text-green-400 transition-colors" 
        />
        <motion.span
          key={language}
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: 10 }}
          className="font-semibold text-sm text-gray-700 dark:text-gray-300 min-w-[2rem] text-center"
        >
          {language === 'ar' ? 'AR' : 'EN'}
        </motion.span>
      </div>
      
      {/* Ripple Effect */}
      <motion.div
        className="absolute inset-0 rounded-lg bg-green-500/20"
        initial={{ scale: 0, opacity: 0 }}
        whileTap={{ scale: 2, opacity: [0, 0.5, 0] }}
        transition={{ duration: 0.6 }}
      />
    </motion.button>
  )
}

