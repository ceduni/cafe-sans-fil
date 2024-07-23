import { Orders} from "../src/models/OrdersModel";
import { Stock, IStock } from "../src/models/StockModel";

export class ProductService {
 
  public constructor() {}

  /**
   * Fetches all sales from the database.
   * @param productName Optional product name to filter sales by.
   * @returns A promise that resolves to an array of sales.
   */
  public async getSales(productName?: string): Promise<any[]> {
    console.log(" in the productServices class");
    try {
      const query = productName ? { "items.item_name": productName } : {};
      console.log("query", query);
      const salesData = await Orders.find(query).exec();
      return salesData;
    } 
    catch (err) {
      console.error("Error fetching sales data:", err);
      return [];
    }
  }

  /**
   * Fetches stock data from the database.
   * @returns A promise that resolves to an array of stock items.
   */
  public async getStock(): Promise<IStock[]> {
    try {
      const stockData = await Stock.find({}).exec();
      return stockData;
    } catch (err) {
      console.error("Error fetching stock data:", err);
      return [];
    }
  }

  public async addOrder(order: any):Promise<{message:string}> {
    try {
      const newOrder = new  Orders(order);
      await newOrder.save();
      return { message: "Order added successfully" };
    } catch (err) {
      console.error("Error adding order:", err);
      return { message: "Error adding order" };
    }
    
  }
}

export default ProductService;
