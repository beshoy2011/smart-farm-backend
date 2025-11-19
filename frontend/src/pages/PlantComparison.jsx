import { useState } from 'react'
import { motion } from 'framer-motion'
import { GitCompare, CheckCircle2, AlertTriangle, Droplet, Leaf, TrendingUp } from 'lucide-react'
import { useAnalysisFeed } from '../modules/smartfarm/DataStore'
import api from '../services/api'

export default function PlantComparisonPage() {
  const { results } = useAnalysisFeed()
  const [selected1, setSelected1] = useState(null)
  const [selected2, setSelected2] = useState(null)
  const [comparison, setComparison] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleCompare = async () => {
    if (!selected1 || !selected2) {
      alert('يرجى اختيار نباتين للمقارنة')
      return
    }

    if (selected1 === selected2) {
      alert('يرجى اختيار نباتين مختلفين')
      return
    }

    setLoading(true)
    try {
      const response = await api.post('/analysis/compare_plants', {
        analysis_id_1: selected1,
        analysis_id_2: selected2,
      })
      setComparison(response.data)
    } catch (error) {
      console.error('Comparison failed:', error)
      alert('فشلت المقارنة. يرجى المحاولة مرة أخرى.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-rose-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      <div className="container mx-auto px-4 py-12">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 mb-6 shadow-lg">
            <GitCompare size={40} className="text-white" />
          </div>
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4">
            مقارنة النباتات بالذكاء الاصطناعي
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
            قارن بين نباتين واكتشف أيهم أكثر صحة، يحتاج مياه أكثر، ينمو أسرع، أو مهدد بمرض
          </p>
        </motion.div>

        {/* Plant Selection */}
        <div className="max-w-6xl mx-auto mb-8">
          <div className="grid md:grid-cols-2 gap-6 mb-6">
            {/* Plant 1 Selection */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6"
            >
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">النبات الأول</h3>
              <select
                value={selected1 || ''}
                onChange={(e) => setSelected1(Number(e.target.value))}
                className="w-full p-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              >
                <option value="">اختر نبات...</option>
                {results.map((r) => (
                  <option key={r.id} value={r.aiPayload?.analysis_id}>
                    {new Date(r.timestamp).toLocaleString('ar-EG')} - صحة: {r.metrics?.healthScore?.toFixed(1)}%
                  </option>
                ))}
              </select>
              {selected1 && (
                <div className="mt-4 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  {(() => {
                    const plant = results.find(r => r.aiPayload?.analysis_id === selected1)
                    if (!plant) return null
                    return (
                      <>
                        <img
                          src={plant.imageSource}
                          alt="Plant 1"
                          className="w-full h-32 object-cover rounded-lg mb-2"
                        />
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          الصحة: {plant.metrics?.healthScore?.toFixed(1)}%
                        </p>
                      </>
                    )
                  })()}
                </div>
              )}
            </motion.div>

            {/* Plant 2 Selection */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6"
            >
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">النبات الثاني</h3>
              <select
                value={selected2 || ''}
                onChange={(e) => setSelected2(Number(e.target.value))}
                className="w-full p-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              >
                <option value="">اختر نبات...</option>
                {results.map((r) => (
                  <option key={r.id} value={r.aiPayload?.analysis_id}>
                    {new Date(r.timestamp).toLocaleString('ar-EG')} - صحة: {r.metrics?.healthScore?.toFixed(1)}%
                  </option>
                ))}
              </select>
              {selected2 && (
                <div className="mt-4 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  {(() => {
                    const plant = results.find(r => r.aiPayload?.analysis_id === selected2)
                    if (!plant) return null
                    return (
                      <>
                        <img
                          src={plant.imageSource}
                          alt="Plant 2"
                          className="w-full h-32 object-cover rounded-lg mb-2"
                        />
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          الصحة: {plant.metrics?.healthScore?.toFixed(1)}%
                        </p>
                      </>
                    )
                  })()}
                </div>
              )}
            </motion.div>
          </div>

          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleCompare}
            disabled={loading || !selected1 || !selected2}
            className="w-full md:w-auto px-8 py-4 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-xl font-semibold shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'جاري المقارنة...' : 'مقارنة النباتات'}
          </motion.button>
        </div>

        {/* Comparison Results */}
        {comparison && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="max-w-6xl mx-auto"
          >
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 mb-6">
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">نتائج المقارنة</h2>
              <p className="text-lg text-gray-700 dark:text-gray-300 mb-8 p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg">
                {comparison.summary_arabic}
              </p>

              <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="p-6 bg-emerald-50 dark:bg-emerald-900/20 rounded-xl">
                  <div className="flex items-center gap-3 mb-3">
                    <CheckCircle2 size={24} className="text-emerald-600" />
                    <h3 className="font-bold text-gray-900 dark:text-white">الأكثر صحة</h3>
                  </div>
                  <p className="text-2xl font-bold text-emerald-700 dark:text-emerald-300 mb-2">
                    {comparison.healthier}
                  </p>
                  <div className="text-sm text-gray-600 dark:text-gray-400 space-y-1">
                    <p>النبات 1: {comparison.health_score_1?.toFixed(1)}%</p>
                    <p>النبات 2: {comparison.health_score_2?.toFixed(1)}%</p>
                  </div>
                </div>

                <div className="p-6 bg-blue-50 dark:bg-blue-900/20 rounded-xl">
                  <div className="flex items-center gap-3 mb-3">
                    <Droplet size={24} className="text-blue-600" />
                    <h3 className="font-bold text-gray-900 dark:text-white">يحتاج مياه</h3>
                  </div>
                  <p className="text-2xl font-bold text-blue-700 dark:text-blue-300 mb-2">
                    {comparison.needs_water}
                  </p>
                  <div className="text-sm text-gray-600 dark:text-gray-400 space-y-1">
                    <p>النبات 1: {comparison.water_level_1?.toFixed(1)}%</p>
                    <p>النبات 2: {comparison.water_level_2?.toFixed(1)}%</p>
                  </div>
                </div>

                <div className="p-6 bg-amber-50 dark:bg-amber-900/20 rounded-xl">
                  <div className="flex items-center gap-3 mb-3">
                    <TrendingUp size={24} className="text-amber-600" />
                    <h3 className="font-bold text-gray-900 dark:text-white">أسرع نمو</h3>
                  </div>
                  <p className="text-2xl font-bold text-amber-700 dark:text-amber-300 mb-2">
                    {comparison.faster_growth}
                  </p>
                  <div className="text-sm text-gray-600 dark:text-gray-400 space-y-1">
                    <p>النبات 1: {comparison.growth_rate_1?.toFixed(1)}</p>
                    <p>النبات 2: {comparison.growth_rate_2?.toFixed(1)}</p>
                  </div>
                </div>

                <div className="p-6 bg-rose-50 dark:bg-rose-900/20 rounded-xl">
                  <div className="flex items-center gap-3 mb-3">
                    <AlertTriangle size={24} className="text-rose-600" />
                    <h3 className="font-bold text-gray-900 dark:text-white">مهدد بمرض</h3>
                  </div>
                  <p className="text-2xl font-bold text-rose-700 dark:text-rose-300 mb-2">
                    {comparison.disease_threat}
                  </p>
                  <div className="text-sm text-gray-600 dark:text-gray-400 space-y-1">
                    <p>النبات 1: {comparison.disease_prob_1?.toFixed(1)}%</p>
                    <p>النبات 2: {comparison.disease_prob_2?.toFixed(1)}%</p>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        )}

        {results.length < 2 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="max-w-2xl mx-auto text-center bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-8"
          >
            <GitCompare size={64} className="mx-auto mb-4 text-gray-400" />
            <h3 className="text-2xl font-semibold text-gray-900 dark:text-white mb-2">
              تحتاج نباتين على الأقل للمقارنة
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              ارفع صور نباتاتك في صفحة تحليل النباتات أولاً
            </p>
          </motion.div>
        )}
      </div>
    </div>
  )
}

