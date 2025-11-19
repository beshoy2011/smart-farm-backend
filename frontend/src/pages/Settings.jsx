import { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  Palette, 
  Globe, 
  Bell, 
  Lock, 
  Sun, 
  Moon, 
  Languages,
  Mail,
  Smartphone,
  Cloud,
  Save,
  RotateCcw
} from 'lucide-react'
import { useLanguage } from '../context/LanguageContext'
import { useTheme } from '../context/ThemeContext'

export default function Settings() {
  const { language, setLanguage, t } = useLanguage()
  const { theme, setTheme, toggleTheme } = useTheme()
  const [notifications, setNotifications] = useState({
    email: true,
    push: true,
    analysisUpdates: true,
    weatherAlerts: true
  })
  const [passwordData, setPasswordData] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  })

  const handleNotificationChange = (key) => {
    setNotifications({
      ...notifications,
      [key]: !notifications[key]
    })
  }

  const handlePasswordChange = (e) => {
    setPasswordData({
      ...passwordData,
      [e.target.name]: e.target.value
    })
  }

  const handleSaveSettings = () => {
    // TODO: Implement save functionality
    console.log('Settings saved:', { theme, language, notifications })
  }

  const handleReset = () => {
    setNotifications({
      email: true,
      push: true,
      analysisUpdates: true,
      weatherAlerts: true
    })
    setPasswordData({
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    })
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 py-8">
      <div className="container mx-auto px-4 max-w-4xl">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
            {t('settings.title')}
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Manage your account settings and preferences
          </p>
        </motion.div>

        <div className="space-y-6">
          {/* Appearance Settings */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-lg border border-gray-200 dark:border-gray-700"
          >
            <div className="flex items-center gap-3 mb-6">
              <Palette className="text-green-500" size={24} />
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                {t('settings.appearance.title')}
              </h2>
            </div>

            <div className="space-y-6">
              {/* Theme Selection */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
                  {t('settings.appearance.theme')}
                </label>
                <div className="flex gap-4">
                  <button
                    onClick={() => setTheme('light')}
                    className={`flex-1 flex items-center justify-center gap-2 px-4 py-3 rounded-lg border-2 transition-all ${
                      theme === 'light'
                        ? 'border-green-500 bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-400'
                        : 'border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:border-gray-400'
                    }`}
                  >
                    <Sun size={20} />
                    <span className="font-medium">{t('settings.appearance.light')}</span>
                  </button>
                  <button
                    onClick={() => setTheme('dark')}
                    className={`flex-1 flex items-center justify-center gap-2 px-4 py-3 rounded-lg border-2 transition-all ${
                      theme === 'dark'
                        ? 'border-green-500 bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-400'
                        : 'border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:border-gray-400'
                    }`}
                  >
                    <Moon size={20} />
                    <span className="font-medium">{t('settings.appearance.dark')}</span>
                  </button>
                </div>
              </div>

              {/* Language Selection */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
                  {t('settings.appearance.language')}
                </label>
                <div className="flex gap-4">
                  <button
                    onClick={() => setLanguage('en')}
                    className={`flex-1 flex items-center justify-center gap-2 px-4 py-3 rounded-lg border-2 transition-all ${
                      language === 'en'
                        ? 'border-green-500 bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-400'
                        : 'border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:border-gray-400'
                    }`}
                  >
                    <Languages size={20} />
                    <span className="font-medium">{t('settings.appearance.english')}</span>
                  </button>
                  <button
                    onClick={() => setLanguage('ar')}
                    className={`flex-1 flex items-center justify-center gap-2 px-4 py-3 rounded-lg border-2 transition-all ${
                      language === 'ar'
                        ? 'border-green-500 bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-400'
                        : 'border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:border-gray-400'
                    }`}
                  >
                    <Languages size={20} />
                    <span className="font-medium">{t('settings.appearance.arabic')}</span>
                  </button>
                </div>
              </div>
            </div>
          </motion.div>

          {/* Notifications Settings */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-lg border border-gray-200 dark:border-gray-700"
          >
            <div className="flex items-center gap-3 mb-6">
              <Bell className="text-green-500" size={24} />
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                {t('settings.notifications.title')}
              </h2>
            </div>

            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                <div className="flex items-center gap-3">
                  <Mail className="text-gray-500 dark:text-gray-400" size={20} />
                  <div>
                    <p className="font-medium text-gray-900 dark:text-white">
                      {t('settings.notifications.emailNotifications')}
                    </p>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      Receive email notifications
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => handleNotificationChange('email')}
                  className={`relative w-12 h-6 rounded-full transition-colors ${
                    notifications.email ? 'bg-green-500' : 'bg-gray-300 dark:bg-gray-600'
                  }`}
                >
                  <span
                    className={`absolute top-1 left-1 w-4 h-4 bg-white rounded-full transition-transform ${
                      notifications.email ? 'translate-x-6' : 'translate-x-0'
                    }`}
                  />
                </button>
              </div>

              <div className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                <div className="flex items-center gap-3">
                  <Smartphone className="text-gray-500 dark:text-gray-400" size={20} />
                  <div>
                    <p className="font-medium text-gray-900 dark:text-white">
                      {t('settings.notifications.pushNotifications')}
                    </p>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      Receive push notifications
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => handleNotificationChange('push')}
                  className={`relative w-12 h-6 rounded-full transition-colors ${
                    notifications.push ? 'bg-green-500' : 'bg-gray-300 dark:bg-gray-600'
                  }`}
                >
                  <span
                    className={`absolute top-1 left-1 w-4 h-4 bg-white rounded-full transition-transform ${
                      notifications.push ? 'translate-x-6' : 'translate-x-0'
                    }`}
                  />
                </button>
              </div>

              <div className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                <div className="flex items-center gap-3">
                  <Cloud className="text-gray-500 dark:text-gray-400" size={20} />
                  <div>
                    <p className="font-medium text-gray-900 dark:text-white">
                      {t('settings.notifications.analysisUpdates')}
                    </p>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      Get notified when analysis completes
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => handleNotificationChange('analysisUpdates')}
                  className={`relative w-12 h-6 rounded-full transition-colors ${
                    notifications.analysisUpdates ? 'bg-green-500' : 'bg-gray-300 dark:bg-gray-600'
                  }`}
                >
                  <span
                    className={`absolute top-1 left-1 w-4 h-4 bg-white rounded-full transition-transform ${
                      notifications.analysisUpdates ? 'translate-x-6' : 'translate-x-0'
                    }`}
                  />
                </button>
              </div>

              <div className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                <div className="flex items-center gap-3">
                  <Cloud className="text-gray-500 dark:text-gray-400" size={20} />
                  <div>
                    <p className="font-medium text-gray-900 dark:text-white">
                      {t('settings.notifications.weatherAlerts')}
                    </p>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      Get weather alerts for your farms
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => handleNotificationChange('weatherAlerts')}
                  className={`relative w-12 h-6 rounded-full transition-colors ${
                    notifications.weatherAlerts ? 'bg-green-500' : 'bg-gray-300 dark:bg-gray-600'
                  }`}
                >
                  <span
                    className={`absolute top-1 left-1 w-4 h-4 bg-white rounded-full transition-transform ${
                      notifications.weatherAlerts ? 'translate-x-6' : 'translate-x-0'
                    }`}
                  />
                </button>
              </div>
            </div>
          </motion.div>

          {/* Account Settings */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-lg border border-gray-200 dark:border-gray-700"
          >
            <div className="flex items-center gap-3 mb-6">
              <Lock className="text-green-500" size={24} />
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                {t('settings.account.title')}
              </h2>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  {t('settings.account.currentPassword')}
                </label>
                <input
                  type="password"
                  name="currentPassword"
                  value={passwordData.currentPassword}
                  onChange={handlePasswordChange}
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-transparent"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  {t('settings.account.newPassword')}
                </label>
                <input
                  type="password"
                  name="newPassword"
                  value={passwordData.newPassword}
                  onChange={handlePasswordChange}
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-transparent"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  {t('settings.account.confirmPassword')}
                </label>
                <input
                  type="password"
                  name="confirmPassword"
                  value={passwordData.confirmPassword}
                  onChange={handlePasswordChange}
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-transparent"
                />
              </div>
            </div>
          </motion.div>

          {/* Action Buttons */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="flex gap-4"
          >
            <button
              onClick={handleSaveSettings}
              className="flex-1 flex items-center justify-center gap-2 px-6 py-3 bg-green-500 hover:bg-green-600 text-white rounded-lg font-medium transition-colors"
            >
              <Save size={20} />
              {t('settings.save')}
            </button>
            <button
              onClick={handleReset}
              className="flex items-center justify-center gap-2 px-6 py-3 bg-gray-500 hover:bg-gray-600 text-white rounded-lg font-medium transition-colors"
            >
              <RotateCcw size={20} />
              {t('settings.reset')}
            </button>
          </motion.div>
        </div>
      </div>
    </div>
  )
}

