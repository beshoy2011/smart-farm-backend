import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { ChevronDown, Info, Eye, BarChart3 } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'

export default function ExplainabilityPanel({ explainability }) {
  const { t } = useLanguage()
  const [isOpen, setIsOpen] = useState(false)

  if (!explainability) return null

  const confidenceBreakdown = explainability.confidenceBreakdown || {}
  const visualIndicators = explainability.visualIndicators || []

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.6 }}
      className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg overflow-hidden"
    >
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between p-6 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
      >
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center">
            <Info size={20} className="text-white" />
          </div>
          <h3 className="text-xl font-bold text-gray-900 dark:text-white">
            {t('plantAnalysis.explainability.title')}
          </h3>
        </div>
        <motion.div
          animate={{ rotate: isOpen ? 180 : 0 }}
          transition={{ duration: 0.3 }}
        >
          <ChevronDown size={24} className="text-gray-600 dark:text-gray-400" />
        </motion.div>
      </button>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3 }}
            className="overflow-hidden"
          >
            <div className="px-6 pb-6 space-y-6">
              {/* Confidence Breakdown */}
              <div>
                <div className="flex items-center gap-2 mb-4">
                  <BarChart3 size={20} className="text-indigo-600 dark:text-indigo-400" />
                  <h4 className="font-semibold text-gray-900 dark:text-white">
                    {t('plantAnalysis.explainability.confidenceBreakdown')}
                  </h4>
                </div>
                {Object.keys(confidenceBreakdown).length > 0 ? (
                  <div className="space-y-3">
                    {Object.entries(confidenceBreakdown).map(([key, value]) => (
                      <div key={key}>
                        <div className="flex items-center justify-between mb-1">
                          <span className="text-sm text-gray-600 dark:text-gray-400 capitalize">
                            {key}
                          </span>
                          <span className="text-sm font-semibold text-gray-900 dark:text-white">
                            {(value * 100).toFixed(0)}%
                          </span>
                        </div>
                        <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                          <motion.div
                            initial={{ width: 0 }}
                            animate={{ width: `${value * 100}%` }}
                            transition={{ duration: 0.8 }}
                            className="bg-gradient-to-r from-indigo-500 to-purple-500 h-2 rounded-full"
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    No explainability data available for this sample.
                  </p>
                )}
              </div>

              {/* Visual Indicators */}
              <div>
                <div className="flex items-center gap-2 mb-4">
                  <Eye size={20} className="text-indigo-600 dark:text-indigo-400" />
                  <h4 className="font-semibold text-gray-900 dark:text-white">
                    {t('plantAnalysis.explainability.visualIndicators')}
                  </h4>
                </div>
                {visualIndicators.length > 0 ? (
                  <ul className="space-y-2">
                    {visualIndicators.map((indicator, index) => (
                      <motion.li
                        key={index}
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.1 * index }}
                        className="flex items-start gap-2 text-sm text-gray-600 dark:text-gray-400"
                      >
                        <span className="text-indigo-600 dark:text-indigo-400 mt-1">•</span>
                        <span>{indicator}</span>
                      </motion.li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    No visual indicators captured.
                  </p>
                )}
              </div>

              {/* Heatmap Placeholder */}
              <div className="bg-gray-100 dark:bg-gray-700 rounded-xl p-8 text-center">
                <Eye size={48} className="mx-auto mb-4 text-gray-400" />
                <p className="text-gray-600 dark:text-gray-400">
                  {t('plantAnalysis.explainability.heatmapPlaceholder')}
                </p>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  )
}

