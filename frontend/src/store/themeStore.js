import { create } from 'zustand'

// Simple localStorage helper
const storage = {
  getItem: (key) => {
    if (typeof window === 'undefined') return null
    try {
      return localStorage.getItem(key)
    } catch {
      return null
    }
  },
  setItem: (key, value) => {
    if (typeof window === 'undefined') return
    try {
      localStorage.setItem(key, value)
    } catch {}
  }
}

const getStoredTheme = () => {
  const stored = storage.getItem('smartfarm-theme')
  return stored === 'dark' ? 'dark' : 'light'
}

const getStoredLanguage = () => {
  const stored = storage.getItem('smartfarm-language')
  return stored === 'ar' ? 'ar' : 'en'
}

export const useThemeStore = create((set, get) => ({
  theme: getStoredTheme(),
  language: getStoredLanguage(),
  
  setTheme: (theme) => {
    set({ theme })
    storage.setItem('smartfarm-theme', theme)
    if (theme === 'dark') {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  },
  
  setLanguage: (language) => {
    set({ language })
    storage.setItem('smartfarm-language', language)
    document.documentElement.dir = language === 'ar' ? 'rtl' : 'ltr'
    document.documentElement.lang = language
  },
  
  toggleTheme: () => {
    const currentTheme = get().theme
    const newTheme = currentTheme === 'light' ? 'dark' : 'light'
    get().setTheme(newTheme)
  },
  
  toggleLanguage: () => {
    const currentLang = get().language
    const newLang = currentLang === 'en' ? 'ar' : 'en'
    get().setLanguage(newLang)
  },
  
  init: () => {
    const { theme, language } = get()
    if (theme === 'dark') {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
    document.documentElement.dir = language === 'ar' ? 'rtl' : 'ltr'
    document.documentElement.lang = language
  }
}))

// Initialize on load
if (typeof window !== 'undefined') {
  useThemeStore.getState().init()
}

