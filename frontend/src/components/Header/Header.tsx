"use client";
import { Camera, ChevronLeft, ChevronRight, Bell } from "lucide-react";

type HeaderProps = {
    alertsCount: number;
    sidebarOpen: boolean;
    setAlertsOpen: (v: boolean) => void;
    setSidebarOpen: (v: boolean) => void;
};

export const Header = ({ sidebarOpen, setSidebarOpen, setAlertsOpen, alertsCount }: HeaderProps) => {
    return (
        <div className="bg-white shadow-sm border-b border-gray-200 p-4 flex items-center justify-between">
            <div className="flex items-center gap-4">
                <button
                    onClick={() => setSidebarOpen(!sidebarOpen)}
                    className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                >
                    {sidebarOpen ? <ChevronLeft className="w-5 h-5 text-gray-800" /> : <ChevronRight className="w-5 h-5 text-gray-800" />}
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
                Alertas ({alertsCount})
            </button>
        </div>
    );
};
