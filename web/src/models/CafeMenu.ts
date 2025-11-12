// --- ENUMS (extend as needed) ---
export type Layout = "LIST" | "GRID" | "CARDS"; // adapt to your backend definitions

// --- MENU STRUCTURE ---

export interface Menu {
  layout: Layout;
  categories: MenuCategory[];
}

// --- MENU CATEGORY ---

export interface MenuCategoryBase {
  name: string;
  description?: string | null;
}

export interface MenuCategory extends MenuCategoryBase {
  items?: MenuItem[]; // not explicitly defined backend-side, but useful for frontend structure
}

// --- MENU ITEM OPTION ---

export interface MenuItemOption {
  type: string;
  value: string;
  fee: number; // corresponds to DecimalAnnotation in Python
}

// --- NUTRITION INFO ---

export interface NutritionInfo {
  calories?: number | null;
  lipids?: number | null;
  proteins?: number | null;
  carbohydrates?: number | null;
  sugar?: number | null;
  sodium?: number | null;
  fiber?: number | null;
  saturated_fat?: number | null;
  zinc?: number | null;
  iron?: number | null;
  calcium?: number | null;
  magnesium?: number | null;
  potassium?: number | null;
  vitamina?: number | null;
  vitaminc?: number | null;
  vitamind?: number | null;
  vitamine?: number | null;
  vitamink?: number | null;
  vitaminb6?: number | null;
  vitaminb12?: number | null;
}

// --- MENU ITEM BASE ---

export interface MenuItemBase {
  name: string;
  description?: string | null;
  tags?: string[] | null;
  image_url?: string | null;
  price: number;
  in_stock: boolean;
  likes: string[]; // user IDs
  barecode?: string | null;
  nutritional_informations: NutritionInfo;
  health_score: number;
  options: MenuItemOption[];
}

// --- MENU ITEM DOCUMENT (full model) ---

export interface MenuItem extends MenuItemBase {
  _id?: string;          // corresponds to MongoDB ObjectId
  cafe_id?: string;      // reference to Cafe
  category_ids?: string[]; // references to MenuCategory
}