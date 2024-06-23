import { MongoClient, Db, Collection, Document } from 'mongodb';

class Database {
    private static instance: Database;
    private client: MongoClient;
    private db: Db;
    private readonly uri = 'mongodb+srv://cafe:sans-fil@cluster0.ti5co91.mongodb.net/sales?retryWrites=true&w=majority';

    private constructor(dbName: string) {
        this.client = new MongoClient(this.uri);
        this.db = this.client.db(dbName);
    }

    public static async getInstance(dbName: string): Promise<Database> {
        if (!Database.instance) {
            Database.instance = new Database(dbName);
            await Database.instance.connect();
        } else {
            console.log("Reusing existing database instance");
        }
        return Database.instance;
    }

    private async connect() {
        try {
            console.log('Attempting to connect to MongoDB...');
            await this.client.connect();
            console.log('Connected to MongoDB');
        } catch (error) {
            console.error('Connection to MongoDB failed:', error);
            // Re-throw the error so that it can be caught and handled in getInstance
            throw error;
        }
    }

    public getCollection<T extends Document>(name: string): Collection<T> {
        return this.db.collection<T>(name);
    }

    public async close() {
        await this.client.close();
        console.log('Disconnected from MongoDB');
    }
}

export default Database;
