import Database from "./DataBase";
import { Orders, OrdersModel } from "../src/models/OrdersModel";
import { Stock, IStock } from "../src/models/StockModel";

export class ProductService {
  private database: Database | undefined;

  public static readonly DB_NAME = "sales";

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
    this.database = await Database.getInstance(ProductService.DB_NAME);
    try {
      const query = productName ? { "items.item_slug": productName } : {};
      const salesData = await Orders.find(query).exec();
      return salesData;
    } catch (err) {
      console.error("Error fetching sales data:", err);
      return [];
    } finally {
      this.database.close();
    }
  }

  /**
   * Fetches stock data from the database.
   * @returns A promise that resolves to an array of stock items.
   */
  public async getStock(): Promise<IStock[]> {
    this.database = await Database.getInstance(ProductService.DB_NAME);
    console.log("Database connected for stock data");
    try {
      const stockData = await Stock.find({}).exec();
      return stockData;
    } catch (err) {
      console.error("Error fetching stock data:", err);
      return [];
    } finally {
      this.database.close();
    }
  }
}

export default ProductService;
