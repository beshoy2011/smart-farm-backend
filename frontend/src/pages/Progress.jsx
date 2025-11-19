import { useEffect, useState } from 'react'
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { TrendingUp, Droplet, Leaf } from 'lucide-react'
import api from '../services/api'

export default function Progress() {
  const [progressData, setProgressData] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadProgressData()
  }, [])

  const loadProgressData = async () => {
    try {
      const response = await api.get('/dashboard/progress?weeks=8')
      setProgressData(response.data)
    } catch (error) {
      console.error('Failed to load progress data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-600">Loading progress data...</div>
      </div>
    )
  }

  const chartData = progressData.map(item => ({
    week: `Week ${item.week_number}`,
    water: item.water_usage,
    fertilizer: item.fertilizer_usage,
    health: (item.plant_health_avg * 100).toFixed(1)
  }))

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-800 mb-2">Progress Tracking</h1>
        <p className="text-gray-600">تتبع التقدم والتحسينات</p>
      </div>

      {/* Summary Cards */}
      {progressData.length > 0 && (
        <div className="grid md:grid-cols-3 gap-6">
          <SummaryCard
            icon={Droplet}
            label="Avg Water Usage"
            value={`${(progressData.reduce((sum, p) => sum + p.water_usage, 0) / progressData.length).toFixed(2)} L/day`}
            color="text-blue-600"
            bgColor="bg-blue-50"
          />
          <SummaryCard
            icon={Leaf}
            label="Avg Fertilizer"
            value={`${(progressData.reduce((sum, p) => sum + p.fertilizer_usage, 0) / progressData.length).toFixed(2)} units`}
            color="text-green-600"
            bgColor="bg-green-50"
          />
          <SummaryCard
            icon={TrendingUp}
            label="Avg Health Score"
            value={`${(progressData.reduce((sum, p) => sum + p.plant_health_avg, 0) / progressData.length * 100).toFixed(1)}%`}
            color="text-purple-600"
            bgColor="bg-purple-50"
          />
        </div>
      )}

      {/* Charts */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* Water & Fertilizer Usage */}
        <div className="bg-white rounded-xl shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4 text-gray-800">Water & Fertilizer Usage</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="week" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="water" fill="#3b82f6" name="Water (L/day)" />
              <Bar dataKey="fertilizer" fill="#10b981" name="Fertilizer (units)" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Plant Health Trend */}
        <div className="bg-white rounded-xl shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4 text-gray-800">Plant Health Trend</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="week" />
              <YAxis domain={[0, 100]} />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="health" stroke="#8b5cf6" strokeWidth={2} name="Health (%)" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Weekly Improvement Score */}
      <div className="bg-white rounded-xl shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4 text-gray-800">Weekly Improvement Score</h2>
        <div className="grid md:grid-cols-4 gap-4">
          {chartData.map((item, idx) => {
            const prevHealth = idx > 0 ? parseFloat(chartData[idx - 1].health) : parseFloat(item.health)
            const improvement = parseFloat(item.health) - prevHealth
            return (
              <div key={idx} className="text-center p-4 bg-gray-50 rounded-lg">
                <p className="text-sm text-gray-600 mb-2">{item.week}</p>
                <p className={`text-2xl font-bold ${improvement >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                  {improvement >= 0 ? '+' : ''}{improvement.toFixed(1)}%
                </p>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}

function SummaryCard({ icon: Icon, label, value, color, bgColor }) {
  return (
    <div className={`${bgColor} rounded-xl p-6`}>
      <div className="flex items-center space-x-3 mb-2">
        <Icon className={color} size={24} />
        <span className="text-gray-600 font-medium">{label}</span>
      </div>
      <p className="text-3xl font-bold text-gray-800">{value}</p>
    </div>
  )
}

