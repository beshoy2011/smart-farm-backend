import { CheckCircle, AlertTriangle, Droplet, Leaf, Bug, FileText } from 'lucide-react'

export default function ResultCard({ results }) {
  const healthScore = results.plant_health_score || 0
  const healthColor = healthScore > 0.7 ? 'text-green-600' : healthScore > 0.4 ? 'text-yellow-600' : 'text-red-600'
  const healthStatus = healthScore > 0.7 ? 'Healthy' : healthScore > 0.4 ? 'Moderate' : 'Poor'

  return (
    <div className="bg-white rounded-xl shadow-md p-6 space-y-6">
      <h2 className="text-2xl font-bold text-gray-800">Analysis Results</h2>

      {/* Health Score */}
      <div className="bg-gradient-to-r from-primary-50 to-secondary-50 rounded-lg p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-xl font-semibold text-gray-800">Plant Health Score</h3>
          <span className={`text-3xl font-bold ${healthColor}`}>
            {(healthScore * 100).toFixed(1)}%
          </span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-4">
          <div
            className={`h-4 rounded-full transition-all ${
              healthScore > 0.7 ? 'bg-green-500' : healthScore > 0.4 ? 'bg-yellow-500' : 'bg-red-500'
            }`}
            style={{ width: `${healthScore * 100}%` }}
          />
        </div>
        <p className="mt-2 text-gray-600">Status: <span className="font-semibold">{healthStatus}</span></p>
      </div>

      {/* Key Metrics Grid */}
      <div className="grid md:grid-cols-3 gap-4">
        <MetricCard
          icon={Droplet}
          label="Water Needs"
          value={`${results.water_needs?.toFixed(2) || 'N/A'} L/day`}
          color="text-blue-600"
        />
        <MetricCard
          icon={Leaf}
          label="Soil Quality"
          value={results.soil_quality || 'N/A'}
          color="text-green-600"
        />
        <MetricCard
          icon={Bug}
          label="Pests Detected"
          value={results.pests?.length || 0}
          color="text-red-600"
        />
      </div>

      {/* Recommendations */}
      {results.recommendations && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center space-x-2">
            <FileText size={20} />
            <span>Recommendations</span>
          </h3>
          <div className="space-y-3">
            {results.recommendations.water?.map((rec, idx) => (
              <div key={idx} className="flex items-start space-x-2">
                <Droplet className="text-blue-600 mt-1" size={18} />
                <p className="text-gray-700">{rec}</p>
              </div>
            ))}
            {results.recommendations.fertilizer?.map((rec, idx) => (
              <div key={idx} className="flex items-start space-x-2">
                <Leaf className="text-green-600 mt-1" size={18} />
                <p className="text-gray-700">{rec}</p>
              </div>
            ))}
            {results.recommendations.urgent?.map((rec, idx) => (
              <div key={idx} className="flex items-start space-x-2">
                <AlertTriangle className="text-red-600 mt-1" size={18} />
                <p className="text-gray-700 font-semibold">{rec}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Diseases & Pests */}
      {(results.diseases?.length > 0 || results.pests?.length > 0) && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-red-800 mb-4">Issues Detected</h3>
          {results.diseases?.length > 0 && (
            <div className="mb-4">
              <p className="font-semibold text-red-700 mb-2">Diseases:</p>
              <ul className="list-disc list-inside text-red-600">
                {results.diseases.map((disease, idx) => (
                  <li key={idx}>{disease.name || disease}</li>
                ))}
              </ul>
            </div>
          )}
          {results.pests?.length > 0 && (
            <div>
              <p className="font-semibold text-red-700 mb-2">Pests:</p>
              <ul className="list-disc list-inside text-red-600">
                {results.pests.map((pest, idx) => (
                  <li key={idx}>{pest.name || pest}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

function MetricCard({ icon: Icon, label, value, color }) {
  return (
    <div className="bg-gray-50 rounded-lg p-4">
      <div className="flex items-center space-x-3 mb-2">
        <Icon className={color} size={24} />
        <span className="text-gray-600 font-medium">{label}</span>
      </div>
      <p className={`text-2xl font-bold ${color}`}>{value}</p>
    </div>
  )
}

