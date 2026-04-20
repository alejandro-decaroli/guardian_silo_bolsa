import { writable, derived } from 'svelte/store'
import * as api from '../api.js'

// ── Auth ──────────────────────────────────────────────────────────────────────
export const currentUser     = writable(null)
export const isAuthenticated = derived(currentUser, $u => !!$u)

// ── Data stores ───────────────────────────────────────────────────────────────
export const campos     = writable([])
export const silobolsas = writable([])
export const sensores   = writable([])
export const alertas    = writable([])

// ── Toast ─────────────────────────────────────────────────────────────────────
export const toasts = writable([])

export function addToast(message, type = 'success', duration = 3500) {
  const id = Date.now()
  toasts.update(t => [...t, { id, message, type }])
  setTimeout(() => toasts.update(t => t.filter(x => x.id !== id)), duration)
}

// ── Auth actions ──────────────────────────────────────────────────────────────
export async function loginUser(email, password) {
  const { user } = await api.login(email, password)
  currentUser.set(user)
  await loadDashboardData()
}

export async function signupUser(nombre, apellido, email, password, telefono) {
  const { user } = await api.signup(nombre, apellido, email, password, telefono)
  currentUser.set(user)
  await loadDashboardData()
}

export async function logoutUser() {
  await api.logout()
  currentUser.set(null)
  campos.set([])
  silobolsas.set([])
  sensores.set([])
  alertas.set([])
}

// ── Data loading ──────────────────────────────────────────────────────────────
export async function loadDashboardData() {
  const [rawCampos, rawSilos, rawSensores, rawAlertas] = await Promise.all([
    api.getCampos(),
    api.getSilos(),
    api.getSensores(),
    api.getAlertas(),
  ])
  campos.set(rawCampos     ?? [])
  silobolsas.set(rawSilos  ?? [])
  sensores.set(rawSensores ?? [])
  alertas.set(rawAlertas   ?? [])
}

// ── Campos CRUD ───────────────────────────────────────────────────────────────
export async function crearCampo(nombre, ubicacion) {
  const campo = await api.createCampo(nombre, ubicacion)
  campos.update(cs => [...cs, campo])
  return campo.id
}

// ── Silobolsas CRUD ───────────────────────────────────────────────────────────
export async function crearSilobolsa(campoId, datos) {
  const payload = {
    marca:         datos.marca,
    capacidad_max: Number(datos.capacidad),
    almacenado:    Number(datos.capacidad),
    grano:         datos.grano.toUpperCase(),
    ubicacion:     datos.ubicacion,
    observaciones: datos.observaciones ?? '',
  }
  const silo = await api.createSilo(campoId, payload)
  silobolsas.update(ss => [...ss, silo])
  return silo.id
}

// ── Sensores CRUD ─────────────────────────────────────────────────────────────
export async function crearSensor(campoId, datos) {
  const payload = {
    modelo:      datos.modelo,
    mac_address: datos.mac,
    estado:      'ACTIVO',
  }
  const sensor = await api.createSensor(campoId, payload)
  sensores.update(ss => [...ss, sensor])
  return sensor.id
}

// ── Vincular sensor ───────────────────────────────────────────────────────────
export async function vincularSensor(silobolsaId, sensorId) {
  await api.setearSensor(silobolsaId, sensorId)
  silobolsas.update(ss =>
    ss.map(s => s.id === silobolsaId ? { ...s, sensor_id: sensorId } : s)
  )
}

// ── Alertas ───────────────────────────────────────────────────────────────────
export async function marcarVista(alertaId) {
  const updated = await api.marcarAlertaVista(alertaId)
  alertas.update(as => as.map(a => a.id === alertaId ? updated : a))
}
