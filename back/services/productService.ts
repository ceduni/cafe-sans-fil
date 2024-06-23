import Database from './DataBase';
import { Collection, Document } from 'mongodb';

export class ProductService {
    
    public static readonly DB_NAME = 'sales';

    public constructor() {}
    /**
     * 
     * @param product the product we want the sales 
     * @returns return all the sales if the product names isn't specified else the sales of a
     */
    public async getSales(productName?:string): Promise<Document[]> {
        const database: Database = await Database.getInstance(ProductService.DB_NAME);
        const salesCollection: Collection<Document> = database.getCollection<Document>('sales');
        
        try {
            const query = productName ? { name:productName } : {};
            console.log(query);
            const salesData = await salesCollection.find(query).toArray();

            return salesData; 
        } catch (err) {
            console.error('Error fetching sales data:', err);
            return [];
        } finally {
            await database.close();
        }
    }
}
