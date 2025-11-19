import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Calendar, CheckCircle2, AlertCircle, Clock, Sparkles } from 'lucide-react'
import api from '../services/api'

export default function WeeklyRecommendationsPage() {
  const [recommendations, setRecommendations] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchRecommendations = async () => {
      try {
        const response = await api.get('/analysis/weekly_recommendations')
        setRecommendations(response.data)
      } catch (error) {
        console.error('Failed to fetch recommendations:', error)
      } finally {
        setLoading(false)
      }
    }
    fetchRecommendations()
  }, [])

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high':
        return 'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800'
      case 'medium':
        return 'bg-yellow-50 dark:bg-yellow-900/20 border-yellow-200 dark:border-yellow-800'
      case 'low':
        return 'bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800'
      default:
        return 'bg-gray-50 dark:bg-gray-800 border-gray-200 dark:border-gray-700'
    }
  }

  const getPriorityIcon = (priority) => {
    switch (priority) {
      case 'high':
        return <AlertCircle size={20} className="text-red-600 dark:text-red-400" />
      case 'medium':
        return <Clock size={20} className="text-yellow-600 dark:text-yellow-400" />
      case 'low':
        return <CheckCircle2 size={20} className="text-blue-600 dark:text-blue-400" />
      default:
        return <CheckCircle2 size={20} className="text-gray-600 dark:text-gray-400" />
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      <div className="container mx-auto px-4 py-12">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-gradient-to-br from-blue-500 to-indigo-500 mb-6 shadow-lg">
            <Calendar size={40} className="text-white" />
          </div>
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4">
            التوصيات الأسبوعية
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
            خطة عناية أسبوعية ذكية لكل نباتاتك بناءً على تحليل الذكاء الاصطناعي
          </p>
        </motion.div>

        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
            <p className="mt-4 text-gray-600 dark:text-gray-400">جاري تحميل التوصيات...</p>
          </div>
        ) : recommendations ? (
          <div className="max-w-4xl mx-auto">
            {/* Summary Card */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 mb-8"
            >
              <div className="flex items-center gap-3 mb-4">
                <Sparkles size={24} className="text-indigo-600 dark:text-indigo-400" />
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white">ملخص الأسبوع</h2>
              </div>
              <p className="text-lg text-gray-700 dark:text-gray-300 mb-4">
                {recommendations.summary}
              </p>
              <div className="grid grid-cols-3 gap-4">
                <div className="p-4 bg-emerald-50 dark:bg-emerald-900/20 rounded-lg">
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">متوسط الصحة</p>
                  <p className="text-2xl font-bold text-emerald-700 dark:text-emerald-300">
                    {recommendations.average_health?.toFixed(1)}%
                  </p>
                </div>
                <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">متوسط المياه</p>
                  <p className="text-2xl font-bold text-blue-700 dark:text-blue-300">
                    {recommendations.average_water?.toFixed(1)}%
                  </p>
                </div>
                <div className="p-4 bg-rose-50 dark:bg-rose-900/20 rounded-lg">
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">خطر المرض</p>
                  <p className="text-2xl font-bold text-rose-700 dark:text-rose-300">
                    {recommendations.average_disease_risk?.toFixed(1)}%
                  </p>
                </div>
              </div>
            </motion.div>

            {/* Recommendations List */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="space-y-4"
            >
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">خطة العناية</h2>
              {recommendations.recommendations?.map((rec, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className={`bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 border-2 ${getPriorityColor(rec.priority)}`}
                >
                  <div className="flex items-start gap-4">
                    <div className="flex-shrink-0 mt-1">
                      {getPriorityIcon(rec.priority)}
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <span className="px-3 py-1 bg-indigo-100 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-300 rounded-full text-sm font-semibold">
                          {rec.day}
                        </span>
                        <h3 className="text-xl font-bold text-gray-900 dark:text-white">
                          {rec.action}
                        </h3>
                      </div>
                      <p className="text-gray-700 dark:text-gray-300">
                        {rec.description}
                      </p>
                    </div>
                  </div>
                </motion.div>
              ))}
            </motion.div>
          </div>
        ) : (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="max-w-2xl mx-auto text-center bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-12"
          >
            <Calendar size={64} className="mx-auto mb-4 text-gray-400" />
            <h3 className="text-2xl font-semibold text-gray-900 dark:text-white mb-2">
              لا توجد توصيات بعد
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              ارفع صور نباتاتك أولاً لإنشاء خطة عناية أسبوعية مخصصة
            </p>
          </motion.div>
        )}
      </div>
    </div>
  )
}

