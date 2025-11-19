import { analyzePlantImage } from '../../services/plantAnalysisApi'
import { DataStore } from './DataStore'

const clamp = (value, min = 0, max = 100) => {
  if (typeof value !== 'number' || Number.isNaN(value)) return min
  return Math.min(Math.max(value, min), max)
}

const percentageFromProfile = (profile) => {
  if (!profile || typeof profile !== 'object') return null
  const values = Object.values(profile)
    .map((item) => {
      if (typeof item === 'number') return item
      if (typeof item?.value === 'number') return item.value
      return null
    })
    .filter((value) => typeof value === 'number')

  if (!values.length) return null
  const avg = values.reduce((acc, value) => acc + value, 0) / values.length
  return clamp(Math.round(avg * 100))
}

const derivePlantStatus = (healthScore, moisture, diseaseProbability) => {
  if (healthScore <= 35 || diseaseProbability >= 70 || moisture <= 20) return 'Critical'
  if (healthScore <= 65 || diseaseProbability >= 40 || moisture <= 35) return 'Warning'
  return 'Healthy'
}

const getDiseaseProbability = (payload) => {
  const diseases = payload?.detected_diseases || payload?.diseases || []
  if (!diseases.length) {
    const nitrogenProbability = payload?.nitrogen_deficiency_probability
    return typeof nitrogenProbability === 'number'
      ? clamp(Math.round(nitrogenProbability * 100))
      : 5
  }

  const best = diseases.reduce((acc, disease) => {
    const probability = typeof disease?.probability === 'number'
      ? disease.probability
      : (disease?.confidence || 0)
    return probability > acc ? probability : acc
  }, 0)

  return clamp(Math.round(best * 100))
}

const normalizeResult = (payload, imageSource, originalFile) => {
  const healthScore = clamp(payload?.plant_health_score ?? 0, 0, 100)
  const moisture = clamp(
    typeof payload?.soil_moisture_percent === 'number'
      ? payload.soil_moisture_percent
      : payload?.water_level_percent ?? 0,
    0,
    100,
  )
  const nutrientLevel = percentageFromProfile(payload?.nutrient_profile)
    ?? clamp(100 - (payload?.fertilizer_need_percent ?? 40))
  const diseaseProbability = getDiseaseProbability(payload)

  return {
    imageSource,
    imagePath: payload?.image_path || null,
    filename: originalFile?.name || payload?.analysis_id?.toString() || 'image',
    timestamp: payload?.timestamp || new Date().toISOString(),
    moistureLevel: moisture,
    nutrientLevel,
    soilCondition: payload?.soil_quality || 'unknown',
    diseaseProbability,
    recommendedActions: Array.isArray(payload?.recommendations) ? payload.recommendations : [],
    plantStatus: derivePlantStatus(healthScore, moisture, diseaseProbability),
    metrics: {
      healthScore,
      waterNeeds: payload?.water_needs ?? 0,
      drynessFactor: payload?.dryness_factor ?? 0,
      fertilizerNeedPercent: payload?.fertilizer_need_percent ?? null,
    },
    // Advanced features data
    advanced: {
      diseaseProbability: payload?.disease_probability ?? diseaseProbability,
      predictedDiseases: payload?.predicted_diseases ?? [],
      soilPh: payload?.soil_ph,
      soilNitrogen: payload?.soil_nitrogen,
      soilPhosphorus: payload?.soil_phosphorus,
      soilPotassium: payload?.soil_potassium,
      nitrogenLevel: payload?.nitrogen_level,
      phosphorusLevel: payload?.phosphorus_level,
      potassiumLevel: payload?.potassium_level,
      recommendedFertilizerAmount: payload?.recommended_fertilizer_amount,
      fertilizerType: payload?.fertilizer_type,
      irrigationNeeded: payload?.irrigation_needed,
      irrigationDurationMinutes: payload?.irrigation_duration_minutes,
      warnings: payload?.warnings ?? {},
      temperatureAlert: payload?.temperature_alert,
      waterAlert: payload?.water_alert,
      fertilizerAlert: payload?.fertilizer_alert,
      diseaseAlert: payload?.disease_alert,
      estimatedWaterCost: payload?.estimated_water_cost,
      estimatedFertilizerCost: payload?.estimated_fertilizer_cost,
      costSavings: payload?.cost_savings,
      efficiencyPercentage: payload?.efficiency_percentage,
      aiSummaryArabic: payload?.ai_summary_arabic,
      aiSummaryEnglish: payload?.ai_summary_english,
      leafDamagePercent: payload?.leaf_damage_percent,
    },
    aiPayload: payload,
  }
}

const fileToBase64 = (file) => new Promise((resolve, reject) => {
  const reader = new FileReader()
  reader.onload = () => resolve(reader.result)
  reader.onerror = (error) => reject(error)
  reader.readAsDataURL(file)
})

export const ImageAnalyzer = {
  async analyze(file) {
    if (!file) throw new Error('No file provided for analysis.')
    const imageSource = await fileToBase64(file)
    const freshResult = await analyzePlantImage(file)
    const normalized = normalizeResult(freshResult, imageSource, file)
    DataStore.addResult(normalized)
    return normalized
  },
}


