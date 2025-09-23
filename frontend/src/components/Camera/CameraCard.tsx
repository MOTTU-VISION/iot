"use client";
import { Cam } from "@/types";
import { apiClient } from "@/api/apiClient";
import { Camera, Video } from "lucide-react";

type CameraCardProps = {
    camera: Cam;
    selected: boolean;
    onSelect: (id: string) => void;
};

export const CameraCard = ({ camera, selected, onSelect }: CameraCardProps) => {
    return (
        <div
            onClick={() => onSelect(camera.id)}
            className={`${selected ? "ring-2 ring-blue-500" : "hover:shadow-lg"}
                bg-white 
                rounded-lg 
                shadow-md 
                duration-200
                cursor-pointer 
                transition-all
                overflow-hidden
            `}
        >
            <div className="relative aspect-video bg-gray-900 flex items-center justify-center">
                {camera.status === "online" ? (
                    <div className="w-full h-full bg-gradient-to-br from-gray-800 to-gray-900 flex items-center justify-center">
                        <img
                            src={`${apiClient.defaults.baseURL}/stream/${camera.id}`}
                            alt={`Stream da ${camera.name}`}
                            className="w-full h-full object-contain"
                            onError={(e) => {
                                const img = e.target as HTMLImageElement;
                                img.style.display = "none";
                                if (img.nextSibling && img.nextSibling instanceof HTMLElement) {
                                    (img.nextSibling as HTMLElement).style.display = "flex";
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
                <div className={`absolute top-2 right-2 w-3 h-3 rounded-full ${camera.status === "online" ? "bg-green-400" : "bg-red-400"}`}></div>
            </div>

            <div className="p-4">
                <h3 className="font-medium text-gray-900">{camera.name}</h3>
                <p className="text-sm text-gray-500 mt-1">{camera.location}</p>
                <div className="flex items-center justify-between mt-3">
                    <span
                        className={`text-xs px-2 py-1 rounded-full ${camera.status === "online" ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"
                            }`}
                    >
                        {camera.status === "online" ? "Online" : "Offline"}
                    </span>
                    <span className="text-xs text-gray-400">{camera.id}</span>
                </div>
            </div>
        </div>
    );
};
