import mongoose from 'mongoose';
import { Orders } from './OrdersModel';

const uri = 'mongodb+srv://cafe:sans-fil@cluster0.ti5co91.mongodb.net/sales?retryWrites=true&w=majority';

async function testQuery() {
    try {
        await mongoose.connect(uri);
        console.log('Connected to MongoDB');

        const query = { 'items.itemSlug': '' }; // Adjust the query as needed
        const salesData = await Orders.find(query).exec();
        console.log('Sales Data:', salesData); // This should print the sales data

        await mongoose.connection.close();
        console.log('Disconnected from MongoDB');
    } catch (error) {
        console.error('Error:', error);
    }
}

testQuery();
