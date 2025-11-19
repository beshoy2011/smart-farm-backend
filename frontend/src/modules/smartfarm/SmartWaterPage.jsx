import { motion } from 'framer-motion'
import { Droplets, TrendingUp, BarChart3, RefreshCw, Sparkles } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'
import { useAnalysisFeed } from './DataStore'

const StatCard = ({ icon: Icon, label, value, color }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6"
  >
    <div className={`w-16 h-16 rounded-xl bg-gradient-to-br ${color} flex items-center justify-center mb-4`}>
      <Icon size={32} className="text-white" />
    </div>
    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
      {label}
    </h3>
    <p className="text-3xl font-bold text-gray-900 dark:text-white">
      {value}
    </p>
  </motion.div>
)

export default function SmartWaterPage() {
  const { t } = useLanguage()
  const { latest } = useAnalysisFeed()

  const waterLevel = latest?.metrics?.waterNeeds ?? 0
  const soilMoisture = latest?.moistureLevel ?? 0
  const drynessFactor = latest?.metrics?.drynessFactor ?? 0
  const recommendations = latest?.aiPayload?.recommendations || []

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-300">
      <div className="container mx-auto px-4 py-12">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <motion.div
            className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-gradient-to-br from-blue-500 to-cyan-500 mb-6"
            whileHover={{ scale: 1.1, rotate: 360 }}
            transition={{ duration: 0.6 }}
          >
            <Droplets size={40} className="text-white" />
          </motion.div>
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
            {t('pages.smartWaterOptimization.title')}
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-400">
            {t('pages.smartWaterOptimization.description')}
          </p>
        </motion.div>

        {latest && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="max-w-6xl mx-auto mb-4 text-center"
          >
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-blue-50 dark:bg-blue-900/20 rounded-full">
              <RefreshCw size={16} className="text-blue-600 dark:text-blue-400 animate-spin" />
              <p className="text-sm text-blue-600 dark:text-blue-400">
                {t('plantAnalysis.lastUpdated')} {new Date(latest.timestamp).toLocaleString()}
              </p>
            </div>
          </motion.div>
        )}

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="max-w-6xl mx-auto grid md:grid-cols-3 gap-6"
        >
          <StatCard
            icon={Droplets}
            label="Water Output"
            value={latest ? `${waterLevel.toFixed(2)} L/day` : '—'}
            color="from-blue-500 to-cyan-500"
          />
          <StatCard
            icon={TrendingUp}
            label="Soil Moisture"
            value={latest ? `${soilMoisture.toFixed(1)}%` : '—'}
            color="from-green-500 to-emerald-500"
          />
          <StatCard
            icon={BarChart3}
            label="Dryness Factor"
            value={latest ? drynessFactor.toFixed(2) : '—'}
            color="from-purple-500 to-pink-500"
          />
        </motion.div>

        {recommendations.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="max-w-5xl mx-auto mt-10"
          >
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
                Dynamic Recommendations
              </h3>
              <div className="space-y-3">
                {recommendations.map((rec, idx) => (
                  <div key={`rec-${idx}`} className="flex items-start gap-3 p-4 rounded-xl bg-gray-50 dark:bg-gray-700">
                    <Sparkles size={20} className="text-blue-500 mt-1" />
                    <div>
                      <p className="font-semibold text-gray-900 dark:text-white">{rec.title || 'Action'}</p>
                      <p className="text-sm text-gray-600 dark:text-gray-300">{rec.description || rec}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  )
}

