import { MongoClient, Db, Collection, Document } from 'mongodb';

class Database {
    private static instance: Database;
    private client: MongoClient;
    private db: Db;
    private static readonly  URI = 'mongodb+srv://cafe:sans-fil@cluster0.ti5co91.mongodb.net/sales?retryWrites=true&w=majority';
    private static _connectionFlag:boolean=false;
    private constructor(dbName: string) {
        this.client = new MongoClient(Database.URI);
        this.db = this.client.db(dbName);
    }

    public static async getInstance(dbName: string): Promise<Database> {
        console.log("fect");
        if (!Database.instance) {
            console.log('Creating new Database instance...');
            Database.instance = new Database(dbName);
            await Database.instance.connect();
        }
        if(!Database._connectionFlag){
            console.log("not connected");
            await Database.instance.connect();
        }
        console.log('returning');
        return Database.instance;
    }

    public async connect() {
        
            try {
                console.log("asking for connection")
                await this.client.connect();       
                Database._connectionFlag = true;
                
                console.log('Connected to MongoDB');
            } catch (error) {
                console.error('Error connecting to MongoDB:', error);
            }

        
        
    }

    public getCollection<T extends Document>(name: string): Collection<T> {
        if (!Database._connectionFlag) {
            throw new Error('Client is not connected');
        }
        return this.db.collection<T>(name);
    }

    public async close() {
        if (Database._connectionFlag) {
            try {
                await this.client.close();
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
