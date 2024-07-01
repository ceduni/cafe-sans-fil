const { faker } = require('@faker-js/faker'); // Correct import
const mongoose = require('mongoose');
const {Sale,Order,Stock} = require('./model'); // Ensure this path is correct and the model is named appropriately

async function seedData(){
    const uri = 'mongodb+srv://cafe:sans-fil@cluster0.ti5co91.mongodb.net/sales?retryWrites=true&w=majority';
    const seed_count = 20;
    mongoose.set('strictQuery', false);
    mongoose.connect(uri, {
        useNewUrlParser: true,
        useUnifiedTopology: true
    }).then(() => {
        console.log('Connected to Mongo');
    }).catch((err) =>{
        console.error('error',err);
    });

    //const fakeSales = seedSalesData();
    //const fakeOrders = seedOrdersData(seed_count);
    //console.log(fakeOrders);
    const  stock = seedStock(seed_count);
    const seedDB = async () => {
        //await Sale.insertMany(fakeSales);
        await Stock.insertMany(stock);
    }

    seedDB().then(() => {
        mongoose.connection.close();
    });
}
function seedSalesData(count){
    
    const orders = [];
    for (let i = 0; i < seed_count; i++) {
        fakeSales.push({
            product: faker.commerce.productName(),
            category: faker.commerce.department(),
            quantity: faker.datatype.number({ min: 1, max: 100 }),
            date: faker.date.between('2023-01-01', '2023-12-31')
        });
    }
    return orders

}

function seedOrdersData(count){

    
    const orders = [];
    for (let i = 0; i < count; i++) {
        orders.push({
            product: faker.commerce.productName(),
            category: faker.commerce.department(),
            date: faker.date.past(1),
            time: faker.date.recent() // G
        });
    }
    console.log(orders);
    return orders;
    
}

function seedStock(count){
    const stockData = [];
    for (let i = 0; i < count; i++) {
        stockData.push(
            {
                stock_id: faker.datatype.uuid(),
                item_name: faker.commerce.productName(),
                category: faker.commerce.department(),
                quantity: faker.datatype.number({ min: 1, max: 100 })
            }
        )
    }
    return stockData;
}


seedData();
