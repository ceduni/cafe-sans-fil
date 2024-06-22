const { faker } = require('@faker-js/faker'); // Correct import
const mongoose = require('mongoose');
const Sale = require('./model'); // Ensure this path is correct and the model is named appropriately

async function seedData(){
    const uri = 'mongodb+srv://cafe:sans-fil@cluster0.ti5co91.mongodb.net/sales?retryWrites=true&w=majority';
    const seed_count = 5000;
    mongoose.set('strictQuery', false);
    mongoose.connect(uri, {
        useNewUrlParser: true,
        useUnifiedTopology: true
    }).then(() => {
        console.log('Connected to Mongo');
    }).catch((err) =>{
        console.error('error',err);
    });

    let fakeSales = [];
    for (let i = 0; i < seed_count; i++) {
        fakeSales.push({
            name: faker.commerce.productName(),
            category: faker.commerce.department(),
            quantity: faker.datatype.number({ min: 1, max: 100 }),
            date: faker.date.between('2023-01-01', '2023-12-31')
        });
    }

    const seedDB = async () => {
        await Sale.insertMany(fakeSales);
    }

    seedDB().then(() => {
        mongoose.connection.close();
    });
}

seedData();
