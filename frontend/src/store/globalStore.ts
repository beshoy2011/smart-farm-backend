import { create } from 'zustand'

type NutrientValue = {
  level?: string
  value?: number
}

export interface PlantDataPayload {
  analysis_id?: number
  user_id?: number
  image_path?: string
  plant_type?: string | null
  plant_health_score?: number
  water_needs?: number
  soil_quality?: string
  fertilizer_deficiency?: Record<string, string>
  detected_diseases?: Array<Record<string, any>>
  diseases?: Array<Record<string, any>>
  pests?: Record<string, any>
  recommendations?: Array<Record<string, any>>
  nutrient_profile?: Record<string, NutrientValue>
  water_level_percent?: number
  soil_moisture_percent?: number
  fertilizer_need_percent?: number
  leaf_color_index?: number
  dryness_factor?: number
  nitrogen_deficiency_probability?: number
  growth_stage?: Record<string, any>
  explainability?: Record<string, any>
  analysis_metadata?: Record<string, any>
  timestamp?: string
  created_at?: string
}

interface FarmAIState {
  plantData: PlantDataPayload | null
  lastUpdated: string | null
  isProcessing: boolean
  error: string | null
  setPlantData: (payload: PlantDataPayload | null) => void
  setProcessing: (state: boolean) => void
  setError: (message: string | null) => void
  reset: () => void
}

const STORAGE_KEY = 'smartfarm-ai-global-store'

const loadFromStorage = () => {
  if (typeof window === 'undefined') {
    return { plantData: null, lastUpdated: null }
  }

  try {
    const cached = window.localStorage.getItem(STORAGE_KEY)
    if (!cached) return { plantData: null, lastUpdated: null }
    return JSON.parse(cached)
  } catch {
    return { plantData: null, lastUpdated: null }
  }
}

const persistToStorage = (data: { plantData: PlantDataPayload | null, lastUpdated: string | null }) => {
  if (typeof window === 'undefined') return
  try {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(data))
  } catch {
    // Swallow storage errors silently
  }
}

const initialState = loadFromStorage()

export const useFarmAI = create<FarmAIState>((set) => ({
  plantData: initialState.plantData,
  lastUpdated: initialState.lastUpdated,
  isProcessing: false,
  error: null,
  setPlantData: (payload) => {
    const nextTimestamp = payload ? new Date().toISOString() : null
    set({
      plantData: payload,
      lastUpdated: nextTimestamp,
      isProcessing: false,
      error: null,
    })
    persistToStorage({ plantData: payload, lastUpdated: nextTimestamp })
  },
  setProcessing: (state) => set({ isProcessing: state }),
  setError: (message) => set({ error: message }),
  reset: () => {
    persistToStorage({ plantData: null, lastUpdated: null })
    set({ plantData: null, lastUpdated: null, error: null, isProcessing: false })
  },
}))

