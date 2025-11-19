import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Brain, Sparkles, CheckCircle2, History } from 'lucide-react'
import PlantUploader from '../../components/PlantUploader/PlantUploader'
import PlantResults from '../../components/plant/PlantResults'
import ExplainabilityPanel from '../../components/plant/ExplainabilityPanel'
import { ImageAnalyzer } from './ImageAnalyzer'
import { useAnalysisFeed } from './DataStore'
import { useLanguage } from '../../context/LanguageContext'

const formatDate = (value) => {
  try {
    return new Date(value).toLocaleString()
  } catch {
    return value
  }
}

const HistoryCard = ({ entry }) => (
  <motion.div
    initial={{ opacity: 0, y: 10 }}
    animate={{ opacity: 1, y: 0 }}
    className="bg-white/80 dark:bg-gray-900/60 backdrop-blur rounded-2xl border border-gray-200/60 dark:border-gray-700/60 overflow-hidden shadow-lg"
  >
    <div className="relative">
      <img
        src={entry.imageSource || entry.imagePath}
        alt={entry.filename}
        className="w-full h-48 object-cover"
        loading="lazy"
      />
      <span className="absolute top-4 left-4 inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-semibold bg-black/60 text-white">
        <Sparkles size={14} />
        {entry.plantStatus}
      </span>
    </div>
    <div className="p-4 space-y-2 text-sm">
      <p className="text-gray-500 dark:text-gray-400">{formatDate(entry.timestamp)}</p>
      <div className="flex flex-wrap gap-2 text-gray-700 dark:text-gray-200">
        <span className="px-2 py-1 rounded-lg bg-emerald-50 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300 text-xs font-semibold">
          Moisture {entry.moistureLevel}%
        </span>
        <span className="px-2 py-1 rounded-lg bg-sky-50 dark:bg-sky-900/30 text-sky-700 dark:text-sky-300 text-xs font-semibold">
          Nutrients {entry.nutrientLevel}%
        </span>
        <span className="px-2 py-1 rounded-lg bg-rose-50 dark:bg-rose-900/30 text-rose-700 dark:text-rose-300 text-xs font-semibold">
          Disease {entry.diseaseProbability}%
        </span>
      </div>
      <p className="text-xs text-gray-500 dark:text-gray-400">
        Soil: {entry.soilCondition}
      </p>
    </div>
  </motion.div>
)

export default function PlantAnalyzePage() {
  const { t } = useLanguage()
  const { results, latest } = useAnalysisFeed()
  const [showSuccess, setShowSuccess] = useState(false)
  const [error, setError] = useState(null)
  const [isProcessing, setIsProcessing] = useState(false)

  const handleImageUpload = async (file) => {
    if (!file) return
    setShowSuccess(false)
    setError(null)
    setIsProcessing(true)

    try {
      await ImageAnalyzer.analyze(file)
      setShowSuccess(true)
      setTimeout(() => setShowSuccess(false), 2500)
    } catch (err) {
      const message = err?.response?.data?.detail || err?.message || 'Analysis failed'
      setError(message)
    } finally {
      setIsProcessing(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 transition-colors duration-300">
      <div className="container mx-auto px-4 py-12">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <motion.div
            className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 mb-6 shadow-lg"
            whileHover={{ scale: 1.1, rotate: 360 }}
            transition={{ duration: 0.6 }}
          >
            <Brain size={40} className="text-white" />
          </motion.div>
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4">
            {t('pages.aiPlantAnalysis.title')}
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
            {t('pages.aiPlantAnalysis.description')}
          </p>
        </motion.div>

        <div className="max-w-4xl mx-auto mb-8">
          <PlantUploader
            onFileSelected={handleImageUpload}
            isProcessing={isProcessing}
            error={error}
            onClearError={() => setError(null)}
          />
        </div>

        <AnimatePresence>
          {showSuccess && (
            <motion.div
              initial={{ opacity: 0, y: -50, scale: 0.9 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -50, scale: 0.9 }}
              className="fixed top-24 left-1/2 transform -translate-x-1/2 z-50 max-w-md"
            >
              <div className="bg-green-500 text-white rounded-xl shadow-2xl p-4 flex items-center gap-3">
                <CheckCircle2 size={24} />
                <div>
                  <p className="font-semibold">{t('plantAnalysis.successTitle')}</p>
                  <p className="text-sm text-green-100">{t('plantAnalysis.successDescription')}</p>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {latest?.timestamp && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="max-w-4xl mx-auto mb-4 text-center"
          >
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {t('plantAnalysis.lastUpdated')} {formatDate(latest.timestamp)}
            </p>
          </motion.div>
        )}

        {latest?.aiPayload && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="max-w-6xl mx-auto"
          >
            <div className="grid lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2 space-y-6">
                <PlantResults results={latest.aiPayload} />
              </div>
              <div className="space-y-6">
                <motion.div
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.2 }}
                  className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-md rounded-2xl shadow-lg p-6 border border-gray-200/50 dark:border-gray-700/50"
                >
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
                      <Sparkles size={24} className="text-white" />
                    </div>
                    <div>
                      <h3 className="font-bold text-gray-900 dark:text-white">
                        AI Analysis
                      </h3>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        Powered by SmartFarm AI
                      </p>
                    </div>
                  </div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    This analysis uses advanced machine learning models to detect diseases,
                    nutrient deficiencies, and provide actionable recommendations.
                  </p>
                </motion.div>

                <ExplainabilityPanel explainability={latest.aiPayload.explainability} />
              </div>
            </div>
          </motion.div>
        )}

        {!latest?.aiPayload && !isProcessing && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="max-w-2xl mx-auto text-center mt-12"
          >
            <div className="bg-white/60 dark:bg-gray-800/60 backdrop-blur-md rounded-2xl p-8 border border-gray-200/50 dark:border-gray-700/50">
              <Sparkles size={48} className="mx-auto mb-4 text-gray-400" />
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                {t('plantAnalysis.readyTitle')}
              </h3>
              <p className="text-gray-600 dark:text-gray-400">
                {t('plantAnalysis.readyDescription')}
              </p>
            </div>
          </motion.div>
        )}

        <div className="max-w-6xl mx-auto mt-16">
          <div className="flex items-center gap-3 mb-6">
            <History size={24} className="text-emerald-500" />
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
              Analysis History
            </h2>
          </div>
          {results.length === 0 ? (
            <p className="text-gray-500 dark:text-gray-400">
              Upload a plant image to see the analysis timeline.
            </p>
          ) : (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {results.map((entry) => (
                <HistoryCard key={entry.id} entry={entry} />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

