import { createContext, useContext, useState, useEffect } from 'react'
import enTranslations from '../locales/en.json'
import arTranslations from '../locales/ar.json'

const LanguageContext = createContext()

export const useLanguage = () => {
  const context = useContext(LanguageContext)
  if (!context) {
    throw new Error('useLanguage must be used within LanguageProvider')
  }
  return context
}

export const LanguageProvider = ({ children }) => {
  const [language, setLanguage] = useState(() => {
    const saved = localStorage.getItem('smartfarm-language')
    return saved || 'en'
  })

  const translations = language === 'ar' ? arTranslations : enTranslations

  useEffect(() => {
    localStorage.setItem('smartfarm-language', language)
    
    // Update document direction and lang
    document.documentElement.dir = language === 'ar' ? 'rtl' : 'ltr'
    document.documentElement.lang = language
  }, [language])

  const t = (key) => {
    const keys = key.split('.')
    let value = translations
    for (const k of keys) {
      value = value?.[k]
      if (value === undefined) return key
    }
    return value || key
  }

  const toggleLanguage = () => {
    setLanguage(prev => prev === 'en' ? 'ar' : 'en')
  }

  return (
    <LanguageContext.Provider value={{ language, setLanguage, toggleLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  )
}

