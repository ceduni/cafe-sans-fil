import type { CafeBase } from './Cafe';

export interface CafeNode extends CafeBase {
    id: string;
    x?: number;
    y?: number;
    vx?: number;
    vy?: number;
    fx?: number | null;
    fy?: number | null;
    radius: number;
    color: string;
    activityLevel: number;
    logo?: string;
    coordinates?: {
        lat: number;
        lng: number;
    };
}

export interface EventNode {
    id: string;
    cafeId: string;
    title: string;
    time: string;
    timestamp: Date;
    attendance: number;
    color: string;
    angle: number;
}