export interface Notification {
    id: string;
    message: string;
    type: "success" | "warning" | "error" | "info";
    timestamp: number;
    read: boolean;
    actionUrl?: string;
}