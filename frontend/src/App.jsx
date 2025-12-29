import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from './store/authStore'
import { LanguageProvider } from './context/LanguageContext'
import { ThemeProvider } from './context/ThemeContext'
import Layout from './components/Layout'
import Home from './pages/Home'
import AIPlantAnalysis from './pages/AIPlantAnalysis'
import SmartWaterOptimization from './pages/SmartWaterOptimization'
import SoilHealthDetection from './pages/SoilHealthDetection'
import FertilizerPestDiagnosis from './pages/FertilizerPestDiagnosis'
import Dashboard from './pages/Dashboard'
import PlantsLibrary from './pages/PlantsLibrary'
import Progress from './pages/Progress'
import Reports from './pages/Reports'
import Profile from './pages/Profile'
import Settings from './pages/Settings'
import Login from './pages/Login'
import Register from './pages/Register'
import ForgotPassword from './pages/ForgotPassword'
import PlantComparison from './pages/PlantComparison'
import WeeklyRecommendations from './pages/WeeklyRecommendations'
import Achievements from './pages/Achievements'
import Chatbot from './pages/Chatbot'

function PrivateRoute({ children }) {
  const { isAuthenticated, token, isLoading } = useAuthStore()
  // Check token in localStorage first (fast, no API call)
  const hasToken = !!localStorage.getItem('auth_token')
  const authenticated = isAuthenticated || !!token || hasToken
  
  // Show loading only briefly, then redirect if not authenticated
  if (isLoading && hasToken) {
    // Show minimal loading (don't block)
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-500"></div>
      </div>
    )
  }
  
  if (!authenticated) {
    return <Navigate to="/login" replace />
  }
  
  return children
}

function App() {
  return (
    <LanguageProvider>
      <ThemeProvider>
        <Router>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/forgot-password" element={<ForgotPassword />} />
            <Route path="/reset-password" element={<ForgotPassword />} />
            <Route
              path="/"
              element={
                <PrivateRoute>
                  <Layout />
                </PrivateRoute>
              }
            >
              <Route index element={<Home />} />
              <Route path="ai-plant-analysis" element={<AIPlantAnalysis />} />
              <Route path="smart-water-optimization" element={<SmartWaterOptimization />} />
              <Route path="soil-health-detection" element={<SoilHealthDetection />} />
              <Route path="fertilizer-pest-diagnosis" element={<FertilizerPestDiagnosis />} />
              <Route path="dashboard" element={<Dashboard />} />
              <Route path="plants" element={<PlantsLibrary />} />
              <Route path="progress" element={<Progress />} />
              <Route path="reports" element={<Reports />} />
              <Route path="profile" element={<Profile />} />
              <Route path="settings" element={<Settings />} />
              <Route path="plant-comparison" element={<PlantComparison />} />
              <Route path="weekly-recommendations" element={<WeeklyRecommendations />} />
              <Route path="achievements" element={<Achievements />} />
              <Route path="chatbot" element={<Chatbot />} />
            </Route>
          </Routes>
        </Router>
      </ThemeProvider>
    </LanguageProvider>
  )
}

export default App

