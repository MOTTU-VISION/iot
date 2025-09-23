export type Cam = {
  id: string,
  name: string,
  status: string,
  location: string,
}

export type Alerts = {
  placa: string,
  alert: string,
  camera_id: string,
  timestamp: string,
  severity: Severity
}

export type Records = {
  placa: string,
  label: string
  timestamp: string,
  camera_id: string,
  bounding_box: number[],
}

export enum Severity {
  low = "low",
  high = "high",
  medium = "medium",
}