import { motion } from 'framer-motion'
import { Bug, AlertTriangle, CheckCircle2, RefreshCw } from 'lucide-react'
import { useLanguage } from '../context/LanguageContext'
import { useAnalysisFeed } from '../modules/smartfarm/DataStore'

export default function FertilizerPestDiagnosis() {
  const { t } = useLanguage()
  const { latest } = useAnalysisFeed()
  const plantData = latest?.aiPayload
  const lastUpdated = latest?.timestamp

  const fertilizerNeed = plantData?.fertilizer_need_percent
  const pestData = plantData?.pests
  const diseases = plantData?.detected_diseases || []
  const recommendations = plantData?.recommendations || []
  const hasFertilizerMetric = typeof fertilizerNeed === 'number'
  const fertilizerNeedLabel = hasFertilizerMetric ? `${fertilizerNeed.toFixed(1)}% need` : 'Awaiting data'
  const fertilizerNeedsAttention = hasFertilizerMetric && fertilizerNeed > 60
  const firstDisease = diseases[0]
  const diseaseConfidence = firstDisease ? `${((firstDisease.confidence || 0) * 100).toFixed(0)}%` : null

  const cards = [
    {
      title: 'Pest Detection',
      status: pestData?.detected_pests?.length ? pestData.detected_pests.join(', ') : 'No pests detected',
      icon: pestData?.detected_pests?.length ? AlertTriangle : CheckCircle2,
      color: pestData?.detected_pests?.length ? 'text-yellow-500' : 'text-green-500',
      bg: pestData?.detected_pests?.length ? 'bg-yellow-50 dark:bg-yellow-900/20' : 'bg-green-50 dark:bg-green-900/20',
      details: pestData?.risk_level ? `Risk: ${pestData.risk_level}` : null
    },
    {
      title: 'Disease Analysis',
      status: diseases.length > 0 ? firstDisease?.name || 'Disease detected' : 'Healthy',
      icon: diseases.length > 0 ? AlertTriangle : CheckCircle2,
      color: diseases.length > 0 ? 'text-red-500' : 'text-green-500',
      bg: diseases.length > 0 ? 'bg-red-50 dark:bg-red-900/20' : 'bg-green-50 dark:bg-green-900/20',
      details: diseaseConfidence ? `Confidence ${diseaseConfidence}` : null
    },
    {
      title: 'Fertilizer Status',
      status: fertilizerNeedLabel,
      icon: hasFertilizerMetric ? (fertilizerNeedsAttention ? AlertTriangle : CheckCircle2) : AlertTriangle,
      color: hasFertilizerMetric ? (fertilizerNeedsAttention ? 'text-yellow-500' : 'text-green-500') : 'text-yellow-500',
      bg: hasFertilizerMetric ? (fertilizerNeedsAttention ? 'bg-yellow-50 dark:bg-yellow-900/20' : 'bg-green-50 dark:bg-green-900/20') : 'bg-yellow-50 dark:bg-yellow-900/20',
      details: recommendations.find((rec) => rec.type === 'fertilizer')?.description
    },
    {
      title: 'Treatment Plan',
      status: diseases.length > 0 ? 'Treatment needed' : 'No treatment needed',
      icon: diseases.length > 0 ? AlertTriangle : CheckCircle2,
      color: diseases.length > 0 ? 'text-orange-500' : 'text-blue-500',
      bg: diseases.length > 0 ? 'bg-orange-50 dark:bg-orange-900/20' : 'bg-blue-50 dark:bg-blue-900/20',
      details: recommendations.find((rec) => rec.type === 'treatment')?.description
    }
  ]

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
            className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-gradient-to-br from-orange-500 to-red-500 mb-6"
            whileHover={{ scale: 1.1, rotate: 360 }}
            transition={{ duration: 0.6 }}
          >
            <Bug size={40} className="text-white" />
          </motion.div>
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
            {t('pages.fertilizerPestDiagnosis.title')}
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-400">
            {t('pages.fertilizerPestDiagnosis.description')}
          </p>
        </motion.div>

        {/* Auto-Update Indicator */}
        {plantData && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="max-w-4xl mx-auto mb-4 text-center"
          >
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-orange-50 dark:bg-orange-900/20 rounded-full">
              <RefreshCw size={16} className="text-orange-600 dark:text-orange-400 animate-spin" />
              <p className="text-sm text-orange-600 dark:text-orange-400">
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
          className="max-w-4xl mx-auto grid md:grid-cols-2 gap-6"
        >
          {cards.map((item, index) => (
            <motion.div
              key={item.title}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.3 + index * 0.1 }}
              className={`${item.bg} rounded-2xl shadow-lg p-6`}
            >
              <div className="flex items-center gap-3 mb-4">
                <item.icon size={24} className={item.color} />
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                  {item.title}
                </h3>
              </div>
              <p className={`text-sm font-medium ${item.color}`}>
                {item.status}
              </p>
              {item.details && (
                <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                  {item.details}
                </p>
              )}
            </motion.div>
          ))}
        </motion.div>

        {recommendations.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="max-w-4xl mx-auto mt-10"
          >
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
                AI Recommendations
              </h3>
              <div className="space-y-3">
                {recommendations.map((rec, idx) => (
                  <div key={idx} className="p-4 rounded-xl border border-gray-200 dark:border-gray-700">
                    <p className="text-sm uppercase text-gray-500 dark:text-gray-400">{rec.type}</p>
                    <p className="text-lg font-semibold text-gray-900 dark:text-white">{rec.title}</p>
                    <p className="text-sm text-gray-600 dark:text-gray-300 mt-1">{rec.description}</p>
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

