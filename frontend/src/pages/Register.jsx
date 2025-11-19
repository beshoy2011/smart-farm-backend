import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useGoogleLogin } from '@react-oauth/google'
import { useAuthStore } from '../store/authStore'
import { useLanguage } from '../context/LanguageContext'
import { UserPlus, Check, X } from 'lucide-react'

export default function Register() {
  const { t } = useLanguage()
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    password: '',
    full_name: '',
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const { register, loginWithGoogle } = useAuthStore()

  // Password validation
  const validatePassword = (password) => {
    const hasMinLength = password.length >= 8
    const hasMaxLength = password.length <= 72  // Bcrypt limit
    const hasUppercase = /[A-Z]/.test(password)
    const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password)
    
    return {
      isValid: hasMinLength && hasMaxLength && hasUppercase && hasSpecialChar,
      hasMinLength,
      hasMaxLength,
      hasUppercase,
      hasSpecialChar
    }
  }

  const passwordValidation = validatePassword(formData.password)

  const handleGoogleLogin = useGoogleLogin({
    onSuccess: async (tokenResponse) => {
      const result = await loginWithGoogle(tokenResponse.access_token)
      if (result.success) {
        navigate('/')
      } else {
        setError(result.error || 'Google registration failed')
      }
    },
    onError: () => {
      setError('Google registration failed')
    },
  })

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    
    // Validate password
    if (!passwordValidation.isValid) {
      setError(t('auth.register.passwordRequirements'))
      return
    }

    setLoading(true)

    const result = await register(formData)
    
    setLoading(false)
    
    if (result.success) {
      navigate('/')
    } else {
      setError(result.error || 'Registration failed')
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-500 to-secondary-600 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center p-4">
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl p-8 w-full max-w-md">
        <div className="text-center mb-8">
          <div className="w-16 h-16 bg-primary-500 rounded-full flex items-center justify-center mx-auto mb-4">
            <span className="text-3xl">🌱</span>
          </div>
          <h1 className="text-3xl font-bold text-gray-800 dark:text-white mb-2">{t('auth.register.title')}</h1>
          <p className="text-gray-600 dark:text-gray-400">انشاء حساب جديد</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          {error && (
            <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-4 py-3 rounded-lg text-sm">
              <strong>{t('common.error')}:</strong> {error}
            </div>
          )}

          <div>
            <label className="block text-gray-700 dark:text-gray-300 font-semibold mb-2">{t('auth.register.fullName')}</label>
            <input
              type="text"
              name="full_name"
              value={formData.full_name}
              onChange={handleChange}
              className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 dark:bg-gray-700 dark:text-white"
              placeholder={t('auth.register.fullName')}
            />
          </div>

          <div>
            <label className="block text-gray-700 dark:text-gray-300 font-semibold mb-2">{t('auth.register.email')}</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 dark:bg-gray-700 dark:text-white"
              placeholder={t('auth.register.email')}
            />
          </div>

          <div>
            <label className="block text-gray-700 dark:text-gray-300 font-semibold mb-2">{t('auth.register.username')}</label>
            <input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleChange}
              required
              className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 dark:bg-gray-700 dark:text-white"
              placeholder={t('auth.register.username')}
            />
          </div>

          <div>
            <label className="block text-gray-700 dark:text-gray-300 font-semibold mb-2">{t('auth.register.password')}</label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-primary-500 dark:bg-gray-700 dark:text-white ${
                formData.password && !passwordValidation.isValid
                  ? 'border-red-500 dark:border-red-500'
                  : formData.password && passwordValidation.isValid
                  ? 'border-green-500 dark:border-green-500'
                  : 'border-gray-300 dark:border-gray-600'
              }`}
              placeholder={t('auth.register.password')}
            />
            {formData.password && (
              <div className="mt-2 space-y-1">
                <div className={`flex items-center gap-2 text-xs ${
                  passwordValidation.hasMinLength ? 'text-green-600 dark:text-green-400' : 'text-gray-500 dark:text-gray-400'
                }`}>
                  {passwordValidation.hasMinLength ? <Check size={14} /> : <X size={14} />}
                  {t('auth.register.passwordMinLength')}
                </div>
                {!passwordValidation.hasMaxLength && (
                  <div className="flex items-center gap-2 text-xs text-red-500 dark:text-red-400">
                    <X size={14} />
                    Password must be 72 characters or less
                  </div>
                )}
                <div className={`flex items-center gap-2 text-xs ${
                  passwordValidation.hasUppercase ? 'text-green-600 dark:text-green-400' : 'text-gray-500 dark:text-gray-400'
                }`}>
                  {passwordValidation.hasUppercase ? <Check size={14} /> : <X size={14} />}
                  {t('auth.register.passwordUppercase')}
                </div>
                <div className={`flex items-center gap-2 text-xs ${
                  passwordValidation.hasSpecialChar ? 'text-green-600 dark:text-green-400' : 'text-gray-500 dark:text-gray-400'
                }`}>
                  {passwordValidation.hasSpecialChar ? <Check size={14} /> : <X size={14} />}
                  {t('auth.register.passwordSpecialChar')}
                </div>
              </div>
            )}
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-primary-500 text-white py-3 rounded-lg font-semibold hover:bg-primary-600 transition flex items-center justify-center space-x-2 disabled:opacity-50"
          >
            <UserPlus size={20} />
            <span>{loading ? t('auth.register.creatingAccount') : t('auth.register.registerButton')}</span>
          </button>
        </form>

        <div className="mt-6">
          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-gray-300"></div>
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-2 bg-white text-gray-500">Or continue with</span>
            </div>
          </div>

          <button
            onClick={handleGoogleLogin}
            className="mt-4 w-full flex items-center justify-center space-x-2 px-4 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition"
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
            <span className="text-gray-700 font-medium">Sign up with Google</span>
          </button>
        </div>

        <p className="mt-6 text-center text-gray-600 dark:text-gray-400">
          {t('auth.register.hasAccount')}{' '}
          <Link to="/login" className="text-primary-600 dark:text-primary-400 font-semibold hover:underline">
            {t('auth.register.login')}
          </Link>
        </p>
      </div>
    </div>
  )
}

