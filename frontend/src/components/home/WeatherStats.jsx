import { motion, useInView } from 'framer-motion'
import { useRef, useState, useEffect } from 'react'
import { Cloud, Droplets, Sprout, TrendingUp, Sun } from 'lucide-react'
import api from '../../services/api'
import { useLanguage } from '../../context/LanguageContext'

export default function WeatherStats() {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, amount: 0.2 })
  const { t } = useLanguage()
  const [weather, setWeather] = useState(null)
  const [stats, setStats] = useState({
    waterSaved: 0,
    fertilizerEfficiency: 0,
    plantHealth: 0
  })

  useEffect(() => {
    // Fetch weather data
    api.get('/weather/current')
      .then(response => setWeather(response.data))
      .catch(() => {
        // Fallback data
        setWeather({
          location: 'Cairo, Egypt',
          temperature: 25,
          humidity: 60,
          rainfall: 0
        })
      })

    // Fetch stats (you can replace with actual API call)
    setStats({
      waterSaved: 1250,
      fertilizerEfficiency: 85,
      plantHealth: 92
    })
  }, [])

  return (
    <section ref={ref} className="py-20 bg-gradient-to-br from-green-600 to-emerald-700 text-white relative overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute inset-0" style={{
          backgroundImage: `radial-gradient(circle at 2px 2px, white 1px, transparent 0)`,
          backgroundSize: '40px 40px'
        }} />
      </div>

      <div className="container mx-auto px-4 relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={isInView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="text-5xl font-bold mb-4">
            {t('home.weatherStats.title')}
          </h2>
          <p className="text-xl text-green-100">
            {t('home.weatherStats.subtitle')}
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* Weather Card */}
          <WeatherCard weather={weather} isInView={isInView} index={0} />
          
          {/* Stats Cards */}
          <StatCard
            icon={Droplets}
            label={t('home.weatherStats.waterSaved')}
            value={stats.waterSaved}
            unit="L"
            color="from-blue-400 to-cyan-400"
            isInView={isInView}
            index={1}
          />
          <StatCard
            icon={Sprout}
            label={t('home.weatherStats.fertilizerEfficiency')}
            value={stats.fertilizerEfficiency}
            unit="%"
            color="from-green-400 to-emerald-400"
            isInView={isInView}
            index={2}
          />
          <StatCard
            icon={TrendingUp}
            label={t('home.weatherStats.plantHealthScore')}
            value={stats.plantHealth}
            unit="%"
            color="from-emerald-400 to-teal-400"
            isInView={isInView}
            index={3}
          />
        </div>
      </div>
    </section>
  )
}

function WeatherCard({ weather, isInView, index }) {
  const { t } = useLanguage()
  
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={isInView ? { opacity: 1, scale: 1 } : {}}
      transition={{ duration: 0.6, delay: index * 0.1 }}
      className="bg-white/10 backdrop-blur-lg rounded-3xl p-8 border border-white/20 shadow-2xl"
    >
      <div className="flex items-center justify-between mb-6">
        <div>
          <p className="text-green-200 text-sm mb-2">{t('home.weatherStats.currentWeather')}</p>
          <h3 className="text-2xl font-bold">
            {weather?.location || t('common.loading')}
          </h3>
        </div>
        <motion.div
          animate={{ rotate: [0, 10, -10, 0] }}
          transition={{ duration: 4, repeat: Infinity }}
        >
          <Sun className="text-yellow-300" size={48} />
        </motion.div>
      </div>

      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Cloud className="text-blue-200" size={24} />
            <span className="text-green-100">{t('home.weatherStats.temperature')}</span>
          </div>
          <span className="text-3xl font-bold">
            {weather?.temperature ? Math.round(weather.temperature) : '--'}°C
          </span>
        </div>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Droplets className="text-cyan-200" size={24} />
            <span className="text-green-100">{t('home.weatherStats.humidity')}</span>
          </div>
          <span className="text-2xl font-semibold">
            {weather?.humidity ? Math.round(weather.humidity) : '--'}%
          </span>
        </div>
      </div>
    </motion.div>
  )
}

function StatCard({ icon: Icon, label, value, unit, color, isInView, index }) {
  const [displayValue, setDisplayValue] = useState(0)
  const gradientId = `gradient-${index}`

  useEffect(() => {
    if (isInView) {
      const duration = 2000
      const steps = 60
      const increment = value / steps
      let current = 0
      
      const timer = setInterval(() => {
        current += increment
        if (current >= value) {
          setDisplayValue(value)
          clearInterval(timer)
        } else {
          setDisplayValue(Math.floor(current))
        }
      }, duration / steps)

      return () => clearInterval(timer)
    }
  }, [isInView, value])

  const percentage = unit === '%' ? value : (value / 2000) * 100

  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={isInView ? { opacity: 1, y: 0 } : {}}
      transition={{ duration: 0.6, delay: index * 0.1 }}
      className="bg-white/10 backdrop-blur-lg rounded-3xl p-8 border border-white/20 shadow-2xl"
    >
      <div className="flex items-center justify-between mb-6">
        <div className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${color} flex items-center justify-center shadow-lg`}>
          <Icon className="text-white" size={32} />
        </div>
      </div>

      <h3 className="text-2xl font-bold mb-2">
        {displayValue}{unit}
      </h3>
      <p className="text-green-200 text-sm mb-6">{label}</p>

      {/* Circular Progress */}
      <div className="relative w-32 h-32 mx-auto">
        <svg className="transform -rotate-90 w-32 h-32">
          <circle
            cx="64"
            cy="64"
            r="56"
            stroke="rgba(255,255,255,0.2)"
            strokeWidth="8"
            fill="none"
          />
          <motion.circle
            cx="64"
            cy="64"
            r="56"
            stroke={`url(#${gradientId})`}
            strokeWidth="8"
            fill="none"
            strokeLinecap="round"
            initial={{ pathLength: 0 }}
            animate={isInView ? { pathLength: percentage / 100 } : {}}
            transition={{ duration: 2, delay: index * 0.1 }}
          />
          <defs>
            <linearGradient id={gradientId} x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#60a5fa" />
              <stop offset="100%" stopColor="#34d399" />
            </linearGradient>
          </defs>
        </svg>
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-2xl font-bold">{percentage.toFixed(0)}%</span>
        </div>
      </div>
    </motion.div>
  )
}

