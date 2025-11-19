import { useState } from 'react'
import { FileText, Download, Calendar } from 'lucide-react'
import api from '../services/api'

export default function Reports() {
  const [days, setDays] = useState(30)
  const [generating, setGenerating] = useState(false)

  const handleGenerateReport = async () => {
    setGenerating(true)
    try {
      const response = await api.get(`/reports/generate-pdf?days=${days}`, {
        responseType: 'blob'
      })

      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `smartfarm_report_${new Date().toISOString().split('T')[0]}.pdf`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)
    } catch (error) {
      console.error('Failed to generate report:', error)
      alert('Failed to generate report. Please try again.')
    } finally {
      setGenerating(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-800 mb-2">Reports</h1>
        <p className="text-gray-600">التقارير والإحصائيات</p>
      </div>

      <div className="bg-white rounded-xl shadow-md p-6">
        <div className="flex items-center space-x-3 mb-6">
          <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
            <FileText className="text-primary-600" size={24} />
          </div>
          <div>
            <h2 className="text-xl font-semibold text-gray-800">Generate PDF Report</h2>
            <p className="text-gray-600">Create a comprehensive report of your farm's performance</p>
          </div>
        </div>

        <div className="space-y-4">
          <div>
            <label className="block text-gray-700 font-semibold mb-2">
              Report Period
            </label>
            <div className="flex items-center space-x-4">
              <Calendar className="text-gray-400" size={20} />
              <select
                value={days}
                onChange={(e) => setDays(parseInt(e.target.value))}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              >
                <option value={7}>Last 7 days</option>
                <option value={30}>Last 30 days</option>
                <option value={60}>Last 60 days</option>
                <option value={90}>Last 90 days</option>
              </select>
            </div>
          </div>

          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h3 className="font-semibold text-blue-800 mb-2">Report Includes:</h3>
            <ul className="list-disc list-inside text-blue-700 space-y-1">
              <li>Summary statistics (total analyses, average health score)</li>
              <li>Water usage trends</li>
              <li>Recent analysis results</li>
              <li>Recommendations and insights</li>
            </ul>
          </div>

          <button
            onClick={handleGenerateReport}
            disabled={generating}
            className="w-full md:w-auto px-8 py-3 bg-primary-500 text-white rounded-lg font-semibold hover:bg-primary-600 transition flex items-center justify-center space-x-2 disabled:opacity-50"
          >
            {generating ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                <span>Generating...</span>
              </>
            ) : (
              <>
                <Download size={20} />
                <span>Generate & Download Report</span>
              </>
            )}
          </button>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4 text-gray-800">Report Features</h2>
        <div className="grid md:grid-cols-2 gap-4">
          <FeatureItem
            title="Comprehensive Statistics"
            description="Detailed metrics and performance indicators"
          />
          <FeatureItem
            title="Visual Charts"
            description="Graphical representation of trends"
          />
          <FeatureItem
            title="Analysis History"
            description="Complete record of all analyses"
          />
          <FeatureItem
            title="Recommendations"
            description="Actionable insights for improvement"
          />
        </div>
      </div>
    </div>
  )
}

function FeatureItem({ title, description }) {
  return (
    <div className="flex items-start space-x-3">
      <div className="w-2 h-2 bg-primary-500 rounded-full mt-2"></div>
      <div>
        <h3 className="font-semibold text-gray-800 mb-1">{title}</h3>
        <p className="text-gray-600 text-sm">{description}</p>
      </div>
    </div>
  )
}

