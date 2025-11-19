import { motion } from 'framer-motion'
import { Link, useLocation } from 'react-router-dom'
import { useLanguage } from '../../context/LanguageContext'

export default function NavItem({ item, index }) {
  const location = useLocation()
  const { t } = useLanguage()
  const Icon = item.icon
  const isActive = location.pathname === item.path

  return (
    <motion.div
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, delay: index * 0.05 }}
    >
      <Link
        to={item.path}
        className="group relative flex items-center gap-2 px-4 py-2 rounded-xl transition-all duration-300"
      >
        {/* Active Background - covers entire block */}
        {isActive && (
          <motion.div
            layoutId="activeNavBackground"
            className={`absolute inset-0 bg-gradient-to-r ${item.gradient} rounded-xl shadow-md`}
            transition={{ type: 'spring', stiffness: 400, damping: 30 }}
          />
        )}

        {/* Hover Background */}
        {!isActive && (
          <motion.div
            className={`absolute inset-0 bg-gradient-to-r ${item.gradient} rounded-xl opacity-0 group-hover:opacity-15 transition-opacity duration-300`}
          />
        )}

        {/* Content */}
        <div className="relative flex items-center gap-2">
          <Icon
            size={18}
            className={`transition-all duration-300 ${
              isActive
                ? 'text-white'
                : 'text-gray-700 dark:text-gray-300 group-hover:text-green-600 dark:group-hover:text-green-400'
            }`}
          />
          <span
            className={`text-[15px] font-medium transition-colors duration-300 ${
              isActive
                ? 'text-white'
                : 'text-gray-800 dark:text-gray-200 group-hover:text-green-600 dark:group-hover:text-green-400'
            }`}
          >
            {t(item.translationKey)}
          </span>
        </div>
      </Link>
    </motion.div>
  )
}

