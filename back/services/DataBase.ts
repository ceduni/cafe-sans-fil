import { MongoClient, Db, Collection, Document } from 'mongodb';
import mongoose,{Connection} from 'mongoose';
class Database {
    private static instance: Database;
    private client: Connection;
    //private db: Db;
    private static readonly  URI = "mongodb+srv://cafe:sans-fil@cluster0.ti5co91.mongodb.net/sales?retryWrites=true&w=majority";
    private static _connectionFlag:boolean=false;
    private constructor(dbName: string) {
        this.client = mongoose.connection;
    }

    public static async getInstance(dbName: string): Promise<Database> {

        if (!Database.instance) {
            Database.instance = new Database(dbName);
            await Database.instance.connect();
        }
        if(!Database._connectionFlag){
            await Database.instance.connect();
        }
        return Database.instance;
    }

    public async connect() {
        
            try {
                await mongoose.connect(Database.URI);    
                Database._connectionFlag = true;
                
                console.log('Connected to MongoDB');
            } catch (error) {
                console.error('Error connecting to MongoDB:', error);
            }

        
        
    }

   

    public async close() {
        if (Database._connectionFlag) {
            try {
                await mongoose.disconnect();
                Database._connectionFlag = false;
                console.log('Disconnected from MongoDB');
            } catch (error) {
                console.error('Failed to disconnect from MongoDB:', error);
            }
        }
    }

  

    public get connectionFlag(): boolean {
        return Database._connectionFlag;
    }
}

export default Database;
