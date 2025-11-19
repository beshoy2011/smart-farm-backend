import { motion } from 'framer-motion'
import { useLanguage } from '../../context/LanguageContext'

export default function HealthGauge({ score }) {
  const { t } = useLanguage()
  const circumference = 2 * Math.PI * 90
  const offset = circumference - (score / 100) * circumference

  const getColor = (score) => {
    if (score >= 80) return '#10b981' // green
    if (score >= 60) return '#f59e0b' // yellow
    return '#ef4444' // red
  }

  const getStatus = (score) => {
    if (score >= 80) return t('plantAnalysis.health.excellent')
    if (score >= 60) return t('plantAnalysis.health.good')
    return t('plantAnalysis.health.poor')
  }

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ delay: 0.3 }}
      className="relative w-64 h-64 mx-auto"
    >
      <svg className="transform -rotate-90 w-full h-full">
        {/* Background circle */}
        <circle
          cx="128"
          cy="128"
          r="90"
          stroke="currentColor"
          strokeWidth="16"
          fill="none"
          className="text-gray-200 dark:text-gray-700"
        />
        {/* Progress circle */}
        <motion.circle
          cx="128"
          cy="128"
          r="90"
          stroke={getColor(score)}
          strokeWidth="16"
          fill="none"
          strokeLinecap="round"
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 1.5, ease: "easeOut" }}
        />
      </svg>
      
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.5, type: "spring" }}
          className="text-5xl font-bold"
          style={{ color: getColor(score) }}
        >
          {score}
        </motion.div>
        <div className="text-sm text-gray-600 dark:text-gray-400 mt-2">
          {getStatus(score)}
        </div>
      </div>
    </motion.div>
  )
}

