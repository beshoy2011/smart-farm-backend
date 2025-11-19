import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import {
  BarChart3,
  TrendingUp,
  TrendingDown,
  Activity,
  RefreshCw,
  AlertTriangle,
  Droplet,
  Leaf,
  Zap,
  DollarSign,
  Image as ImageIcon,
  LineChart,
  AlertCircle,
  CheckCircle2,
} from 'lucide-react'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js'
import { Line, Bar } from 'react-chartjs-2'
import { useAnalysisFeed } from './DataStore'
import { useLanguage } from '../../context/LanguageContext'
import api from '../../services/api'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

const formatNumber = (value, unit = '') => {
  if (value === null || value === undefined) return '—'
  if (typeof value === 'number') {
    return `${value.toFixed(1)}${unit}`
  }
  return `${value}${unit}`
}

export default function DashboardPage() {
  const { t, language } = useLanguage()
  const { results, latest } = useAnalysisFeed()
  const [costData, setCostData] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    // Fetch cost optimization data
    const fetchCostData = async () => {
      try {
        const response = await api.get('/analysis/cost_optimization')
        setCostData(response.data)
      } catch (error) {
        console.error('Failed to fetch cost data:', error)
      }
    }
    if (results.length > 0) {
      fetchCostData()
    }
  }, [results.length])

  const healthScore = latest?.metrics?.healthScore ?? 0
  const waterNeeds = latest?.metrics?.waterNeeds ?? 0
  const soilMoisture = latest?.moistureLevel ?? 0
  const nutrientLevel = latest?.nutrientLevel ?? 0
  const diseaseProbability = latest?.diseaseProbability ?? 0
  const advanced = latest?.advanced || {}
  // Get fertilizer need from advanced or fallback to aiPayload
  const fertilizerNeedPercent = advanced.fertilizerNeedPercent ?? latest?.aiPayload?.fertilizer_need_percent ?? 0

  // Build health progression chart
  const healthChartData = {
    labels: results.slice(0, 10).reverse().map((r, i) => {
      const label = language === 'ar' ? 'تحليل' : 'Analysis'
      return `${label} ${i + 1}`
    }),
    datasets: [
      {
        label: t('pages.dashboard.stats.plantHealth'),
        data: results.slice(0, 10).reverse().map(r => r.metrics?.healthScore ?? 0),
        borderColor: 'rgb(34, 197, 94)',
        backgroundColor: 'rgba(34, 197, 94, 0.1)',
        tension: 0.4,
        fill: true,
      },
    ],
  }

  const healthChartOptions = {
    responsive: true,
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: true,
        text: t('pages.dashboard.healthProgressionSubtitle'),
        font: { size: 16 },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
      },
    },
  }

  // Statistics cards with advanced data
  const stats = [
    {
      label: t('pages.dashboard.stats.plantHealth'),
      value: formatNumber(healthScore, '%'),
      change: latest ? `${healthScore >= 70 ? t('pages.dashboard.stats.excellent') : t('pages.dashboard.stats.needsCare')}` : '—',
      trend: healthScore >= 70 ? 'up' : 'down',
      icon: Activity,
      color: 'from-emerald-500 to-teal-600',
    },
    {
      label: t('pages.dashboard.stats.soilMoisture'),
      value: formatNumber(soilMoisture, '%'),
      change: latest ? `${soilMoisture >= 40 ? t('pages.dashboard.stats.suitable') : t('pages.dashboard.stats.low')}` : '—',
      trend: soilMoisture >= 40 ? 'up' : 'down',
      icon: Droplet,
      color: 'from-blue-500 to-cyan-600',
    },
    {
      label: t('pages.dashboard.stats.diseaseProbability'),
      value: formatNumber(diseaseProbability, '%'),
      change: latest ? (diseaseProbability >= 40 ? t('pages.dashboard.stats.danger') : t('pages.dashboard.stats.low')) : '—',
      trend: diseaseProbability >= 40 ? 'down' : 'up',
      icon: AlertTriangle,
      color: 'from-rose-500 to-pink-600',
    },
    {
      label: t('pages.dashboard.stats.fertilizerNeed'),
      value: formatNumber(fertilizerNeedPercent, '%'),
      change: latest ? (fertilizerNeedPercent > 50 ? t('pages.dashboard.stats.high') : t('pages.dashboard.stats.normal')) : '—',
      trend: fertilizerNeedPercent > 50 ? 'down' : 'up',
      icon: Leaf,
      color: 'from-amber-500 to-orange-600',
    },
  ]

  // Warnings display
  const warnings = advanced.warnings || {}
  const hasWarnings = advanced.waterAlert || advanced.diseaseAlert || advanced.temperatureAlert || advanced.fertilizerAlert

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-emerald-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 transition-colors duration-300">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center shadow-lg">
                <BarChart3 size={32} className="text-white" />
              </div>
              <div>
                <h1 className="text-4xl font-bold text-gray-900 dark:text-white">
                  {t('pages.dashboard.title')}
                </h1>
                <p className="text-lg text-gray-600 dark:text-gray-400">
                  {t('pages.dashboard.description')}
                </p>
              </div>
            </div>
            {latest && (
              <div className="flex items-center gap-2 px-4 py-2 bg-indigo-50 dark:bg-indigo-900/20 rounded-full">
                <RefreshCw size={16} className="text-indigo-600 dark:text-indigo-400" />
                <p className="text-sm text-indigo-600 dark:text-indigo-400">
                  {t('pages.dashboard.lastUpdated')}: {new Date(latest.timestamp).toLocaleString()}
                </p>
              </div>
            )}
          </div>
        </motion.div>

        {/* Emergency Warnings */}
        {hasWarnings && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="mb-6 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl"
          >
            <div className="flex items-center gap-3 mb-3">
              <AlertCircle size={24} className="text-red-600 dark:text-red-400" />
              <h3 className="text-lg font-bold text-red-900 dark:text-red-100">{t('pages.dashboard.emergencyAlerts')}</h3>
            </div>
            <div className="space-y-2">
              {advanced.waterAlert && (
                <div className="flex items-center gap-2 text-red-700 dark:text-red-300">
                  <AlertTriangle size={16} />
                  <span>{warnings.water_message || t('pages.dashboard.warnings.waterMessage')}</span>
                </div>
              )}
              {advanced.diseaseAlert && (
                <div className="flex items-center gap-2 text-red-700 dark:text-red-300">
                  <AlertTriangle size={16} />
                  <span>{warnings.disease_message || t('pages.dashboard.warnings.diseaseMessage')}</span>
                </div>
              )}
              {advanced.temperatureAlert && (
                <div className="flex items-center gap-2 text-red-700 dark:text-red-300">
                  <AlertTriangle size={16} />
                  <span>{warnings.temperature_message || t('pages.dashboard.warnings.temperatureMessage')}</span>
                </div>
              )}
              {advanced.fertilizerAlert && (
                <div className="flex items-center gap-2 text-red-700 dark:text-red-300">
                  <AlertTriangle size={16} />
                  <span>{warnings.fertilizer_message || t('pages.dashboard.warnings.fertilizerMessage')}</span>
                </div>
              )}
            </div>
          </motion.div>
        )}

        {/* Statistics Cards */}
        <motion.div
          className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.1 }}
        >
          {stats.map((stat) => {
            const Icon = stat.icon
            return (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className={`bg-gradient-to-br ${stat.color} rounded-2xl shadow-lg p-6 text-white`}
              >
                <div className="flex items-center justify-between mb-4">
                  <div className="w-12 h-12 rounded-lg bg-white/20 backdrop-blur flex items-center justify-center">
                    <Icon size={24} className="text-white" />
                  </div>
                  {stat.trend === 'up' ? (
                    <TrendingUp size={20} className="text-white/80" />
                  ) : (
                    <TrendingDown size={20} className="text-white/80" />
                  )}
                </div>
                <h3 className="text-sm font-medium text-white/80 mb-1">{stat.label}</h3>
                <p className="text-3xl font-bold mb-1">{stat.value}</p>
                <p className="text-sm text-white/70">{stat.change}</p>
              </motion.div>
            )
          })}
        </motion.div>

        {/* AI Summary */}
        {(advanced.aiSummaryArabic || advanced.aiSummaryEnglish) && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-8 p-6 bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700"
          >
            <div className="flex items-center gap-3 mb-3">
              <Zap size={24} className="text-purple-600 dark:text-purple-400" />
              <h3 className="text-xl font-bold text-gray-900 dark:text-white">{t('pages.dashboard.aiSummary')}</h3>
            </div>
            <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
              {language === 'ar' 
                ? (advanced.aiSummaryArabic || advanced.aiSummaryEnglish || '')
                : (advanced.aiSummaryEnglish || advanced.aiSummaryArabic || '')}
            </p>
          </motion.div>
        )}

        {/* Charts Row */}
        <div className="grid lg:grid-cols-2 gap-6 mb-8">
          {/* Health Progression Chart */}
          {results.length > 0 && (
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6"
            >
              <div className="flex items-center gap-3 mb-4">
                <LineChart size={24} className="text-indigo-600 dark:text-indigo-400" />
                <h3 className="text-xl font-bold text-gray-900 dark:text-white">{t('pages.dashboard.healthProgression')}</h3>
              </div>
              <div className="h-64">
                <Line data={healthChartData} options={healthChartOptions} />
              </div>
            </motion.div>
          )}

          {/* Cost Optimization */}
          {costData && (
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6"
            >
              <div className="flex items-center gap-3 mb-4">
                <DollarSign size={24} className="text-emerald-600 dark:text-emerald-400" />
                <h3 className="text-xl font-bold text-gray-900 dark:text-white">{t('pages.dashboard.costOptimization')}</h3>
              </div>
              <div className="space-y-4">
                <div className="flex justify-between items-center p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <span className="text-gray-600 dark:text-gray-400">{t('pages.dashboard.totalSavings')}</span>
                  <span className="text-2xl font-bold text-emerald-600">{formatNumber(costData.total_savings, t('common.currency'))}</span>
                </div>
                <div className="flex justify-between items-center p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <span className="text-gray-600 dark:text-gray-400">{t('pages.dashboard.efficiency')}</span>
                  <span className="text-2xl font-bold text-blue-600">{formatNumber(costData.average_efficiency, '%')}</span>
                </div>
                <div className="grid grid-cols-2 gap-3">
                  <div className="p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                    <p className="text-sm text-gray-600 dark:text-gray-400">{t('pages.dashboard.waterUsage')}</p>
                    <p className="text-lg font-bold text-gray-900 dark:text-white">{formatNumber(costData.water_usage_liters, t('common.liters'))}</p>
                  </div>
                  <div className="p-3 bg-amber-50 dark:bg-amber-900/20 rounded-lg">
                    <p className="text-sm text-gray-600 dark:text-gray-400">{t('pages.dashboard.fertilizerUsage')}</p>
                    <p className="text-lg font-bold text-gray-900 dark:text-white">{formatNumber(costData.fertilizer_usage_kg, t('common.kg'))}</p>
                  </div>
                </div>
              </div>
            </motion.div>
          )}
        </div>

        {/* Plant Gallery */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="flex items-center gap-3 mb-6">
            <ImageIcon size={28} className="text-indigo-600 dark:text-indigo-400" />
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white">{t('pages.dashboard.plantGallery')}</h2>
            <span className="px-3 py-1 bg-indigo-100 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-300 rounded-full text-sm font-semibold">
              {results.length} {t('pages.dashboard.images')}
            </span>
          </div>

          {results.length === 0 ? (
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-12 text-center">
              <ImageIcon size={64} className="mx-auto mb-4 text-gray-400" />
              <h3 className="text-2xl font-semibold text-gray-900 dark:text-white mb-2">
                {t('pages.dashboard.noImages')}
              </h3>
              <p className="text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
                {t('pages.dashboard.noImagesDesc')}
              </p>
            </div>
          ) : (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {results.map((entry, index) => (
                <motion.div
                  key={entry.id || index}
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: index * 0.1 }}
                  className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg overflow-hidden border border-gray-200 dark:border-gray-700"
                >
                  <div className="relative">
                    <img
                      src={entry.imageSource || entry.imagePath}
                      alt={entry.filename}
                      className="w-full h-48 object-cover"
                      loading="lazy"
                    />
                    <div className="absolute top-4 left-4">
                      <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                        entry.plantStatus === 'Healthy' 
                          ? 'bg-green-500 text-white' 
                          : entry.plantStatus === 'Warning'
                          ? 'bg-yellow-500 text-white'
                          : 'bg-red-500 text-white'
                      }`}>
                        {entry.plantStatus === 'Healthy' ? t('pages.dashboard.stats.healthy') : entry.plantStatus === 'Warning' ? t('pages.dashboard.stats.warning') : t('pages.dashboard.stats.critical')}
                      </span>
                    </div>
                    <div className="absolute bottom-4 left-4 right-4">
                      <div className="bg-black/60 backdrop-blur rounded-lg p-2 text-white text-xs">
                        {new Date(entry.timestamp).toLocaleString('ar-EG')}
                      </div>
                    </div>
                  </div>
                  <div className="p-4 space-y-3">
                    <div className="grid grid-cols-2 gap-2">
                      <div className="p-2 bg-emerald-50 dark:bg-emerald-900/20 rounded-lg">
                        <p className="text-xs text-gray-600 dark:text-gray-400 mb-1">{t('dashboard.stats.plantHealth')}</p>
                        <p className="text-lg font-bold text-emerald-700 dark:text-emerald-300">
                          {formatNumber(entry.metrics?.healthScore, '%')}
                        </p>
                      </div>
                      <div className="p-2 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                        <p className="text-xs text-gray-600 dark:text-gray-400 mb-1">{t('pages.dashboard.stats.soilMoisture')}</p>
                        <p className="text-lg font-bold text-blue-700 dark:text-blue-300">
                          {formatNumber(entry.moistureLevel, '%')}
                        </p>
                      </div>
                      <div className="p-2 bg-rose-50 dark:bg-rose-900/20 rounded-lg">
                        <p className="text-xs text-gray-600 dark:text-gray-400 mb-1">{t('pages.dashboard.stats.diseaseProbability')}</p>
                        <p className="text-lg font-bold text-rose-700 dark:text-rose-300">
                          {formatNumber(entry.diseaseProbability, '%')}
                        </p>
                      </div>
                      <div className="p-2 bg-amber-50 dark:bg-amber-900/20 rounded-lg">
                        <p className="text-xs text-gray-600 dark:text-gray-400 mb-1">{t('pages.dashboard.stats.soil')}</p>
                        <p className="text-sm font-bold text-amber-700 dark:text-amber-300">
                          {entry.soilCondition || '—'}
                        </p>
                      </div>
                    </div>
                    {(entry.advanced?.aiSummaryArabic || entry.advanced?.aiSummaryEnglish) && (
                      <p className="text-xs text-gray-600 dark:text-gray-400 line-clamp-2">
                        {language === 'ar' 
                          ? (entry.advanced.aiSummaryArabic || entry.advanced.aiSummaryEnglish || '')
                          : (entry.advanced.aiSummaryEnglish || entry.advanced.aiSummaryArabic || '')}
                      </p>
                    )}
                  </div>
                </motion.div>
              ))}
            </div>
          )}
        </motion.div>
      </div>
    </div>
  )
}
