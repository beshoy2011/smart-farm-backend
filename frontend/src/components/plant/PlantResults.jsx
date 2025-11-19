import { motion } from 'framer-motion'
import {
  AlertTriangle,
  CheckCircle,
  Leaf,
  Sprout,
  TrendingUp,
  Droplet,
  Bug,
  Lightbulb,
} from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'
import HealthGauge from './HealthGauge'

export default function PlantResults({ results }) {
  const { t } = useLanguage()

  if (!results) return null

  const healthScore = Math.round(results.plant_health_score ?? results.healthScore ?? 0)
  const detectedDiseases = results.detected_diseases || results.diseases || (results.disease ? [results.disease] : [])
  const primaryDisease = detectedDiseases[0] || {
    name: 'No disease detected',
    confidence: 0,
    severity: 'none',
  }
  const growthStage = results.growth_stage || results.growthStage || {
    stage: 'unknown',
    progress: 0,
  }
  const nutrients = results.nutrient_profile || results.nutrients || {}
  const recommendations = results.recommendations || []

  const aiMetrics = [
    { label: 'Water Level', value: results.water_level_percent },
    { label: 'Soil Moisture', value: results.soil_moisture_percent },
    { label: 'Fertilizer Need', value: results.fertilizer_need_percent },
    { label: 'Leaf Color Index', value: results.leaf_color_index },
    { label: 'Dryness Factor', value: results.dryness_factor, suffix: '' },
    { label: 'Nitrogen Deficiency', value: results.nitrogen_deficiency_probability, suffix: '' },
  ]

  const growthStages = {
    seedling: { icon: Sprout, color: 'from-blue-500 to-cyan-500' },
    vegetative: { icon: Leaf, color: 'from-green-500 to-emerald-500' },
    flowering: { icon: TrendingUp, color: 'from-purple-500 to-pink-500' },
    mature: { icon: CheckCircle, color: 'from-orange-500 to-red-500' },
  }

  const GrowthIcon = growthStages[growthStage.stage]?.icon || Sprout
  const growthColor = growthStages[growthStage.stage]?.color || 'from-green-500 to-emerald-500'

  const getNutrientColor = (level) => {
    if (level === 'optimal') return 'text-green-600 dark:text-green-400'
    if (level === 'low') return 'text-yellow-600 dark:text-yellow-400'
    return 'text-red-600 dark:text-red-400'
  }

  const getNutrientBg = (level) => {
    if (level === 'optimal') return 'bg-green-50 dark:bg-green-900/20'
    if (level === 'low') return 'bg-yellow-50 dark:bg-yellow-900/20'
    return 'bg-red-50 dark:bg-red-900/20'
  }

  const formatMetric = (metric) => {
    if (metric.value === undefined || metric.value === null) return '—'
    if (metric.label === 'Dryness Factor' || metric.label === 'Nitrogen Deficiency') {
      return metric.value.toFixed(2)
    }
    return `${metric.value.toFixed(1)}%`
  }

  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-8"
      >
        <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 text-center">
          {t('plantAnalysis.results.healthScore')}
        </h3>
        <HealthGauge score={healthScore} />
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="grid md:grid-cols-3 gap-4"
      >
        {aiMetrics.map((metric) => (
          <div key={metric.label} className="bg-white dark:bg-gray-800 rounded-2xl shadow p-5">
            <p className="text-sm text-gray-500 dark:text-gray-400">{metric.label}</p>
            <p className="text-3xl font-bold text-gray-900 dark:text-white mt-1">
              {formatMetric(metric)}
            </p>
          </div>
        ))}
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6"
      >
        <div className="flex items-center gap-3 mb-4">
          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-red-500 to-orange-500 flex items-center justify-center">
            <Bug size={24} className="text-white" />
          </div>
          <div>
            <h3 className="text-xl font-bold text-gray-900 dark:text-white">
              {t('plantAnalysis.results.disease')}
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {primaryDisease.name}
            </p>
          </div>
        </div>

        <div className="mt-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-gray-600 dark:text-gray-400">
              {t('plantAnalysis.results.confidence')}
            </span>
            <span className="text-sm font-semibold text-gray-900 dark:text-white">
              {((primaryDisease.confidence || 0) * 100).toFixed(0)}%
            </span>
          </div>
          <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${(primaryDisease.confidence || 0) * 100}%` }}
              transition={{ duration: 1, delay: 0.3 }}
              className="bg-gradient-to-r from-red-500 to-orange-500 h-3 rounded-full"
            />
          </div>
          {primaryDisease.symptoms && primaryDisease.symptoms.length > 0 && (
            <ul className="mt-4 space-y-1 text-sm text-gray-600 dark:text-gray-400">
              {primaryDisease.symptoms.map((symptom, index) => (
                <li key={index}>• {symptom}</li>
              ))}
            </ul>
          )}
        </div>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6"
      >
        <div className="flex items-center gap-3 mb-4">
          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center">
            <Droplet size={24} className="text-white" />
          </div>
          <h3 className="text-xl font-bold text-gray-900 dark:text-white">
            {t('plantAnalysis.results.nutrients')}
          </h3>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 gap-3 mt-4">
          {Object.keys(nutrients).length > 0 ? (
            Object.entries(nutrients).map(([nutrient, data]) => (
              <motion.div
                key={nutrient}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.3 }}
                className={`${getNutrientBg(data.level)} rounded-xl p-4`}
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-gray-900 dark:text-white capitalize">
                    {nutrient}
                  </span>
                  {data.level === 'optimal' ? (
                    <CheckCircle size={16} className="text-green-600 dark:text-green-400" />
                  ) : (
                    <AlertTriangle size={16} className={getNutrientColor(data.level)} />
                  )}
                </div>
                <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${Math.min(100, (data.value || 0) * 100)}%` }}
                    transition={{ duration: 1, delay: 0.4 }}
                    className={`h-2 rounded-full ${
                      data.level === 'optimal'
                        ? 'bg-green-500'
                        : data.level === 'low'
                        ? 'bg-yellow-500'
                        : 'bg-red-500'
                    }`}
                  />
                </div>
              </motion.div>
            ))
          ) : (
            <p className="col-span-full text-center text-gray-500 dark:text-gray-400 py-4">
              No nutrient data available
            </p>
          )}
        </div>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6"
      >
        <div className="flex items-center gap-3 mb-4">
          <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${growthColor} flex items-center justify-center`}>
            <GrowthIcon size={24} className="text-white" />
          </div>
          <div>
            <h3 className="text-xl font-bold text-gray-900 dark:text-white">
              {t('plantAnalysis.results.growthStage')}
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400 capitalize">
              {growthStage.stage}
            </p>
          </div>
        </div>

        <div className="mt-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-gray-600 dark:text-gray-400">
              {t('plantAnalysis.results.progress')}
            </span>
            <span className="text-sm font-semibold text-gray-900 dark:text-white">
              {(growthStage.progress * 100).toFixed(0)}%
            </span>
          </div>
          <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${growthStage.progress * 100}%` }}
              transition={{ duration: 1, delay: 0.5 }}
              className={`bg-gradient-to-r ${growthColor} h-3 rounded-full`}
            />
          </div>
        </div>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6"
      >
        <div className="flex items-center gap-3 mb-4">
          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
            <Lightbulb size={24} className="text-white" />
          </div>
          <h3 className="text-xl font-bold text-gray-900 dark:text-white">
            {t('plantAnalysis.results.recommendations')}
          </h3>
        </div>

        <div className="space-y-3 mt-4">
          {recommendations.length > 0 ? (
            recommendations.map((rec, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.5 + index * 0.1 }}
                className="p-4 rounded-xl border border-gray-200 dark:border-gray-700"
              >
                <p className="text-xs uppercase text-gray-500 dark:text-gray-400">
                  {rec.type}
                </p>
                <h4 className="font-semibold text-gray-900 dark:text-white">
                  {rec.title}
                </h4>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {rec.description}
                </p>
              </motion.div>
            ))
          ) : (
            <p className="text-center text-gray-500 dark:text-gray-400 py-4">
              No recommendations available
            </p>
          )}
        </div>
      </motion.div>
    </div>
  )
}

