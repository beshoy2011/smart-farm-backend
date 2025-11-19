import { useSyncExternalStore } from 'react'

// Get current user ID - we'll use a simple approach with a global variable
// that gets updated when user changes
let currentUserId = null

// Function to set current user ID (called from auth store)
export const setCurrentUserId = (userId) => {
  const oldUserId = currentUserId
  currentUserId = userId
  // If user changed, reload cache
  if (oldUserId !== userId) {
    lastUserId = userId
    cache = readStorage()
    notify() // Notify listeners of the change
  }
}

// Get current user ID
const getUserId = () => {
  if (typeof window === 'undefined') return null
  // Try to get from auth token if available
  try {
    const token = localStorage.getItem('auth_token')
    if (token) {
      // If we have a stored user ID, use it
      if (currentUserId) return currentUserId
      // Otherwise try to get from a separate storage
      const storedUserId = localStorage.getItem('current_user_id')
      return storedUserId ? parseInt(storedUserId) : null
    }
  } catch {
    return null
  }
  return null
}

const getStorageKey = () => {
  const userId = getUserId()
  return userId ? `smartfarm:analysis-results:v2:user:${userId}` : 'smartfarm:analysis-results:v2:guest'
}

const EVENT_NAME = 'smartfarm:data-updated'

const isBrowser = typeof window !== 'undefined'
const listeners = new Set()
let broadcastChannel = null

if (isBrowser && 'BroadcastChannel' in window) {
  broadcastChannel = new BroadcastChannel('smartfarm-analysis-sync')
}

const readStorage = () => {
  if (!isBrowser) return []
  try {
    const storageKey = getStorageKey()
    const payload = window.localStorage.getItem(storageKey)
    if (!payload) return []
    const parsed = JSON.parse(payload)
    return Array.isArray(parsed) ? parsed : []
  } catch {
    return []
  }
}

let cache = readStorage()
let lastUserId = getUserId() // Track last user ID to detect user changes

// Function to reload cache when user changes
const reloadCache = () => {
  const currentUserId = getUserId()
  if (currentUserId !== lastUserId) {
    lastUserId = currentUserId
    cache = readStorage()
  }
}

const persist = (next) => {
  cache = next
  if (isBrowser) {
    const storageKey = getStorageKey()
    window.localStorage.setItem(storageKey, JSON.stringify(next))
  }
}

const notify = (detail = null) => {
  listeners.forEach((listener) => listener(cache))
  if (isBrowser) {
    window.dispatchEvent(new CustomEvent(EVENT_NAME, { detail: detail || cache[0] || null }))
  }
  if (broadcastChannel) {
    broadcastChannel.postMessage({ type: 'sync', payload: cache })
  }
}

if (isBrowser) {
  window.addEventListener('storage', (event) => {
    const storageKey = getStorageKey()
    if (!event.key?.startsWith('smartfarm:analysis-results:v2') || !event.newValue) return
    if (event.key !== storageKey) return
    try {
      cache = JSON.parse(event.newValue) || []
    } catch {
      cache = []
    }
    listeners.forEach((listener) => listener(cache))
    window.dispatchEvent(new CustomEvent(EVENT_NAME, { detail: cache[0] || null }))
  })
  
  // Listen for auth token changes to reload cache when user changes
  window.addEventListener('storage', (event) => {
    if (event.key === 'auth_token' || event.key === 'current_user_id') {
      // User changed, reload cache
      const newUserId = getUserId()
      if (newUserId !== lastUserId) {
        lastUserId = newUserId
        cache = readStorage()
        listeners.forEach((listener) => listener(cache))
        window.dispatchEvent(new CustomEvent(EVENT_NAME, { detail: cache[0] || null }))
      }
    }
  })

  if (broadcastChannel) {
    broadcastChannel.addEventListener('message', (event) => {
      if (event?.data?.type !== 'sync') return
      if (!Array.isArray(event.data.payload)) return
      cache = event.data.payload
      listeners.forEach((listener) => listener(cache))
      window.dispatchEvent(new CustomEvent(EVENT_NAME, { detail: cache[0] || null }))
    })
  }
}

const createId = () => {
  if (typeof crypto !== 'undefined' && crypto.randomUUID) {
    return crypto.randomUUID()
  }
  return `${Date.now()}-${Math.random().toString(16).slice(2)}`
}

const buildRecord = (payload) => ({
  id: createId(),
  createdAt: new Date().toISOString(),
  ...payload,
})

export const DataStore = {
  getAll: () => {
    // Only reload if user changed, otherwise return cached data
    reloadCache()
    return cache
  },
  getLatest: () => {
    // Only reload if user changed, otherwise return cached data
    reloadCache()
    return cache[0] || null
  },
  addResult: (entry) => {
    // Reload to ensure we have current user's data
    reloadCache()
    const record = buildRecord(entry)
    const next = [record, ...cache]
    persist(next)
    cache = next
    notify(record)
    return record
  },
  replaceAll: (entries) => {
    persist(entries)
    cache = entries
    notify()
  },
  clear: () => {
    persist([])
    cache = []
    notify()
  },
  clearForUser: (userId) => {
    // Clear data for a specific user (only if explicitly requested)
    if (isBrowser && userId) {
      const userKey = `smartfarm:analysis-results:v2:user:${userId}`
      window.localStorage.removeItem(userKey)
    }
    cache = []
    notify()
  },
  subscribe: (listener) => {
    listeners.add(listener)
    return () => listeners.delete(listener)
  },
}

export const useAnalysisFeed = () => {
  const results = useSyncExternalStore(
    DataStore.subscribe,
    () => DataStore.getAll(),
    () => DataStore.getAll(),
  )

  return {
    results,
    latest: results[0] || null,
  }
}

export const getEventName = () => EVENT_NAME

