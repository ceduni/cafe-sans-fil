import { Orders, OrdersModel } from "../src/models/OrdersModel";
import { Stock, IStock } from "../src/models/StockModel";

export class ProductService {
  public constructor() {}

  /**
   * Fetches all sales from the database.
   * @param productName Optional product name to filter sales by.
   * @returns A promise that resolves to an array of sales.
   */
  public async getSales(
    collection: string,
    productName?: string
  ): Promise<OrdersModel[]> {
    try {
      const query = productName ? { "items.item_slug": productName } : {};
      const salesData = await Orders.find(query).exec();
      return salesData;
    } catch (err) {
      console.error("Error fetching sales data:", err);
      return [];
    }
  }

  /**
   * Fetches stock data from the database.
   * @returns A promise that resolves to an array of stock items.
   */
  public async getStock(): Promise<IStock[]> {
    console.log("Database connected for stock data");
    try {
      const stockData = await Stock.find({}).exec();
      return stockData;
    } catch (err) {
      console.error("Error fetching stock data:", err);
      return [];
    }
  }
}

export default ProductService;
