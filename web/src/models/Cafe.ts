export type Days =
  | "MONDAY"
  | "TUESDAY"
  | "WEDNESDAY"
  | "THURSDAY"
  | "FRIDAY"
  | "SATURDAY"
  | "SUNDAY";

export type PaymentMethod = "CASH" | "CARD" | "INTERAC" | "OTHER"; // example
export type Feature = string; // could be more specific if defined backend-side


// --- BASE MODELS ---

export interface Affiliation {
  university: string;
  faculty: string;
}

export interface TimeBlock {
  start: string; // format: "HH:mm"
  end: string;   // format: "HH:mm"
}

export interface DayHours {
  day: Days;
  blocks: TimeBlock[];
}

export interface Geometry {
  type: string;
  coordinates: number[]; // e.g., [longitude, latitude]
}

export interface Location {
  pavillon: string;
  local: string;
  floor?: string | null;
  geometry?: Geometry | null;
}

export interface Contact {
  email?: string | null;
  phone_number?: string | null;
  website?: string | null;
}

export interface SocialMedia {
  facebook?: string | null;
  instagram?: string | null;
  x?: string | null; // Twitter/X
}

export interface PaymentDetails {
  method: PaymentMethod;
  minimum?: number | null; // Decimal on backend
}


// --- BASE CAFE MODEL ---

export interface CafeBase {
  name: string;
  slug?: string | null;
  previous_slugs?: string[];
  features: Feature[];
  description: string;
  logo_url?: string | null;
  banner_url?: string | null;
  photo_urls?: string[];
  affiliation: Affiliation;
  is_open: boolean;
  status_message?: string | null;
  opening_hours: DayHours[];
  location: Location;
  health_score: number;
  contact: Contact;
  social_media: SocialMedia;
  payment_details: PaymentDetails[];
}

// --- CAFE DOCUMENT MODEL (extends CafeBase) ---

export interface Staff {
  admin_ids: string[];
  volunteer_ids: string[];
}

export type Layout = "LIST" | "GRID"; // example

export interface MenuCategory {
  name: string;
  items: MenuItem[];
}

export interface MenuItem {
  name: string;
  price: number;
  description?: string;
}

export interface Menu {
  categories: MenuCategory[];
  layout: Layout;
}

export interface Cafe extends CafeBase {
  owner_id: string; // corresponds to PydanticObjectId
  staff: Staff;
  menu: Menu;
}