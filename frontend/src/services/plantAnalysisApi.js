import api from './api'

export const analyzePlantImage = async (imageFile, plantType) => {
  const formData = new FormData()
  formData.append('file', imageFile)
  if (plantType) {
    formData.append('plant_type', plantType)
  }

  const response = await api.post('/analysis/analyze_image', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
      'Cache-Control': 'no-cache',
    },
    params: {
      ts: Date.now(),
    },
  })

  return response.data
}
