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
 const Sale = mongoose.model('Sale',salesSchema);
 module.exports = Sale;