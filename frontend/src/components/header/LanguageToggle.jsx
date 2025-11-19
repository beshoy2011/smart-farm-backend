import { motion } from 'framer-motion'
import { Languages } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'

export default function LanguageToggle() {
  const { language, toggleLanguage } = useLanguage()

  return (
    <motion.button
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      onClick={toggleLanguage}
      className="flex items-center justify-center gap-1.5 px-3 h-10 rounded-xl border border-gray-300 dark:border-gray-600 bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm hover:bg-white dark:hover:bg-gray-700 transition-all duration-300 group"
      aria-label="Toggle Language"
    >
      <motion.div
        animate={{ rotate: language === 'ar' ? 180 : 0 }}
        transition={{ duration: 0.3 }}
      >
        <Languages
          size={18}
          className="text-gray-700 dark:text-gray-300 group-hover:text-green-600 dark:group-hover:text-green-400 transition-colors"
        />
      </motion.div>
      <span className="ml-1.5 text-xs font-semibold text-gray-700 dark:text-gray-300 group-hover:text-green-600 dark:group-hover:text-green-400 transition-colors">
        {language === 'ar' ? 'AR' : 'EN'}
      </span>
    </motion.button>
  )
}

