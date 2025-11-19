import { useState } from 'react'
import { Search, Leaf, Droplet, Sun, Thermometer } from 'lucide-react'

const plantDatabase = [
  {
    id: 1,
    name: 'Tomato',
    nameAr: 'طماطم',
    description: 'Popular vegetable crop requiring regular watering and full sun',
    waterNeeds: '2-3 L/day',
    temperature: '18-25°C',
    sunlight: 'Full sun',
    careTips: [
      'Water deeply but infrequently',
      'Provide support for growing plants',
      'Fertilize every 2-3 weeks',
      'Watch for aphids and blight'
    ]
  },
  {
    id: 2,
    name: 'Lettuce',
    nameAr: 'خس',
    description: 'Cool-season crop perfect for salads',
    waterNeeds: '1-2 L/day',
    temperature: '10-20°C',
    sunlight: 'Partial shade',
    careTips: [
      'Keep soil consistently moist',
      'Harvest outer leaves first',
      'Protect from heat',
      'Fertilize with nitrogen-rich fertilizer'
    ]
  },
  {
    id: 3,
    name: 'Pepper',
    nameAr: 'فلفل',
    description: 'Warm-season crop with various heat levels',
    waterNeeds: '2-2.5 L/day',
    temperature: '20-30°C',
    sunlight: 'Full sun',
    careTips: [
      'Water regularly but avoid overwatering',
      'Provide consistent moisture',
      'Fertilize monthly',
      'Support plants as they grow'
    ]
  },
  {
    id: 4,
    name: 'Cucumber',
    nameAr: 'خيار',
    description: 'Fast-growing vine crop',
    waterNeeds: '2.5-3 L/day',
    temperature: '20-25°C',
    sunlight: 'Full sun',
    careTips: [
      'Water deeply and regularly',
      'Provide trellis support',
      'Harvest frequently',
      'Watch for powdery mildew'
    ]
  }
]

export default function PlantsLibrary() {
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedPlant, setSelectedPlant] = useState(null)

  const filteredPlants = plantDatabase.filter(plant =>
    plant.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    plant.nameAr.includes(searchTerm)
  )

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-800 mb-2">Plants Library</h1>
        <p className="text-gray-600">مكتبة النباتات والمعلومات</p>
      </div>

      {/* Search */}
      <div className="bg-white rounded-xl shadow-md p-4">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
          <input
            type="text"
            placeholder="Search plants..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
          />
        </div>
      </div>

      {/* Plants Grid */}
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredPlants.map(plant => (
          <PlantCard
            key={plant.id}
            plant={plant}
            onClick={() => setSelectedPlant(plant)}
          />
        ))}
      </div>

      {/* Plant Detail Modal */}
      {selectedPlant && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50" onClick={() => setSelectedPlant(null)}>
          <div className="bg-white rounded-xl shadow-2xl max-w-2xl w-full p-6 max-h-[90vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
            <div className="flex justify-between items-start mb-4">
              <div>
                <h2 className="text-2xl font-bold text-gray-800">{selectedPlant.name}</h2>
                <p className="text-gray-600">{selectedPlant.nameAr}</p>
              </div>
              <button
                onClick={() => setSelectedPlant(null)}
                className="text-gray-400 hover:text-gray-600 text-2xl"
              >
                ×
              </button>
            </div>

            <p className="text-gray-700 mb-6">{selectedPlant.description}</p>

            <div className="grid md:grid-cols-3 gap-4 mb-6">
              <InfoCard icon={Droplet} label="Water Needs" value={selectedPlant.waterNeeds} />
              <InfoCard icon={Thermometer} label="Temperature" value={selectedPlant.temperature} />
              <InfoCard icon={Sun} label="Sunlight" value={selectedPlant.sunlight} />
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-3 text-gray-800">Care Tips</h3>
              <ul className="space-y-2">
                {selectedPlant.careTips.map((tip, idx) => (
                  <li key={idx} className="flex items-start space-x-2">
                    <Leaf className="text-green-600 mt-1" size={18} />
                    <span className="text-gray-700">{tip}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

function PlantCard({ plant, onClick }) {
  return (
    <div
      onClick={onClick}
      className="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition cursor-pointer"
    >
      <div className="flex items-center space-x-4 mb-4">
        <div className="w-16 h-16 bg-primary-100 rounded-lg flex items-center justify-center">
          <Leaf className="text-primary-600" size={32} />
        </div>
        <div>
          <h3 className="text-xl font-semibold text-gray-800">{plant.name}</h3>
          <p className="text-gray-600">{plant.nameAr}</p>
        </div>
      </div>
      <p className="text-gray-700 mb-4">{plant.description}</p>
      <div className="flex items-center space-x-4 text-sm text-gray-600">
        <span className="flex items-center space-x-1">
          <Droplet size={16} />
          <span>{plant.waterNeeds}</span>
        </span>
        <span className="flex items-center space-x-1">
          <Thermometer size={16} />
          <span>{plant.temperature}</span>
        </span>
      </div>
    </div>
  )
}

function InfoCard({ icon: Icon, label, value }) {
  return (
    <div className="bg-gray-50 rounded-lg p-4">
      <div className="flex items-center space-x-2 mb-2">
        <Icon className="text-primary-600" size={20} />
        <span className="text-gray-600 font-medium">{label}</span>
      </div>
      <p className="text-lg font-semibold text-gray-800">{value}</p>
    </div>
  )
}

