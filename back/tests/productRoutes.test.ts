import request from 'supertest';
import {MainController} from '../contollers/mainController';
import Database from '../services/DataBase';

describe('GET /api/v1/sales', () => {
    let server: MainController;
  
    beforeAll(() => {
      server = new MainController();
    });

    afterAll(async () => {
      const database = await Database.getInstance('sales');
      await database.close();
  });
  
    it('should display the number of sales for a product', async () => {
      const response = await request(server.App).get('/api/v1/orders');
      expect(response.status).toBe(200);
      expect(response.body.Sales.length).toBe(200);
    });
  
});

describe('GET /api/v1sales/productName', () => {
    let server: MainController;
  
    beforeAll(() => {
      server = new MainController();
    });
  
    it('should display the number of sales for a product', async () => {
      const response = await request(server.App).get('/api/v1/orders/saepe');
      expect(response.status).toBe(200);
      console.log(response.body.Sales);
      expect(response.body.Sales.length).toBeGreaterThan(0)
      
    });
  
});




