import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

export default function IntroAnimation({ onComplete }) {
  const [showIntro, setShowIntro] = useState(true)

  useEffect(() => {
    const timer = setTimeout(() => {
      setShowIntro(false)
      setTimeout(() => {
        onComplete?.()
      }, 500)
    }, 2500)

    return () => clearTimeout(timer)
  }, [onComplete])

  return (
    <AnimatePresence>
      {showIntro && (
        <motion.div
          initial={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.5 }}
          className="fixed inset-0 z-50 bg-gray-900 flex items-center justify-center"
        >
          {/* Tree SVG Animation */}
          <motion.div
            initial={{ scale: 0, y: -100 }}
            animate={{ scale: 1, y: 0 }}
            transition={{ duration: 1.2, ease: "easeOut" }}
            className="relative"
          >
            {/* Green Glow */}
            <motion.div
              initial={{ opacity: 0, scale: 0.5 }}
              animate={{ opacity: 0.6, scale: 1.5 }}
              transition={{ duration: 1.5, delay: 0.3 }}
              className="absolute inset-0 bg-green-500 rounded-full blur-3xl"
            />
            
            {/* Tree SVG */}
            <svg
              width="200"
              height="300"
              viewBox="0 0 200 300"
              className="relative z-10"
            >
              {/* Trunk */}
              <motion.rect
                initial={{ height: 0 }}
                animate={{ height: 80 }}
                transition={{ duration: 0.8, delay: 0.2 }}
                x="90"
                y="220"
                width="20"
                height="80"
                fill="#8B4513"
              />
              
              {/* Leaves/Branches */}
              <motion.circle
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ duration: 0.6, delay: 0.4 }}
                cx="100"
                cy="150"
                r="50"
                fill="#0f9d58"
              />
              <motion.circle
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ duration: 0.6, delay: 0.5 }}
                cx="80"
                cy="130"
                r="35"
                fill="#5bbd72"
              />
              <motion.circle
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ duration: 0.6, delay: 0.6 }}
                cx="120"
                cy="130"
                r="35"
                fill="#5bbd72"
              />
              <motion.circle
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ duration: 0.6, delay: 0.7 }}
                cx="100"
                cy="100"
                r="40"
                fill="#0f9d58"
              />
            </svg>
          </motion.div>

          {/* Text Animation */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 1.2 }}
            className="absolute bottom-32 text-center"
          >
            <motion.h1
              className="text-5xl font-bold text-white mb-2"
              initial={{ filter: "blur(10px)" }}
              animate={{ filter: "blur(0px)" }}
              transition={{ duration: 0.6, delay: 1.4 }}
            >
              {['S', 'm', 'a', 'r', 't', 'F', 'a', 'r', 'm', ' ', 'A', 'I'].map((letter, index) => (
                <motion.span
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3, delay: 1.5 + index * 0.05 }}
                  className="inline-block"
                >
                  {letter === ' ' ? '\u00A0' : letter}
                </motion.span>
              ))}
            </motion.h1>
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 0.8 }}
              transition={{ duration: 0.6, delay: 2 }}
              className="text-gray-400 text-lg"
            >
              منصة الزراعة الذكية
            </motion.p>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}

