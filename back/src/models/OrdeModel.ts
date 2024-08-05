import mongoose, { Document, Schema, Model } from "mongoose";
import { v4 as uuidv4 } from "uuid";

// Interface for the ordered items
interface IOrderedItem {
  item_name: string;
  item_slug: string;
  item_image_url: string;
  quantity: number;
  item_price: number;
  options: { fee?: number; type?: string; value?: string }[];
}

// Interface for the order
interface IOrder extends Document {
  order_id: string;
  order_number: number;
  cafe_name: string;
  cafe_slug: string;
  cafe_image_url: string;
  user_username: string;
  items: IOrderedItem[];
  total_price: number;
  status: string;
  created_at: Date;
  updated_at: Date;
}

// Schema for the ordered items
const OrderedItemSchema: Schema = new Schema(
  {
    item_name: { type: String, required: true },
    item_slug: { type: String, required: true },
    item_image_url: { type: String, required: true },
    quantity: { type: Number, required: true },
    item_price: { type: Number, required: true },
    options: [
      {
        fee: { type: Number },
        type: { type: String },
        value: { type: String },
      },
    ],
  },
  { _id: false }
);

// Schema for the order
const OrdeSchema: Schema = new Schema({
  order_id: { type: String, required: true, default: uuidv4 },
  order_number: { type: Number, required: true },
  cafe_name: { type: String, required: true },
  cafe_slug: { type: String, required: true },
  cafe_image_url: { type: String, required: true },
  user_username: { type: String, required: true },
  items: { type: [OrderedItemSchema], required: true },
  total_price: { type: Number, required: true },
  status: { type: String, required: true },
  created_at: { type: Date, required: true },
  updated_at: { type: Date, required: true },
});

// Create the model for orders
const Ordes: Model<IOrder> = mongoose.model<IOrder>("cafe_orders", OrdeSchema);

export { Ordes, IOrder, IOrderedItem };
