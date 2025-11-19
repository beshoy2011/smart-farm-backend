import { useCallback, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Upload, Image as ImageIcon, Loader2, X, AlertCircle } from 'lucide-react'
import { useLanguage } from '../../context/LanguageContext'

export default function PlantUploader({
  onFileSelected,
  isProcessing,
  error,
  onClearError,
}) {
  const { t } = useLanguage()
  const [isDragging, setIsDragging] = useState(false)
  const [preview, setPreview] = useState(null)

  const handleFile = useCallback((file) => {
    if (!file) {
      setPreview(null)
      onFileSelected(null)
      return
    }

    if (!file.type.startsWith('image/')) {
      return
    }

    const reader = new FileReader()
    reader.onload = (e) => {
      setPreview(e.target.result)
      onFileSelected(file)
    }
    reader.readAsDataURL(file)
  }, [onFileSelected])

  const handleDrop = useCallback((event) => {
    event.preventDefault()
    setIsDragging(false)
    const file = event.dataTransfer.files?.[0]
    handleFile(file)
  }, [handleFile])

  const handleDragOver = useCallback((event) => {
    event.preventDefault()
    setIsDragging(true)
  }, [])

  const handleDragLeave = useCallback((event) => {
    event.preventDefault()
    setIsDragging(false)
  }, [])

  const handleReset = useCallback(() => {
    if (onClearError) onClearError()
    handleFile(null)
  }, [handleFile, onClearError])

  const handleInput = useCallback((event) => {
    const file = event.target.files?.[0]
    handleFile(file)
  }, [handleFile])

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="w-full"
    >
      <div
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        className={`
          relative border-2 border-dashed rounded-2xl p-8 md:p-12
          transition-all duration-300
          ${isDragging ? 'border-green-500 bg-green-50 dark:bg-green-900/20 scale-105' : 'border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-800/50'}
          ${preview ? 'border-green-500 bg-green-50/50 dark:bg-green-900/10' : ''}
        `}
      >
        <AnimatePresence mode="wait">
          {!preview ? (
            <motion.div
              key="upload-state"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="text-center"
            >
              <motion.div
                className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-gradient-to-br from-green-500 to-emerald-600 mb-6"
                whileHover={{ scale: 1.08, rotate: 360 }}
                transition={{ duration: 0.6 }}
              >
                <Upload size={40} className="text-white" />
              </motion.div>
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                {t('plantAnalysis.upload.title')}
              </h3>
              <p className="text-gray-600 dark:text-gray-400 mb-6">
                {t('plantAnalysis.upload.description')}
              </p>
              <label className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-green-600 to-emerald-600 text-white rounded-xl font-semibold cursor-pointer hover:shadow-lg transition-all">
                <ImageIcon size={20} />
                <span>{t('plantAnalysis.upload.selectButton')}</span>
                <input
                  type="file"
                  accept="image/*"
                  className="hidden"
                  onChange={handleInput}
                  disabled={isProcessing}
                />
              </label>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-4">
                {t('plantAnalysis.upload.supportedFormats')}
              </p>
            </motion.div>
          ) : (
            <motion.div
              key="preview-state"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className="relative"
            >
              <div className="relative rounded-xl overflow-hidden bg-gray-100 dark:bg-gray-800">
                <img
                  src={preview}
                  alt="Plant preview"
                  className="w-full h-auto max-h-96 object-contain"
                />
                {isProcessing && (
                  <div className="absolute inset-0 bg-black/50 flex items-center justify-center">
                    <motion.div
                      animate={{ rotate: 360 }}
                      transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                    >
                      <Loader2 size={48} className="text-white" />
                    </motion.div>
                  </div>
                )}
              </div>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handleReset}
                disabled={isProcessing}
                className="absolute top-4 right-4 p-2 bg-white dark:bg-gray-800 rounded-full shadow-lg hover:shadow-xl transition-all disabled:opacity-50"
              >
                <X size={20} className="text-gray-700 dark:text-gray-200" />
              </motion.button>
            </motion.div>
          )}
        </AnimatePresence>

        {error && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-6 flex items-center justify-center gap-2 text-red-600 dark:text-red-400 text-sm"
          >
            <AlertCircle size={18} />
            <span>{error}</span>
          </motion.div>
        )}
      </div>
    </motion.div>
  )
}

