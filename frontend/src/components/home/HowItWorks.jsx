import { motion, useInView } from 'framer-motion'
import { useRef } from 'react'
import { Upload, Brain, TrendingUp, ArrowRight } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'

export default function HowItWorks() {
  const ref = useRef(null)
  const isInView = useInView(ref, { once: true, amount: 0.3 })
  const { t } = useLanguage()

  const steps = [
    {
      icon: Upload,
      title: t('home.howItWorks.step1.title'),
      description: t('home.howItWorks.step1.description'),
      number: '01'
    },
    {
      icon: Brain,
      title: t('home.howItWorks.step2.title'),
      description: t('home.howItWorks.step2.description'),
      number: '02'
    },
    {
      icon: TrendingUp,
      title: t('home.howItWorks.step3.title'),
      description: t('home.howItWorks.step3.description'),
      number: '03'
    }
  ]

  return (
    <section ref={ref} className="py-20 bg-gradient-to-b from-white dark:from-gray-900 to-green-50 dark:to-gray-800 relative overflow-hidden">
      <div className="container mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={isInView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="text-5xl font-bold text-gray-900 dark:text-white mb-4">
            {t('home.howItWorks.title')}
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-400">
            {t('home.howItWorks.subtitle')}
          </p>
        </motion.div>

        <div className="relative">
          {/* Connection Line (Desktop) */}
          <div className="hidden lg:block absolute top-1/2 left-0 right-0 h-1 bg-gradient-to-r from-green-200 dark:from-green-800 via-emerald-300 dark:via-emerald-700 to-green-200 dark:to-green-800 transform -translate-y-1/2" />
          
          <div className="grid md:grid-cols-3 gap-8 lg:gap-12 relative">
            {steps.map((step, index) => (
              <StepCard
                key={index}
                step={step}
                index={index}
                isInView={isInView}
              />
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}

function StepCard({ step, index, isInView }) {
  const Icon = step.icon

  return (
    <motion.div
      initial={{ opacity: 0, y: 50 }}
      animate={isInView ? { opacity: 1, y: 0 } : {}}
      transition={{ duration: 0.6, delay: index * 0.2 }}
      className="relative"
    >
      {/* Step Number Badge */}
      <motion.div
        initial={{ scale: 0, rotate: -180 }}
        animate={isInView ? { scale: 1, rotate: 0 } : {}}
        transition={{ duration: 0.6, delay: index * 0.2 + 0.3 }}
        className="absolute -top-6 left-1/2 transform -translate-x-1/2 z-10 w-12 h-12 bg-gradient-to-br from-green-600 to-emerald-600 rounded-full flex items-center justify-center text-white font-bold text-lg shadow-lg"
      >
        {step.number}
      </motion.div>

      <div className="bg-white dark:bg-gray-800 rounded-3xl p-8 shadow-xl hover:shadow-2xl transition-all duration-300 border border-gray-100 dark:border-gray-700 h-full">
        {/* Icon */}
        <motion.div
          whileHover={{ scale: 1.1, rotate: 5 }}
          className="w-20 h-20 bg-gradient-to-br from-green-500 to-emerald-600 rounded-2xl flex items-center justify-center mb-6 mx-auto shadow-lg"
        >
          <Icon className="text-white" size={40} />
        </motion.div>

        <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4 text-center">
          {step.title}
        </h3>
        <p className="text-gray-600 dark:text-gray-300 text-center leading-relaxed mb-4">
          {step.description}
        </p>

        {/* Arrow (Desktop, between steps) */}
        {index < 2 && (
          <div className="hidden lg:block absolute top-1/2 -right-6 transform -translate-y-1/2 z-20">
            <motion.div
              animate={{
                x: [0, 10, 0]
              }}
              transition={{
                duration: 1.5,
                repeat: Infinity,
                delay: index * 0.3
              }}
            >
              <ArrowRight className="text-green-400 dark:text-green-500" size={32} />
            </motion.div>
          </div>
        )}
      </div>
    </motion.div>
  )
}

