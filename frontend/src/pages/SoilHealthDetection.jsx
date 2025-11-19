import { motion } from 'framer-motion'
import { Sprout, CheckCircle, AlertCircle, RefreshCw } from 'lucide-react'
import { useLanguage } from '../context/LanguageContext'
import { useAnalysisFeed } from '../modules/smartfarm/DataStore'

export default function SoilHealthDetection() {
  const { t } = useLanguage()
  const { latest } = useAnalysisFeed()
  const plantData = latest?.aiPayload
  const lastUpdated = latest?.timestamp

  // Use store data or defaults
  const nutrients = plantData?.nutrient_profile && Object.keys(plantData.nutrient_profile).length > 0 
    ? plantData.nutrient_profile 
    : {
        'pH Level': { level: 'optimal', value: 0.68 },
        'Nitrogen': { level: 'optimal', value: 0.72 },
        'Phosphorus': { level: 'low', value: 0.45 },
        'Potassium': { level: 'optimal', value: 0.68 }
      }
  
  const qualityScore = plantData?.plant_health_score || 68

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-300">
      <div className="container mx-auto px-4 py-12">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <motion.div
            className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-gradient-to-br from-green-500 to-emerald-500 mb-6"
            whileHover={{ scale: 1.1, rotate: 360 }}
            transition={{ duration: 0.6 }}
          >
            <Sprout size={40} className="text-white" />
          </motion.div>
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
            {t('pages.soilHealthDetection.title')}
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-400">
            {t('pages.soilHealthDetection.description')}
          </p>
        </motion.div>

        {/* Auto-Update Indicator */}
        {plantData && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="max-w-4xl mx-auto mb-4 text-center"
          >
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-green-50 dark:bg-green-900/20 rounded-full">
              <RefreshCw size={16} className="text-green-600 dark:text-green-400 animate-spin" />
              <p className="text-sm text-green-600 dark:text-green-400">
                {t('plantAnalysis.lastUpdated')} {new Date(lastUpdated).toLocaleString()}
              </p>
            </div>
          </motion.div>
        )}

        {/* Content */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="max-w-4xl mx-auto"
        >
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-8">
            {/* Soil Quality Score */}
            <div className="mb-6 p-4 bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 rounded-xl">
              <div className="flex items-center justify-between">
                <span className="text-lg font-semibold text-gray-900 dark:text-white">Soil Quality Score</span>
                <span className="text-3xl font-bold text-green-600 dark:text-green-400">{qualityScore}</span>
              </div>
            </div>

            <div className="space-y-4">
              {Object.entries(nutrients).map(([nutrient, data], index) => {
                const level = data.level || (data.value > 0.7 ? 'optimal' : data.value > 0.4 ? 'low' : 'deficient')
                const status = level === 'optimal' ? 'good' : 'warning'
                const Icon = status === 'good' ? CheckCircle : AlertCircle
                const value = data.value ? `${(data.value * 100).toFixed(0)}%` : (data.value || 'Optimal')
                
                return (
                  <motion.div
                    key={nutrient}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.3 + index * 0.1 }}
                    className="flex items-center justify-between p-4 rounded-xl bg-gray-50 dark:bg-gray-700"
                  >
                    <div className="flex items-center gap-3">
                      <Icon
                        size={24}
                        className={status === 'good' ? 'text-green-500' : 'text-yellow-500'}
                      />
                      <span className="text-lg font-medium text-gray-900 dark:text-white">
                        {nutrient}
                      </span>
                    </div>
                    <span className={`text-lg font-semibold ${
                      status === 'good' ? 'text-green-600 dark:text-green-400' : 'text-yellow-600 dark:text-yellow-400'
                    }`}>
                      {value}
                    </span>
                  </motion.div>
                )
              })}
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}
