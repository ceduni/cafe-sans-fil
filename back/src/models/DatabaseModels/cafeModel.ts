import mongoose, { Schema, Document } from "mongoose";

// Interfaces pour les sous-schémas
interface ITimeBlock {
  start: string;
  end: string;
}

interface IOpeningHour {
  day: string;
  blocks: ITimeBlock[];
}

interface ILocation {
  pavillon: string;
  local: string;
}

interface IContact {
  email: string;
  phone_number: string;
  website: string;
}

interface ISocialMedia {
  platform_name: string;
  link: string;
}

interface IPaymentMethod {
  method: string;
  minimum: mongoose.Types.Decimal128;
}

interface IAdditionalInfo {
  type: string;
  value: string;
  start: Date;
  end: Date | null;
}

interface IStaffMember {
  username: string;
  role: string;
}

interface IMenuItemOption {
  type: string;
  value: string;
  fee: mongoose.Types.Decimal128;
}

interface IMenuItem {
  item_id: Buffer;
  name: string;
  slug: string;
  tags: string[];
  description: string;
  image_url: string;
  price: mongoose.Types.Decimal128;
  in_stock: boolean;
  category: string;
  options: IMenuItemOption[];
}

// Interface principale pour le document Café
interface ICafe extends Document {
  cafe_id: Buffer;
  name: string;
  slug: string;
  previous_slugs: string[];
  description: string;
  image_url: string;
  faculty: string;
  is_open: boolean;
  status_message: string | null;
  opening_hours: IOpeningHour[];
  location: ILocation;
  contact: IContact;
  social_media: ISocialMedia[];
  payment_methods: IPaymentMethod[];
  additional_info: IAdditionalInfo[];
  staff: IStaffMember[];
  menu_items: IMenuItem[];
}

// Schémas pour les sous-documents
const TimeBlockSchema: Schema = new Schema({
  start: { type: String, required: true },
  end: { type: String, required: true },
});

const OpeningHourSchema: Schema = new Schema({
  day: { type: String, required: true },
  blocks: { type: [TimeBlockSchema], required: true },
});

const LocationSchema: Schema = new Schema({
  pavillon: { type: String, required: true },
  local: { type: String, required: true },
});

const ContactSchema: Schema = new Schema({
  email: { type: String, required: true },
  phone_number: { type: String, required: false },
  website: { type: String, required: false },
});

const SocialMediaSchema: Schema = new Schema({
  platform_name: { type: String, required: true },
  link: { type: String, required: true },
});

const PaymentMethodSchema: Schema = new Schema({
  method: { type: String, required: true },
  minimum: { type: mongoose.Types.Decimal128, required: true },
});

const AdditionalInfoSchema: Schema = new Schema({
  type: { type: String, required: true },
  value: { type: String, required: true },
  start: { type: Date, required: true },
  end: { type: Date, required: false },
});

const StaffMemberSchema: Schema = new Schema({
  username: { type: String, required: true },
  role: { type: String, required: true },
});

const MenuItemOptionSchema: Schema = new Schema({
  type: { type: String, required: true },
  value: { type: String, required: true },
  fee: { type: mongoose.Types.Decimal128, required: true },
});

const MenuItemSchema: Schema = new Schema({
  item_id: { type: Buffer, required: true },
  name: { type: String, required: true },
  slug: { type: String, required: true },
  tags: { type: [String], required: true },
  description: { type: String, required: true },
  image_url: { type: String, required: true },
  price: { type: mongoose.Types.Decimal128, required: true },
  in_stock: { type: Boolean, required: true },
  category: { type: String, required: true },
  options: { type: [MenuItemOptionSchema], required: true },
});

// Schéma principal pour le Café
const CafeSchema: Schema = new Schema({
  cafe_id: { type: Buffer, required: true, unique: true },
  name: { type: String, required: true },
  slug: { type: String, required: true, unique: true },
  previous_slugs: { type: [String], required: true },
  description: { type: String, required: true },
  image_url: { type: String, required: true },
  faculty: { type: String, required: true },
  is_open: { type: Boolean, required: true },
  status_message: { type: String, required: false },
  opening_hours: { type: [OpeningHourSchema], required: true },
  location: { type: LocationSchema, required: true },
  contact: { type: ContactSchema, required: true },
  social_media: { type: [SocialMediaSchema], required: true },
  payment_methods: { type: [PaymentMethodSchema], required: true },
  additional_info: { type: [AdditionalInfoSchema], required: true },
  staff: { type: [StaffMemberSchema], required: true },
  menu_items: { type: [MenuItemSchema], required: true },
});

// Création du modèle
const CafeModel = mongoose.model<ICafe>("Cafe", CafeSchema, "cafes"); // for selecting the collection

export { CafeModel, ICafe };
