"use client";
import { Records } from "@/types";
import { Clock } from "lucide-react";

type RecordListProps = {
    loading: boolean;
    records: Records[];
    selectedCamera: string;
};

export const RecordList = ({ records, selectedCamera, loading }: RecordListProps) => {
    return (
        <div className="p-4 space-y-3 h-full overflow-y-auto">
            {loading ? (
                <div className="flex items-center justify-center py-8">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                </div>
            ) : (
                records
                    .filter((r) => r.camera_id === selectedCamera)
                    .map((record) => (
                        <div key={record.timestamp} className="bg-gray-50 p-3 rounded-lg border">
                            <div className="text-xs text-gray-500 mt-1 flex items-center gap-1">
                                <Clock className="w-3 h-3" />
                                {`${record.timestamp} - ${record.camera_id} - ${record.placa}`}
                            </div>
                        </div>
                    ))
            )}
        </div>
    );
};
