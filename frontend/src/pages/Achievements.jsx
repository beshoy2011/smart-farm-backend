import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Trophy, Award, TrendingUp } from 'lucide-react'
import { useLanguage } from '../context/LanguageContext'
import api from '../services/api'
import { AchievementList } from '../components/AchievementBadge'

export default function Achievements() {
  const { t } = useLanguage()
  const [achievements, setAchievements] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadAchievements()
    loadStats()
  }, [])

  const loadAchievements = async () => {
    try {
      const response = await api.get('/api/achievements/')
      setAchievements(response.data)
    } catch (error) {
      console.error('Error loading achievements:', error)
    } finally {
      setLoading(false)
    }
  }

  const loadStats = async () => {
    try {
      const response = await api.get('/api/achievements/stats')
      setStats(response.data)
    } catch (error) {
      console.error('Error loading stats:', error)
    }
  }

  const checkAchievements = async () => {
    try {
      const response = await api.post('/api/achievements/check')
      if (response.data.newly_unlocked?.length > 0) {
        // Reload achievements
        await loadAchievements()
        await loadStats()
        // Show notification for new achievements
        alert(t('achievements.newAchievement').replace('{count}', response.data.newly_unlocked.length))
      }
    } catch (error) {
      console.error('Error checking achievements:', error)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-500"></div>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2 flex items-center gap-3">
          <Trophy className="text-yellow-500" size={32} />
          {t('achievements.title')}
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          {t('achievements.subtitle')}
        </p>
      </motion.div>

      {/* Stats */}
      {stats && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8"
        >
          <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg border border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 dark:text-gray-400 text-sm">{t('achievements.unlocked')}</p>
                <p className="text-3xl font-bold text-gray-900 dark:text-white mt-2">
                  {stats.unlocked}
                </p>
              </div>
              <Award className="text-yellow-500" size={40} />
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg border border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 dark:text-gray-400 text-sm">{t('achievements.total')}</p>
                <p className="text-3xl font-bold text-gray-900 dark:text-white mt-2">
                  {stats.total}
                </p>
              </div>
              <Trophy className="text-orange-500" size={40} />
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg border border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 dark:text-gray-400 text-sm">{t('achievements.progress')}</p>
                <p className="text-3xl font-bold text-gray-900 dark:text-white mt-2">
                  {stats.progress}%
                </p>
              </div>
              <TrendingUp className="text-green-500" size={40} />
            </div>
            <div className="mt-4 w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
              <div
                className="bg-gradient-to-r from-green-500 to-blue-500 h-2 rounded-full transition-all duration-500"
                style={{ width: `${stats.progress}%` }}
              />
            </div>
          </div>
        </motion.div>
      )}

      {/* Check Button */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="mb-6"
      >
        <button
          onClick={checkAchievements}
          className="bg-gradient-to-r from-green-500 to-blue-500 text-white px-6 py-3 rounded-lg font-semibold hover:shadow-lg transition-all"
        >
          🔍 {t('achievements.checkNew')}
        </button>
      </motion.div>

      {/* Achievements List */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
      >
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
          {t('achievements.allAchievements')}
        </h2>
        <AchievementList achievements={achievements} />
      </motion.div>
    </div>
  )
}


