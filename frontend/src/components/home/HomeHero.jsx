import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import { Upload, BarChart3, Leaf } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'

export default function HomeHero() {
  const { t } = useLanguage()
  
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      {/* Floating Leaf Particles */}
      {[...Array(6)].map((_, i) => {
        const randomX = Math.random() * 100
        const randomY = Math.random() * 100
        return (
          <motion.div
            key={i}
            className="absolute text-green-400 opacity-20"
            style={{
              left: `${randomX}%`,
              top: `${randomY}%`
            }}
            animate={{
              y: [0, -100, -200],
              x: [0, Math.random() * 100 - 50],
              rotate: [0, 180, 360],
              opacity: [0.2, 0.3, 0]
            }}
            transition={{
              duration: 8 + Math.random() * 4,
              repeat: Infinity,
              delay: Math.random() * 2
            }}
          >
            <Leaf size={30} />
          </motion.div>
        )
      })}

      {/* Organic Shapes Background */}
      <div className="absolute inset-0 overflow-hidden">
        <motion.div
          className="absolute top-20 right-20 w-96 h-96 bg-green-200 dark:bg-green-900/30 rounded-full blur-3xl opacity-30 dark:opacity-20"
          animate={{
            scale: [1, 1.2, 1],
            x: [0, 50, 0],
            y: [0, 30, 0]
          }}
          transition={{ duration: 8, repeat: Infinity }}
        />
        <motion.div
          className="absolute bottom-20 left-20 w-96 h-96 bg-emerald-200 dark:bg-emerald-900/30 rounded-full blur-3xl opacity-30 dark:opacity-20"
          animate={{
            scale: [1, 1.3, 1],
            x: [0, -30, 0],
            y: [0, 50, 0]
          }}
          transition={{ duration: 10, repeat: Infinity }}
        />
      </div>

      <div className="container mx-auto px-4 py-20 relative z-10">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left Content */}
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <motion.h1
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="text-6xl lg:text-7xl font-bold text-gray-900 dark:text-white mb-6 leading-tight"
            >
              {t('home.hero.title')}{' '}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-green-600 to-emerald-600 dark:from-green-400 dark:to-emerald-400">
                {t('home.hero.titleHighlight')}
              </span>
            </motion.h1>
            
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
              className="text-xl text-gray-700 dark:text-gray-300 mb-8 leading-relaxed"
            >
              {t('home.hero.description')}
            </motion.p>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.6 }}
              className="flex flex-wrap gap-4"
            >
              <Link
                to="/ai-plant-analysis"
                className="group relative px-8 py-4 bg-gradient-to-r from-green-600 to-emerald-600 dark:from-green-500 dark:to-emerald-500 text-white rounded-full font-semibold text-lg shadow-lg hover:shadow-xl transition-all duration-300 overflow-hidden"
              >
                <span className="relative z-10 flex items-center gap-2">
                  <Upload size={20} />
                  {t('home.hero.startAnalysis')}
                </span>
                <motion.div
                  className="absolute inset-0 bg-gradient-to-r from-emerald-600 to-green-600"
                  initial={{ x: '-100%' }}
                  whileHover={{ x: 0 }}
                  transition={{ duration: 0.3 }}
                />
              </Link>

              <Link
                to="/dashboard"
                className="px-8 py-4 bg-white dark:bg-gray-800 text-green-600 dark:text-green-400 rounded-full font-semibold text-lg shadow-lg hover:shadow-xl border-2 border-green-600 dark:border-green-500 hover:bg-green-50 dark:hover:bg-gray-700 transition-all duration-300 flex items-center gap-2"
              >
                <BarChart3 size={20} />
                {t('home.hero.dashboard')}
              </Link>
            </motion.div>
          </motion.div>

          {/* Right Image */}
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 1, delay: 0.3 }}
            className="relative"
          >
            <motion.div
              animate={{
                y: [0, -20, 0],
                rotate: [0, 2, 0]
              }}
              transition={{
                duration: 6,
                repeat: Infinity,
                ease: "easeInOut"
              }}
              className="relative"
            >
              {/* Plant Image Placeholder */}
              <div className="relative w-full h-[600px] rounded-3xl overflow-hidden shadow-2xl">
                <div className="absolute inset-0 bg-gradient-to-br from-green-400 to-emerald-500 flex items-center justify-center">
                  <Leaf size={200} className="text-white opacity-30" />
                </div>
                <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=800')] bg-cover bg-center opacity-80" />
                <div className="absolute inset-0 bg-gradient-to-t from-green-900/50 to-transparent" />
              </div>

              {/* Decorative Elements */}
            <motion.div
              className="absolute -top-10 -right-10 w-32 h-32 bg-green-200 dark:bg-green-900/30 rounded-full blur-2xl opacity-50 dark:opacity-30"
              animate={{
                scale: [1, 1.2, 1],
                opacity: [0.5, 0.7, 0.5]
              }}
              transition={{ duration: 4, repeat: Infinity }}
            />
            </motion.div>
          </motion.div>
        </div>
      </div>
    </section>
  )
}

