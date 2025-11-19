import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useGoogleLogin } from '@react-oauth/google'
import { useAuthStore } from '../store/authStore'
import { useLanguage } from '../context/LanguageContext'
import { LogIn } from 'lucide-react'

export default function Login() {
  const { t } = useLanguage()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const { login, loginWithGoogle } = useAuthStore()

  const handleGoogleLogin = useGoogleLogin({
    onSuccess: async (tokenResponse) => {
      const result = await loginWithGoogle(tokenResponse.access_token)
      if (result.success) {
        navigate('/')
      } else {
        setError(result.error || 'Google login failed')
      }
    },
    onError: () => {
      setError('Google login failed')
    },
  })

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    const formData = new URLSearchParams()
    formData.append('username', username)
    formData.append('password', password)

    const result = await login(username, password)
    
    setLoading(false)
    
    if (result.success) {
      navigate('/')
    } else {
      setError(result.error || 'Login failed')
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-500 to-secondary-600 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center p-4">
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl p-8 w-full max-w-md">
        <div className="text-center mb-8">
          <div className="w-16 h-16 bg-primary-500 rounded-full flex items-center justify-center mx-auto mb-4">
            <span className="text-3xl">🌱</span>
          </div>
          <h1 className="text-3xl font-bold text-gray-800 dark:text-white mb-2">SmartFarm AI</h1>
          <p className="text-gray-600 dark:text-gray-400">منصة الزراعة الذكية</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {error && (
            <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-4 py-3 rounded-lg text-sm">
              <strong>{t('common.error')}:</strong> {error}
            </div>
          )}

          <div>
            <label className="block text-gray-700 dark:text-gray-300 font-semibold mb-2">
              {t('auth.login.username')}
            </label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
              placeholder={t('auth.login.username')}
            />
          </div>

          <div>
            <div className="flex items-center justify-between mb-2">
              <label className="block text-gray-700 dark:text-gray-300 font-semibold">
                {t('auth.login.password')}
              </label>
              <Link
                to="/forgot-password"
                className="text-sm text-primary-600 dark:text-primary-400 hover:underline font-medium"
              >
                {t('auth.login.forgotPassword')}
              </Link>
            </div>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
              placeholder={t('auth.login.password')}
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-primary-500 text-white py-3 rounded-lg font-semibold hover:bg-primary-600 transition flex items-center justify-center space-x-2 disabled:opacity-50"
          >
            <LogIn size={20} />
            <span>{loading ? t('auth.login.loggingIn') : t('auth.login.loginButton')}</span>
          </button>
        </form>

        <div className="mt-6">
          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-gray-300"></div>
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-2 bg-white dark:bg-gray-800 text-gray-500 dark:text-gray-400">Or continue with</span>
            </div>
          </div>

          <button
            onClick={handleGoogleLogin}
            className="mt-4 w-full flex items-center justify-center space-x-2 px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition"
          >
            <svg className="w-5 h-5" viewBox="0 0 24 24">
              <path
                fill="#4285F4"
                d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
              />
              <path
                fill="#34A853"
                d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
              />
              <path
                fill="#FBBC05"
                d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
              />
              <path
                fill="#EA4335"
                d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
              />
            </svg>
            <span className="text-gray-700 dark:text-gray-300 font-medium">Sign in with Google</span>
          </button>
        </div>

        <p className="mt-6 text-center text-gray-600 dark:text-gray-400">
          {t('auth.login.noAccount')}{' '}
          <Link to="/register" className="text-primary-600 dark:text-primary-400 font-semibold hover:underline">
            {t('auth.login.register')}
          </Link>
        </p>
      </div>
    </div>
  )
}

