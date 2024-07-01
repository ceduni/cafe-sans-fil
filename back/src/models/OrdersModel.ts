import mongoose, { Document, Schema, Model } from 'mongoose';
import { v4 as uuidv4 } from 'uuid';

interface IOrderedItem {
    item_price: number;
    item_slug: string;
    options: { fee: number; type: string; value: string }[];
    quantity: number;
}

interface IOrder extends Document {
    order_id: string;
    order_number: number;
    cafe_slug: string;
    created_at: Date;
    items: IOrderedItem[];
    status: string;
    total_price: number;
    updated_at: Date;
    user_username: string;
}

const OrderedItemSchema: Schema = new Schema({
    item_price: { type: Number, required: true },
    item_slug: { type: String, required: true },
    options: [{ fee: { type: Number, required: true }, type: { type: String, required: true }, value: { type: String, required: true } }],
    quantity: { type: Number, required: true }
}, { _id: false });

const OrderSchema: Schema = new Schema({
    order_id: { type: String, required: true, default: uuidv4 },
    order_number: { type: Number, required: true },
    cafe_slug: { type: String, required: true },
    created_at: { type: Date, required: true },
    items: [OrderedItemSchema],
    status: { type: String, required: true },
    total_price: { type: Number, required: true },
    updated_at: { type: Date, required: true },
    user_username: { type: String, required: true }
});

const Orders: Model<IOrder> = mongoose.model<IOrder>('Orders', OrderSchema);

export class OrdersModel {
    public order_id: string;
    public order_number: number;
    public cafe_slug: string;
    public created_at: Date;
    public items: IOrderedItem[];
    public status: string;
    public total_price: number;
    public updated_at: Date;
    public user_username: string;

    constructor(
        order_id: string,
        order_number: number,
        cafe_slug: string,
        created_at: Date,
        items: IOrderedItem[],
        status: string,
        total_price: number,
        updated_at: Date,
        user_username: string
    ) {
        this.order_id = order_id || uuidv4();
        this.order_number = order_number;
        this.cafe_slug = cafe_slug;
        this.created_at = created_at || new Date();
        this.items = items;
        this.status = status;
        this.total_price = total_price;
        this.updated_at = updated_at || new Date();
        this.user_username = user_username;
    }

    public static fromDocument(doc: IOrder): OrdersModel {
        const items = doc.items.map(item => ({
            item_price: item.item_price,
            item_slug: item.item_slug,
            options: item.options,
            quantity: item.quantity
        }));

        return new OrdersModel(
            doc.order_id,
            doc.order_number,
            doc.cafe_slug,
            doc.created_at,
            items,
            doc.status,
            doc.total_price,
            doc.updated_at,
            doc.user_username
        );
    }

    public static async createOrder(data: Omit<IOrder, '_id'>): Promise<OrdersModel> {
        const order = new Orders(data);
        const savedOrder = await order.save();
        return OrdersModel.fromDocument(savedOrder);
    }

    public static async getOrderById(order_id: string): Promise<OrdersModel | null> {
        const doc = await Orders.findOne({ order_id });
        return doc ? OrdersModel.fromDocument(doc) : null;
    }

    public static async getOrders(): Promise<OrdersModel[]> {
        const docs = await Orders.find();
        return docs.map(doc => OrdersModel.fromDocument(doc));
    }

    public static async updateOrderStatus(order_id: string, status: string): Promise<OrdersModel | null> {
        const doc = await Orders.findOneAndUpdate({ order_id }, { status, updated_at: new Date() }, { new: true });
        return doc ? OrdersModel.fromDocument(doc) : null;
    }

    public static async deleteOrder(order_id: string): Promise<OrdersModel | null> {
        const doc = await Orders.findOneAndDelete({ order_id });
        return doc ? OrdersModel.fromDocument(doc) : null;
    }
}

export { Orders, IOrder }; // Ensure correct export
export default OrdersModel;
