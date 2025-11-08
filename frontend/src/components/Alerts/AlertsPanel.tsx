"use client";
import { apiClient } from "@/api/apiClient";
import { Alerts, Severity, Cam } from "@/types";
import { AlertTriangle, CircleX, Clock, SaveIcon } from "lucide-react";

type AlertsPanelProps = {
    open: boolean;
    cameras: Cam[];
    alerts: Alerts[];
    onClose: () => void;
};

const savePlate = async (alert: Alerts) => {
    try {
        const response = await apiClient.post("/moto", {
            camera: alert.camera_id,
            placa: alert.placa,
        });

        console.log(response.data.message);
    } catch (error) {
        console.error("Erro ao cadastrar moto:", error);
    } finally {
        location.reload();
    }
}

const deleteAlert = async (alert: Alerts) => {
    try {
        const response = await apiClient.delete(`/alert/${alert.placa}`);

        console.log(response.data.message);
    } catch (error) {
        console.error("Erro ao deletar alerta:", error);
    } finally {
        location.reload();
    }
}

const getSeverityColor = (severity: Severity) => {
    switch (severity) {
        case "high": return "text-red-600 bg-red-50";
        case "medium": return "text-yellow-600 bg-yellow-50";
        case "low": return "text-blue-600 bg-blue-50";
        default: return "text-gray-600 bg-gray-50";
    }
};

export const AlertsPanel = ({ open, alerts, cameras, onClose }: AlertsPanelProps) => {
    if (!open) return null;
    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex justify-end">
            <div className="bg-white w-96 h-full shadow-xl overflow-y-auto">
                <div className="p-6 border-b border-gray-200 flex items-center justify-between">
                    <h2 className="text-lg font-semibold text-gray-800 flex items-center gap-2">
                        <AlertTriangle className="w-5 h-5 text-red-600" />
                        Alertas Ativos
                    </h2>
                    <button onClick={onClose} className="p-2 hover:bg-gray-100 rounded-lg">
                        <CircleX className="w-5 h-5 text-gray-800" />
                    </button>
                </div>

                <div className="p-4 space-y-4">
                    {alerts.map((alert, idx) => (
                        <div key={idx} className={`p-4 rounded-lg border ${getSeverityColor(alert.severity)}`}>
                            <div className="flex items-start justify-between">
                                <div className="flex-1">
                                    <p className="text-xs mt-2 flex items-center gap-1">
                                        <Clock className="w-3 h-3" />
                                        {alert.timestamp}
                                    </p>
                                    <p className="font-medium">
                                        Alerta: <span className="font-semibold">{alert.alert}</span>
                                    </p>
                                    <p>
                                        Placa: <span className="font-semibold">{alert.placa}</span>
                                    </p>
                                    <p className="text-sm mt-1">
                                        Câmera: <span className="font-semibold">{alert.camera_id}</span>
                                    </p>
                                    <div className="flex gap-4">
                                        <button
                                            onClick={() => { savePlate(alert); onClose(); }}
                                            className="bg-blue-400 text-amber-50 mb-2 mt-4 p-4 hover:bg-blue-200 hover:text-black rounded-lg flex gap-2"
                                        >
                                            Salvar Placa
                                        </button>

                                        <button
                                            onClick={() => { deleteAlert(alert); onClose(); }}
                                            className="bg-red-500 text-amber-50 mb-2 mt-4 p-4 hover:bg-red-400 rounded-lg flex gap-2"
                                        >
                                            Excluir Alerta
                                        </button>
                                    </div>
                                </div>
                                <AlertTriangle className="w-5 h-5 flex-shrink-0" />
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};
