"use client"
import React, { useState, useEffect } from 'react';
import { Camera, AlertTriangle, FileText, ChevronRight, ChevronLeft, Bell, Clock, Video } from 'lucide-react';


type Cam = {
  id: string,
  name: string,
  location: string,
  status: string,
}

type Alerts = {
  camera_id: string,
  placa: string,
  timestamp: number,
  alert: string,
  severity: Severity
}

type Records = {
  camera_id: string,
  timestamp: number,
  placa: string,
  bounding_box: number[],
  label: string
}

enum Severity {
  low="low",
  high="high",
  medium="medium",
}

const Home = () => {

  const API_BASE = "http://localhost:5000"; // Flask roda nessa porta por padrão

  const [cameras] = useState<Cam[]>([
    { id: 'camera1', name: 'Câmera Entrada', location: 'Hall Principal', status: 'online' },
    { id: 'camera2', name: 'Câmera Estacionamento', location: 'Área Externa', status: 'online' },
    { id: 'camera3', name: 'Câmera Escritório', location: 'Sala 205', status: 'online' },
    { id: 'camera4', name: 'Câmera Depósito', location: 'Térreo', status: 'online' }
  ]);

  const [loading, setLoading] = useState(false);
  const [alertsOpen, setAlertsOpen] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [alerts, setAlerts] = useState<Alerts[]>([]);
  const [records, setRecords] = useState<Records[]>([]);
  const [selectedCamera, setSelectedCamera] = useState('camera1');

  useEffect(() => {
    const fetchRecords = async () => {
      setLoading(true);
      try {
        const res = await fetch(`${API_BASE}/records/${selectedCamera}`);
        const data = await res.json();
        setRecords(data);
      } catch (err) {
        console.error("Erro ao carregar registros:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchRecords();

    // opcional: atualização periódica a cada 5s
    const interval = setInterval(fetchRecords, 5000);
    return () => clearInterval(interval);
  }, [selectedCamera]);
  

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const res = await fetch(`${API_BASE}/alerts`);
        const data = await res.json();
        setAlerts(data);
      } catch (err) {
        console.error("Erro ao carregar alertas:", err);
      }
    };

    fetchAlerts();
    const interval = setInterval(fetchAlerts, 10000); // atualizar a cada 10s
    return () => clearInterval(interval);
  }, []);

  const getSeverityColor = (severity: Severity) => {
    switch (severity) {
      case 'high': return 'text-red-600 bg-red-50';
      case 'medium': return 'text-yellow-600 bg-yellow-50';
      case 'low': return 'text-blue-600 bg-blue-50';
      default: return 'text-gray-600 bg-gray-50';
    }
  };

  return (
    <div className="h-screen bg-gray-50 flex overflow-hidden">
      {/* Sidebar Principal */}
      <div className={`bg-white shadow-lg transition-all duration-300 ${sidebarOpen ? 'w-80' : 'w-0'} overflow-hidden`}>
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-800 flex items-center gap-2">
            <FileText className="w-5 h-5" />
            Registros
          </h2>
        </div>

        <div className="p-4 space-y-3 h-full overflow-y-auto">
          {loading ? (
            <div className="flex items-center justify-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            </div>
          ) : (
            records.map((record) => (
              <div key={record.camera_id} className="bg-gray-50 p-3 rounded-lg border">
                <div className="text-xs text-gray-500 mt-1 flex items-center gap-1">
                  <Clock className="w-3 h-3" />
                  {record.timestamp}
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Área Principal */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="bg-white shadow-sm border-b border-gray-200 p-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            >
              {sidebarOpen ? <ChevronLeft className="w-5 h-5" /> : <ChevronRight className="w-5 h-5" />}
            </button>
            <h1 className="text-xl font-semibold text-gray-800 flex items-center gap-2">
              <Camera className="w-6 h-6 text-blue-600" />
              Sistema de Monitoramento
            </h1>
          </div>

          <button
            onClick={() => setAlertsOpen(true)}
            className="flex items-center gap-2 bg-red-50 text-red-600 px-4 py-2 rounded-lg hover:bg-red-100 transition-colors"
          >
            <Bell className="w-4 h-4" />
            Alertas ({alerts.length})
          </button>
        </div>

        {/* Lista de Câmeras */}
        <div className="p-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4 gap-6">
            {cameras.map((camera) => (
              <div
                key={camera.id}
                className={`bg-white rounded-lg shadow-md overflow-hidden cursor-pointer transition-all duration-200 ${selectedCamera === camera.id ? 'ring-2 ring-blue-500' : 'hover:shadow-lg'
                  }`}
                onClick={() => setSelectedCamera(camera.id)}
              >
                <div className="relative aspect-video bg-gray-900 flex items-center justify-center">
                  {camera.status === 'online' ? (
                    <div className="w-full h-full bg-gradient-to-br from-gray-800 to-gray-900 flex items-center justify-center">
                      <img
                        src={`${API_BASE}/stream/${camera.id}`}
                        alt={`Stream da ${camera.name}`}
                        className="w-full h-full object-cover"
                        onError={(e) => {
                          const img = e.target as HTMLImageElement;
                          img.style.display = 'none';
                          if (img.nextSibling && img.nextSibling instanceof HTMLElement) {
                            (img.nextSibling as HTMLElement).style.display = 'flex';
                          }
                        }}
                      />
                      <div className="hidden w-full h-full bg-gradient-to-br from-blue-600 to-blue-800 items-center justify-center">
                        <Video className="w-12 h-12 text-white opacity-50" />
                      </div>
                    </div>
                  ) : (
                    <div className="w-full h-full bg-gray-600 flex items-center justify-center">
                      <div className="text-center text-white">
                        <Camera className="w-12 h-12 mx-auto mb-2 opacity-50" />
                        <span className="text-sm">Offline</span>
                      </div>
                    </div>
                  )}

                  <div className={`absolute top-2 right-2 w-3 h-3 rounded-full ${camera.status === 'online' ? 'bg-green-400' : 'bg-red-400'
                    }`}></div>
                </div>

                <div className="p-4">
                  <h3 className="font-medium text-gray-900">{camera.name}</h3>
                  <p className="text-sm text-gray-500 mt-1">{camera.location}</p>
                  <div className="flex items-center justify-between mt-3">
                    <span className={`text-xs px-2 py-1 rounded-full ${camera.status === 'online'
                      ? 'bg-green-100 text-green-700'
                      : 'bg-red-100 text-red-700'
                      }`}>
                      {camera.status === 'online' ? 'Online' : 'Offline'}
                    </span>
                    <span className="text-xs text-gray-400">{camera.id}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Painel de Alertas */}
      {alertsOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex justify-end">
          <div className="bg-white w-96 h-full shadow-xl overflow-y-auto">
            <div className="p-6 border-b border-gray-200 flex items-center justify-between">
              <h2 className="text-lg font-semibold text-gray-800 flex items-center gap-2">
                <AlertTriangle className="w-5 h-5 text-red-600" />
                Alertas Ativos
              </h2>
              <button
                onClick={() => setAlertsOpen(false)}
                className="p-2 hover:bg-gray-100 rounded-lg"
              >
                <ChevronRight className="w-5 h-5" />
              </button>
            </div>

            <div className="p-4 space-y-4">
              {alerts.map((alert) => (
                <div key={alert.camera_id} className={`p-4 rounded-lg border ${getSeverityColor(alert.severity)}`}>
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <p className="font-medium">{alert.alert}</p>
                      <p className="text-sm mt-1">Câmera: {cameras.find(c => c.id === alert.camera_id)?.name}</p>
                      <p className="text-xs mt-2 flex items-center gap-1">
                        <Clock className="w-3 h-3" />
                        {alert.timestamp}
                      </p>
                    </div>
                    <AlertTriangle className="w-5 h-5 flex-shrink-0" />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Home;