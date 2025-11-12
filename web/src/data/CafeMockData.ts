import { FACULTY_COLORS } from '@utils/Colors';
import type { CafeNode } from '@models/Node';
import cafesData from './cafesansfil_cafes.json';

type Dimension = {
    width: number;
    height: number;
};

interface RawCafe {
    _id: { $oid: string };
    name: string;
    slug?: string | null;
    previous_slugs?: string[];
    features: string[];
    description: string;
    logo_url?: string | null;
    banner_url?: string | null;
    photo_urls?: string[];
    affiliation: {
        university: string;
        faculty: string;
    };
    is_open: boolean;
    status_message?: string | null;
    opening_hours: Array<{
        day: string;
        blocks: Array<{ start: string; end: string }>;
    }>;
    location: {
        pavillon: string;
        local: string;
        floor?: string | null;
        geometry?: {
            type: string;
            coordinates: [number, number];
        } | null;
    };
    health_score: number;
    contact: {
        email?: string | null;
        phone_number?: string | null;
        website?: string | null;
    };
    social_media: {
        instagram?: string | null;
        facebook?: string | null;
        x?: string | null;
    };
    payment_details: Array<{
        method: string;
        minimum?: { $numberDecimal: string } | null;
    }>;
}

export const generateMockData = (dimensions: Dimension): CafeNode[] => {
    const rawCafes = cafesData as RawCafe[];
    
    // Calculate activity level based on health score and features
    const calculateActivityLevel = (cafe: RawCafe): number => {
        const baseActivity = Math.random() * 50 + 20; // 20-70 base
        const healthBonus = (cafe.health_score / 100) * 20; // Up to 20 bonus
        const featureBonus = cafe.features.length * 2; // 2 per feature
        return Math.min(100, Math.round(baseActivity + healthBonus + featureBonus));
    };

    // Calculate radius based on various factors
    const calculateRadius = (cafe: RawCafe): number => {
        const baseRadius = 50;
        const featureBonus = cafe.features.length * 3;
        const healthBonus = (cafe.health_score / 100) * 15;
        return Math.round(baseRadius + featureBonus + healthBonus);
    };

    return rawCafes.map((cafe, index) => {
        const faculty = cafe.affiliation.faculty;
        const color = FACULTY_COLORS[faculty] || FACULTY_COLORS['default'] || '#667eea';
        
        // Extract coordinates from geometry if available
        let coordinates: { lat: number; lng: number } | undefined;
        if (cafe.location.geometry?.coordinates) {
            const [lng, lat] = cafe.location.geometry.coordinates;
            coordinates = { lat, lng };
        }

        // Generate initial positions in an elliptical pattern if no coordinates (horizontal spread)
        const angle = (index / rawCafes.length) * 2 * Math.PI;
        const radiusX = dimensions.width * 0.4; // Horizontal radius
        const radiusY = dimensions.height * 0.25; // Vertical radius (smaller for horizontal layout)
        const defaultX = dimensions.width / 2 + Math.cos(angle) * radiusX;
        const defaultY = dimensions.height / 2 + Math.sin(angle) * radiusY;

        // Parse payment details
        const parsedPaymentDetails = cafe.payment_details.map(pd => ({
            method: pd.method,
            minimum: pd.minimum?.$numberDecimal ? parseFloat(pd.minimum.$numberDecimal) : null
        }));

        return {
            id: cafe._id.$oid,
            name: cafe.name,
            slug: cafe.slug,
            previous_slugs: cafe.previous_slugs || [],
            features: cafe.features,
            description: cafe.description,
            logo_url: cafe.logo_url,
            banner_url: cafe.banner_url,
            photo_urls: cafe.photo_urls || [],
            affiliation: cafe.affiliation,
            is_open: cafe.is_open,
            status_message: cafe.status_message,
            opening_hours: cafe.opening_hours.map(oh => ({
                day: oh.day as any,
                blocks: oh.blocks
            })),
            location: {
                pavillon: cafe.location.pavillon,
                local: cafe.location.local,
                floor: cafe.location.floor || undefined,
                geometry: cafe.location.geometry || undefined
            },
            health_score: cafe.health_score,
            contact: cafe.contact,
            social_media: cafe.social_media,
            payment_details: parsedPaymentDetails,
            radius: calculateRadius(cafe),
            color: color,
            activityLevel: calculateActivityLevel(cafe),
            logo: cafe.logo_url || `https://api.dicebear.com/7.x/initials/svg?seed=${encodeURIComponent(cafe.name)}&backgroundColor=${color.replace('#', '')}`,
            coordinates: coordinates,
            x: defaultX,
            y: defaultY
        };
    });
};