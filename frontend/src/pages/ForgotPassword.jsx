import { useState, useEffect } from 'react'
import { useNavigate, Link, useSearchParams } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Mail, ArrowLeft, CheckCircle, Lock } from 'lucide-react'
import { useLanguage } from '../context/LanguageContext'
import api from '../services/api'

export default function ForgotPassword() {
  const { t } = useLanguage()
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const [step, setStep] = useState(1) // 1: email, 2: verify code, 3: reset password
  const [email, setEmail] = useState('')
  const [resetToken, setResetToken] = useState('')
  const [verificationCode, setVerificationCode] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [loading, setLoading] = useState(false)

  // Check if token is in URL
  useEffect(() => {
    const token = searchParams.get('token')
    const emailParam = searchParams.get('email')
    
    // Decode email if it's URL encoded
    const decodedEmail = emailParam ? decodeURIComponent(emailParam) : null
    
    if (token && decodedEmail) {
      console.log('Reset password link detected:', { token, email: decodedEmail })
      setResetToken(token)
      setEmail(decodedEmail)
      setStep(3) // Go directly to reset password step
    }
  }, [searchParams])

  const handleSendCode = async (e) => {
    e.preventDefault()
    setError('')
    setSuccess('')
    setLoading(true)

    try {
      const response = await api.post('/auth/forgot-password', { email })
      
      if (response.data.success) {
        // If reset link is provided (development mode), show it
        if (response.data.reset_link) {
          setSuccess(
            <div className="space-y-2">
              <p>{response.data.message || t('auth.forgotPassword.codeSent')}</p>
              <div className="bg-gray-100 dark:bg-gray-800 p-3 rounded-lg break-all">
                <p className="text-sm font-semibold mb-1">Reset Link (Development Mode):</p>
                <a 
                  href={response.data.reset_link} 
                  onClick={(e) => {
                    e.preventDefault()
                    window.location.href = response.data.reset_link
                  }}
                  className="text-blue-600 dark:text-blue-400 hover:underline text-sm cursor-pointer"
                >
                  {response.data.reset_link}
                </a>
                <button
                  onClick={() => {
                    window.location.href = response.data.reset_link
                  }}
                  className="mt-2 px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 text-sm"
                >
                  اضغط هنا لفتح صفحة إعادة تعيين كلمة المرور / Click here to open reset password page
                </button>
              </div>
              <p className="text-xs text-gray-600 dark:text-gray-400">
                Click the link above or copy it to reset your password
              </p>
            </div>
          )
        } else {
          setSuccess(response.data.message || t('auth.forgotPassword.codeSent'))
          // In production, redirect after showing success message
          setTimeout(() => {
            navigate('/login')
          }, 3000)
        }
      } else {
        setError(response.data.error || 'Failed to send reset link')
      }
    } catch (err) {
      // Even if user doesn't exist, we show success for security
      if (err.response?.status === 404 || err.response?.status === 400) {
        setSuccess('If the email exists, a reset link has been sent')
        setTimeout(() => {
          navigate('/login')
        }, 3000)
      } else {
        setError(err.response?.data?.detail || 'Failed to send reset link. Please try again.')
      }
    } finally {
      setLoading(false)
    }
  }

  // Simplified flow - we'll skip the verification code step for now
  // and go directly to reset password with token from URL or email
  const handleVerifyCode = async (e) => {
    e.preventDefault()
    // This step can be skipped if using direct reset link from email
    // For now, we'll move to reset password step
    setStep(3)
  }

  const handleResetPassword = async (e) => {
    e.preventDefault()
    setError('')
    setSuccess('')

    // Validate passwords
    if (newPassword.length < 8) {
      setError(t('auth.register.passwordRequirements'))
      return
    }

    if (newPassword !== confirmPassword) {
      setError('Passwords do not match')
      return
    }

    // Validate password requirements
    const hasUppercase = /[A-Z]/.test(newPassword)
    const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(newPassword)

    if (!hasUppercase || !hasSpecialChar) {
      setError(t('auth.register.passwordRequirements'))
      return
    }

    setLoading(true)

    try {
      // Use reset token from URL or state
      const tokenToUse = resetToken || verificationCode
      
      if (!tokenToUse) {
        setError('Reset token is required. Please use the link from your email.')
        setLoading(false)
        return
      }
      
      const response = await api.post('/auth/reset-password', {
        email,
        reset_token: tokenToUse,
        new_password: newPassword
      })
      
      if (response.data.success) {
        setSuccess(t('auth.forgotPassword.passwordReset'))
        setTimeout(() => {
          navigate('/login')
        }, 2000)
      } else {
        setError(response.data.error || 'Failed to reset password')
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to reset password. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-500 to-emerald-600 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl p-8 w-full max-w-md"
      >
        <div className="text-center mb-8">
          <div className="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-4">
            <Lock className="text-white" size={32} />
          </div>
          <h1 className="text-3xl font-bold text-gray-800 dark:text-white mb-2">
            {t('auth.forgotPassword.title')}
          </h1>
          <p className="text-gray-600 dark:text-gray-400 text-sm">
            {t('auth.forgotPassword.subtitle')}
          </p>
        </div>

        {/* Step 1: Enter Email */}
        {step === 1 && (
          <form onSubmit={handleSendCode} className="space-y-6">
            {error && (
              <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-4 py-3 rounded-lg text-sm">
                {error}
              </div>
            )}
            {success && (
              <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 text-green-700 dark:text-green-400 px-4 py-3 rounded-lg text-sm">
                {typeof success === 'string' ? success : success}
              </div>
            )}

            <div>
              <label className="block text-gray-700 dark:text-gray-300 font-semibold mb-2">
                {t('auth.forgotPassword.email')}
              </label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                  placeholder={t('auth.forgotPassword.email')}
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-green-500 dark:bg-green-600 text-white py-3 rounded-lg font-semibold hover:bg-green-600 dark:hover:bg-green-700 transition flex items-center justify-center gap-2 disabled:opacity-50"
            >
              <Mail size={20} />
              <span>{loading ? t('auth.forgotPassword.sending') : t('auth.forgotPassword.sendCode')}</span>
            </button>
          </form>
        )}

        {/* Step 2: Verify Code */}
        {step === 2 && (
          <form onSubmit={handleVerifyCode} className="space-y-6">
            {error && (
              <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-4 py-3 rounded-lg text-sm">
                {error}
              </div>
            )}
            {success && (
              <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 text-green-700 dark:text-green-400 px-4 py-3 rounded-lg text-sm flex items-center gap-2">
                <CheckCircle size={16} />
                {success}
              </div>
            )}

            <div>
              <label className="block text-gray-700 dark:text-gray-300 font-semibold mb-2">
                {t('auth.forgotPassword.verificationCode')}
              </label>
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                {t('auth.forgotPassword.enterCode')}
              </p>
              <input
                type="text"
                value={verificationCode}
                onChange={(e) => setVerificationCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
                required
                maxLength={6}
                className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent dark:bg-gray-700 dark:text-white text-center text-2xl tracking-widest font-mono"
                placeholder="000000"
              />
            </div>

            <button
              type="submit"
              disabled={loading || verificationCode.length !== 6}
              className="w-full bg-green-500 dark:bg-green-600 text-white py-3 rounded-lg font-semibold hover:bg-green-600 dark:hover:bg-green-700 transition flex items-center justify-center gap-2 disabled:opacity-50"
            >
              <CheckCircle size={20} />
              <span>{loading ? t('auth.forgotPassword.verifying') : t('auth.forgotPassword.verify')}</span>
            </button>
          </form>
        )}

        {/* Step 3: Reset Password */}
        {step === 3 && (
          <form onSubmit={handleResetPassword} className="space-y-6">
            {error && (
              <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-4 py-3 rounded-lg text-sm">
                {error}
              </div>
            )}
            {success && (
              <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 text-green-700 dark:text-green-400 px-4 py-3 rounded-lg text-sm flex items-center gap-2">
                <CheckCircle size={16} />
                {success}
              </div>
            )}

            <div>
              <label className="block text-gray-700 dark:text-gray-300 font-semibold mb-2">
                {t('auth.forgotPassword.newPassword')}
              </label>
              <input
                type="password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                required
                className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                placeholder={t('auth.forgotPassword.newPassword')}
              />
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                {t('auth.register.passwordRequirements')}
              </p>
            </div>

            <div>
              <label className="block text-gray-700 dark:text-gray-300 font-semibold mb-2">
                {t('auth.forgotPassword.confirmPassword')}
              </label>
              <input
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
                className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent dark:bg-gray-700 dark:text-white ${
                  confirmPassword && newPassword !== confirmPassword
                    ? 'border-red-500 dark:border-red-500'
                    : confirmPassword && newPassword === confirmPassword
                    ? 'border-green-500 dark:border-green-500'
                    : 'border-gray-300 dark:border-gray-600'
                }`}
                placeholder={t('auth.forgotPassword.confirmPassword')}
              />
              {confirmPassword && newPassword !== confirmPassword && (
                <p className="text-xs text-red-500 dark:text-red-400 mt-1">
                  {t('auth.forgotPassword.passwordsDoNotMatch')}
                </p>
              )}
            </div>

            <button
              type="submit"
              disabled={loading || !newPassword || !confirmPassword || newPassword !== confirmPassword}
              className="w-full bg-green-500 dark:bg-green-600 text-white py-3 rounded-lg font-semibold hover:bg-green-600 dark:hover:bg-green-700 transition flex items-center justify-center gap-2 disabled:opacity-50"
            >
              <Lock size={20} />
              <span>{loading ? t('auth.forgotPassword.resetting') : t('auth.forgotPassword.resetPassword')}</span>
            </button>
          </form>
        )}

        <div className="mt-6 text-center">
          <Link
            to="/login"
            className="inline-flex items-center gap-2 text-sm text-green-600 dark:text-green-400 hover:underline font-medium"
          >
            <ArrowLeft size={16} />
            {t('auth.forgotPassword.backToLogin')}
          </Link>
        </div>
      </motion.div>
    </div>
  )
}

