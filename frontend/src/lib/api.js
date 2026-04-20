/**
 * api.js — capa de comunicación con el backend de Guardián Silobolsa.
 * Todas las llamadas HTTP pasan por aquí. Las rutas usan /api/v1 que
 * Vite proxea al backend en desarrollo, y Nginx en producción (Docker).
 */

const BASE = '/api/v1'

async function request(method, path, body) {
  const opts = {
    method,
    credentials: 'include',          // envía la cookie JWT en cada request
    headers: { 'Content-Type': 'application/json' },
  }
  if (body !== undefined) opts.body = JSON.stringify(body)

  const res = await fetch(BASE + path, opts)

  if (!res.ok) {
    let msg = `Error ${res.status}`
    try { const data = await res.json(); msg = data.message || data.detail || msg } catch {}
    throw new Error(msg)
  }

  if (res.status === 204) return null
  return res.json()
}

const get  = (path)        => request('GET',    path)
const post = (path, body)  => request('POST',   path, body)
const put  = (path, body)  => request('PUT',    path, body)
const patch= (path, body)  => request('PATCH',  path, body)
const del  = (path)        => request('DELETE', path)

// ── Auth ──────────────────────────────────────────────────────────────────────
export const login    = (email, password)                    => post('/users/login',  { email, password })
export const signup   = (nombre, apellido, email, password, telefono) =>
                          post('/users/signup', { nombre, apellido, email, password, telefono })
export const logout   = ()                                   => post('/users/logout')

// ── Campos ────────────────────────────────────────────────────────────────────
export const getCampos   = ()                   => get('/campos/')
export const getCampo    = (id)                 => get(`/campos/${id}`)
export const createCampo = (nombre, ubicacion)  => post('/campos/create', { nombre, ubicacion })
export const updateCampo = (id, data)           => put(`/campos/update/${id}`, data)
export const deleteCampo = (id)                 => del(`/campos/delete/${id}`)

// ── Silobolsas ────────────────────────────────────────────────────────────────
export const getSilos      = ()              => get('/silos/')
export const getSilo       = (id)            => get(`/silos/${id}`)
export const createSilo    = (campoId, data) => post(`/silos/create/${campoId}`, data)
export const updateSilo    = (id, data)      => put(`/silos/update/${id}`, data)
export const deleteSilo    = (id)            => del(`/silos/delete/${id}`)
export const setearSensor  = (silobolsaId, sensor_id) =>
                               post('/silos/setear-sensor', { silobolsaId, sensor_id })
export const getSiloTelemetry = (siloId)    => get(`/silos/${siloId}/telemetry`)

// ── Sensores ──────────────────────────────────────────────────────────────────
export const getSensores  = ()               => get('/sensors/')
export const getSensor    = (id)             => get(`/sensors/${id}`)
export const createSensor = (campoId, data)  => post(`/sensors/create/${campoId}`, data)
export const updateSensor = (id, data)       => put(`/sensors/update/${id}`, data)
export const deleteSensor = (id)             => del(`/sensors/delete/${id}`)

// ── Alertas ───────────────────────────────────────────────────────────────────
export const getAlertas        = ()  => get('/alertas/')
export const marcarAlertaVista = (id) => patch(`/alertas/${id}/vista`)
