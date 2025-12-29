import { useEffect, useState, useRef } from 'react'
import { useAuthStore } from '../store/authStore'

export function useWebSocket() {
  const [data, setData] = useState(null)
  const [isConnected, setIsConnected] = useState(false)
  const wsRef = useRef(null)
  const { user } = useAuthStore()

  useEffect(() => {
    if (!user?.id) {
      setIsConnected(false)
      return
    }

    let ws = null
    let pingInterval = null
    let reconnectTimeout = null
    let isMounted = true

    const connect = () => {
      if (!isMounted || !user?.id) return

      try {
        // Get WebSocket URL from environment or use default
        const wsUrl = import.meta.env.VITE_WS_URL || `ws://localhost:8000/ws/monitoring/${user.id}`
        
        ws = new WebSocket(wsUrl)
        wsRef.current = ws

        // Set timeout to close if connection takes too long
        const connectionTimeout = setTimeout(() => {
          if (ws && ws.readyState === WebSocket.CONNECTING) {
            ws.close()
            setIsConnected(false)
          }
        }, 5000) // 5 second timeout

        ws.onopen = () => {
          clearTimeout(connectionTimeout)
          if (isMounted) {
            setIsConnected(true)
            console.log('WebSocket connected')
          }

          // Send ping every 30 seconds to keep connection alive
          pingInterval = setInterval(() => {
            if (ws && ws.readyState === WebSocket.OPEN && isMounted) {
              try {
                ws.send('ping')
              } catch (e) {
                console.error('Error sending ping:', e)
              }
            }
          }, 30000)
        }

        ws.onmessage = (event) => {
          if (!isMounted) return
          try {
            const message = JSON.parse(event.data)
            setData(message)
          } catch (error) {
            console.error('Error parsing WebSocket message:', error)
          }
        }

        ws.onerror = (error) => {
          clearTimeout(connectionTimeout)
          if (isMounted) {
            console.error('WebSocket error:', error)
            setIsConnected(false)
          }
        }

        ws.onclose = () => {
          clearTimeout(connectionTimeout)
          if (pingInterval) {
            clearInterval(pingInterval)
            pingInterval = null
          }
          
          if (isMounted) {
            setIsConnected(false)
            console.log('WebSocket closed')
            
            // Try to reconnect after 10 seconds (only if still mounted and user exists)
            reconnectTimeout = setTimeout(() => {
              if (isMounted && user?.id) {
                connect()
              }
            }, 10000)
          }
        }
      } catch (error) {
        console.error('Error creating WebSocket:', error)
        if (isMounted) {
          setIsConnected(false)
          // Retry after 10 seconds
          reconnectTimeout = setTimeout(() => {
            if (isMounted && user?.id) {
              connect()
            }
          }, 10000)
        }
      }
    }

    // Initial connection
    connect()

    return () => {
      isMounted = false
      
      if (reconnectTimeout) {
        clearTimeout(reconnectTimeout)
      }
      
      if (pingInterval) {
        clearInterval(pingInterval)
      }
      
      if (ws) {
        try {
          if (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING) {
            ws.close()
          }
        } catch (e) {
          // Ignore errors on cleanup
        }
        wsRef.current = null
      }
    }
  }, [user?.id])

  return { data, isConnected, sendMessage: (msg) => wsRef.current?.send(msg) }
}

