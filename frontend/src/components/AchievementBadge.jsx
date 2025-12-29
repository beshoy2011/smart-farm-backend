import { motion, AnimatePresence } from 'framer-motion'
import { Trophy, X } from 'lucide-react'
import { useEffect, useState } from 'react'
import { useLanguage } from '../context/LanguageContext'

export function AchievementBadge({ achievement, onClose }) {
  const { t } = useLanguage()
  const [isVisible, setIsVisible] = useState(true)

  useEffect(() => {
    // Auto-close after 5 seconds
    const timer = setTimeout(() => {
      setIsVisible(false)
      setTimeout(() => onClose?.(), 300) // Wait for animation
    }, 5000)

    return () => clearTimeout(timer)
  }, [onClose])

  if (!isVisible) return null

  return (
    <AnimatePresence>
      <motion.div
        initial={{ scale: 0, rotate: -180, opacity: 0 }}
        animate={{ scale: 1, rotate: 0, opacity: 1 }}
        exit={{ scale: 0, rotate: 180, opacity: 0 }}
        transition={{ type: "spring", stiffness: 200, damping: 20 }}
        className="fixed top-4 right-4 z-50 bg-gradient-to-r from-yellow-400 via-orange-500 to-red-500 p-4 rounded-xl shadow-2xl max-w-sm"
        style={{ zIndex: 9999 }}
      >
        <div className="flex items-center gap-3">
          <div className="text-4xl animate-bounce">
            {achievement.icon || '🏆'}
          </div>
          <div className="flex-1">
            <h3 className="font-bold text-white text-lg mb-1">
              {achievement.title}
            </h3>
            <p className="text-sm text-white/90">
              {achievement.description}
            </p>
          </div>
          <button
            onClick={() => {
              setIsVisible(false)
              setTimeout(() => onClose?.(), 300)
            }}
            className="text-white hover:text-gray-200 transition-colors"
          >
            <X size={20} />
          </button>
        </div>
        <div className="mt-2 text-xs text-white/80 text-center">
          🎉 {t('achievements.congratulations')}
        </div>
      </motion.div>
    </AnimatePresence>
  )
}

export function AchievementList({ achievements = [] }) {
  const { t } = useLanguage()
  
  if (achievements.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        <Trophy size={48} className="mx-auto mb-4 opacity-50" />
        <p>{t('achievements.noAchievements')}</p>
        <p className="text-sm mt-2">{t('achievements.noAchievementsDesc')}</p>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {achievements.map((achievement) => (
        <motion.div
          key={achievement.id}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gradient-to-br from-yellow-50 to-orange-50 dark:from-yellow-900/20 dark:to-orange-900/20 p-6 rounded-xl border border-yellow-200 dark:border-yellow-800 hover:shadow-lg transition-shadow"
        >
          <div className="text-4xl mb-3">{achievement.icon}</div>
          <h3 className="font-bold text-lg text-gray-900 dark:text-white mb-2">
            {achievement.title}
          </h3>
          <p className="text-sm text-gray-600 dark:text-gray-300 mb-3">
            {achievement.description}
          </p>
          {achievement.unlocked_at && (
            <p className="text-xs text-gray-500 dark:text-gray-400">
              {t('achievements.unlockedAt')}: {new Date(achievement.unlocked_at).toLocaleDateString()}
            </p>
          )}
        </motion.div>
      ))}
    </div>
  )
}

