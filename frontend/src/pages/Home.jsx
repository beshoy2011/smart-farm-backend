import { useState } from 'react'
import { motion } from 'framer-motion'
import IntroAnimation from '../components/IntroAnimation'
import HomeHero from '../components/home/HomeHero'
import Features from '../components/home/Features'
import HowItWorks from '../components/home/HowItWorks'
import WeatherStats from '../components/home/WeatherStats'
import CTASection from '../components/home/CTASection'

export default function Home() {
  const [introComplete, setIntroComplete] = useState(false)

  return (
    <>
      {!introComplete && (
        <IntroAnimation onComplete={() => setIntroComplete(true)} />
      )}
      
      {introComplete && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8 }}
          className="min-h-screen"
        >
          <HomeHero />
          <Features />
          <HowItWorks />
          <WeatherStats />
          <CTASection />
        </motion.div>
      )}
    </>
  )
}

