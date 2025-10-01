"use client";
import { Header } from "@/components/Header/Header";
import { Sidebar } from "@/components/Sidebar/Sidebar";
import { apiClient } from "@/api/apiClient";
import { CameraCard } from "@/components/Camera/CameraCard";
import { AlertsPanel } from "@/components/Alerts/AlertsPanel";
import { useState, useEffect } from "react";
import { Alerts, Cam, Records } from "@/types";

const Home = () => {
  const [cameras] = useState<Cam[]>([
    { id: "camera1", name: "Câmera1", location: "Patio1", status: "online" },
    { id: "camera2", name: "Câmera2", location: "Patio2", status: "online" },
    { id: "camera3", name: "Câmera3", location: "Patio3", status: "online" },
    { id: "camera4", name: "Câmera4", location: "Patio4", status: "online" },
  ]);

  const [alerts, setAlerts] = useState<Alerts[]>([]);
  const [records, setRecords] = useState<Records[]>([]);
  const [loading, setLoading] = useState(false);
  const [alertsOpen, setAlertsOpen] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [selectedCamera, setSelectedCamera] = useState("camera1");

  useEffect(() => {
    const fetchRecords = async () => {
      setLoading(true);
      try {
        const { data } = await apiClient.get(`/records/file/${selectedCamera}`);
        setRecords(data);
      } catch (err) {
        console.error("Erro ao carregar registros:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchRecords();
  }, [selectedCamera]);

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const { data } = await apiClient.get(`/alerts`);
        setAlerts(data);
      } catch (err) {
        console.error("Erro ao carregar alertas:", err);
      }
    };

    fetchAlerts();
  }, []);

  return (
    <div className="h-screen bg-gray-50 flex overflow-hidden">
      <Sidebar open={sidebarOpen} records={records} selectedCamera={selectedCamera} loading={loading} />

      <div className="flex-1 flex flex-col">
        <Header sidebarOpen={sidebarOpen} setSidebarOpen={setSidebarOpen} setAlertsOpen={setAlertsOpen} alertsCount={alerts.length} />

        <div className="p-6 overflow-y-scroll h-full">
          <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4 gap-6">
            {cameras.map((camera) => (
              <CameraCard key={camera.id} camera={camera} selected={selectedCamera === camera.id} onSelect={setSelectedCamera} />
            ))}
          </div>
        </div>
      </div>

      <AlertsPanel open={alertsOpen} alerts={alerts} cameras={cameras} onClose={() => setAlertsOpen(false)} />
    </div>
  );
};

export default Home;
