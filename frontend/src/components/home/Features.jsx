import { motion } from 'framer-motion'
import { useInView } from 'framer-motion'
import { useRef } from 'react'
import { 
  Brain, 
  Droplets, 
  Sprout, 
  Bug,
  Sparkles
} from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'

export default function Features() {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, amount: 0.2 })
  const { t } = useLanguage()

  const features = [
    {
      icon: Brain,
      title: t('home.features.aiPlantAnalysis.title'),
      description: t('home.features.aiPlantAnalysis.description'),
      gradient: 'from-purple-500 to-pink-500'
    },
    {
      icon: Droplets,
      title: t('home.features.waterOptimization.title'),
      description: t('home.features.waterOptimization.description'),
      gradient: 'from-blue-500 to-cyan-500'
    },
    {
      icon: Sprout,
      title: t('home.features.soilHealth.title'),
      description: t('home.features.soilHealth.description'),
      gradient: 'from-green-500 to-emerald-500'
    },
    {
      icon: Bug,
      title: t('home.features.fertilizerPest.title'),
      description: t('home.features.fertilizerPest.description'),
      gradient: 'from-orange-500 to-red-500'
    }
  ]

  return (
    <section ref={ref} className="py-20 bg-white dark:bg-gray-900 relative overflow-hidden">
      {/* Background Decoration */}
      <div className="absolute inset-0 bg-gradient-to-b from-green-50/50 dark:from-gray-800/50 to-transparent" />
      
      <div className="container mx-auto px-4 relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={isInView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <motion.h2
            initial={{ opacity: 0, scale: 0.9 }}
            animate={isInView ? { opacity: 1, scale: 1 } : {}}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="text-5xl font-bold text-gray-900 dark:text-white mb-4"
          >
            {t('home.features.title')}
          </motion.h2>
          <p className="text-xl text-gray-600 dark:text-gray-400">
            {t('home.features.subtitle')}
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => (
            <FeatureCard
              key={index}
              feature={feature}
              index={index}
              isInView={isInView}
            />
          ))}
        </div>
      </div>
    </section>
  )
}

function FeatureCard({ feature, index, isInView }) {
  const Icon = feature.icon

  return (
    <motion.div
      initial={{ opacity: 0, y: 50 }}
      animate={isInView ? { opacity: 1, y: 0 } : {}}
      transition={{ duration: 0.6, delay: index * 0.1 }}
      whileHover={{ 
        y: -10,
        scale: 1.05,
        rotateY: 5,
        rotateX: 5
      }}
      className="group relative"
    >
      {/* Glass Morphism Card */}
      <div className="relative h-full p-8 rounded-3xl bg-white/80 dark:bg-gray-800/80 backdrop-blur-lg border border-gray-200/50 dark:border-gray-700/50 shadow-lg hover:shadow-2xl transition-all duration-300">
        {/* Gradient Background on Hover */}
        <motion.div
          className={`absolute inset-0 bg-gradient-to-br ${feature.gradient} opacity-0 group-hover:opacity-10 rounded-3xl transition-opacity duration-300`}
        />

        {/* Icon */}
        <motion.div
          whileHover={{ rotate: 360, scale: 1.2 }}
          transition={{ duration: 0.6 }}
          className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${feature.gradient} flex items-center justify-center mb-6 shadow-lg`}
        >
          <Icon className="text-white" size={32} />
        </motion.div>

        {/* Sparkles Effect */}
        <motion.div
          className="absolute top-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity"
          animate={{
            rotate: [0, 180, 360],
            scale: [1, 1.2, 1]
          }}
          transition={{ duration: 2, repeat: Infinity }}
        >
          <Sparkles className="text-yellow-400" size={20} />
        </motion.div>

        <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-3">
          {feature.title}
        </h3>
        <p className="text-gray-600 dark:text-gray-300 mb-4 leading-relaxed">
          {feature.description}
        </p>

        {/* Shine Effect */}
        <motion.div
          className="absolute inset-0 rounded-3xl opacity-0 group-hover:opacity-20"
          style={{
            background: 'linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.5) 50%, transparent 70%)',
          }}
          animate={{
            x: ['-100%', '200%']
          }}
          transition={{
            duration: 1.5,
            repeat: Infinity,
            repeatDelay: 2
          }}
        />
      </div>
    </motion.div>
  )
}

