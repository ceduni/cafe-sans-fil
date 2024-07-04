const mongoose = require('mongoose');
const { ObjectId } = require('mongodb');

const salesSchema = new mongoose.Schema({
    name: { 
          type: String, 
          required: true 
         },
    category: { type: String, 
                required: true 
              },
    quantity: { type: Number, 
                required: true 
              },
    date: { type: Date,
            required: true 
          }
});
const orderSchema = new mongoose.Schema({
  product: { 
           type: String, 
           required: true 
          },
  category: { 
            type: String, 
            required: true 
          },
  date: { 
        type: Date,
        required: true 
    },
  time:{ 
         type:Date,
         Default:Date.now,
         require : true
       }

});

const StockSchema = new mongoose.Schema({
  item_name: { type: String, required: true },
  category: { type: String, required: true },
  quantity: { type: Number, required: true }
});
 const Stock = mongoose.model('Stocks', StockSchema);
 const Sale = mongoose.model('Sale',salesSchema);
 const Order = mongoose.model('Order',orderSchema);
 module.exports = {Sale,Order,Stock};


