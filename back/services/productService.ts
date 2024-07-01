import Database from './DataBase';
import { Collection, Document } from 'mongodb';
import OrdersModel, {Orders} from '../src/models/OrdersModel'
import { promises } from 'dns';

export class ProductService {
    
    private  database: Database | undefined;
    private collection: Collection<Document>|undefined;
    
    public static readonly DB_NAME = 'sales';

    public constructor() {}

   

    /**
     * 
     * @param product the product we want from an order
     * @returns return all the sales if the product names isn't specified else the sales of a
     */
    public async getSales(collection:string,productName?:string): Promise<OrdersModel[]> {
         this.database = await Database.getInstance(ProductService.DB_NAME);
         this.collection = this.database.getCollection<Document>(collection);
        try {
            const query = productName ? {"items.item_slug":productName} : {};
            const salesData = await this.collection.find(query).toArray();
            const salesModel = salesData.map(doc => OrdersModel.fromDocument(doc as any));
            return salesModel ; 
        } catch (err) {
            console.error('Error fetching sales data:', err);
            return [];
        } 
        finally {
            await this.database.close();
        }
    }

   /**
     * Fetches all stock items from the database.
     * @returns A promise that resolves to an array of stock items.
     */
   public async getStock(collection:string): Promise<Document[]> {
        this.database = await Database.getInstance(ProductService.DB_NAME);
        try {
            
            console.log("this is next");
            this.collection= this.database.getCollection<Document>(collection);
            const stock: Document[] = await this.collection.find().toArray();
            console.log('Stock data:', stock);
           
            return stock;
        } catch (err) {
            console.error('Error fetching stock data:', err);
            await this.database.close();
            return [];
        } 
    }

   

}


