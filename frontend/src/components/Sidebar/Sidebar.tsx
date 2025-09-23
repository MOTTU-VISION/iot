"use client";
import { FileText } from "lucide-react";
import { RecordList } from "../Records/RecordList";
import { Records } from "@/types";

type SidebarProps = {
    open: boolean;
    loading: boolean;
    records: Records[];
    selectedCamera: string;
};

export const Sidebar = ({ open, records, selectedCamera, loading }: SidebarProps) => {
    return (
        <div className={`bg-white shadow-lg transition-all duration-300 ${open ? "w-80" : "w-0"} overflow-hidden`}>
            <div className="p-6 border-b border-gray-200">
                <h2 className="text-lg font-semibold text-gray-800 flex items-center gap-2">
                    <FileText className="w-5 h-5" />
                    Registros
                </h2>
            </div>
            <RecordList records={records} selectedCamera={selectedCamera} loading={loading} />
        </div>
    );
};
