// --- TICKETING ---

export interface Ticketing {
  ticket_url: string;   // corresponds to HttpUrl
  ticket_price: number; // float
}

// --- EVENT BASE ---

export interface EventBase {
  name: string;
  description?: string | null;
  image_url?: string | null;
  start_date: string; // ISO datetime (use Date on client when parsed)
  end_date: string;   // ISO datetime
  location?: string | null;
  ticket?: Ticketing | null;
  max_support?: number; // default = 3
}

// --- EVENT DOCUMENT MODEL ---

export interface Event extends EventBase {
  _id?: string;          // MongoDB ObjectId
  cafe_ids: string[];    // related cafes
  creator_id: string;    // event creator
  editor_ids: string[];  // event editors
}
