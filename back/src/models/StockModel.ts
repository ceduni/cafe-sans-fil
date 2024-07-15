import mongoose, { Document, Schema } from "mongoose";

interface IStock extends Document {
  item_name: string;
  category: string;
  quantity: number;
}

const StockSchema: Schema = new Schema({
  item_name: { type: String, required: true },
  category: { type: String, required: true },
  quantity: { type: Number, required: true },
});

const Stock = mongoose.model<IStock>("Stocks", StockSchema);

export { IStock, Stock };
export default Stock;
