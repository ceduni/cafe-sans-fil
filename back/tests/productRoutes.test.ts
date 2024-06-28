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
      const response = await request(server.App).get('/api/v1/sales');
      expect(response.status).toBe(200);
      expect(response.body.Sales.length).toBe(5000);
    });
  
});

describe('GET /api/v1sales/productName', () => {
    let server: MainController;
  
    beforeAll(() => {
      server = new MainController();
    });
  
    it('should display the number of sales for a product', async () => {
      const response = await request(server.App).get('/api/v1/sales/Licensed Soft Car');
      expect(response.status).toBe(200);
      expect(response.body.Sales.length).toBeGreaterThan(0)
      
    });
  
});


describe('GET /api/v1/cafe/sales/category/categoryName', () => {
  let server: MainController;

  beforeAll(() => {
    server = new MainController();
  });

  it('should return all the sales of a specific category', async () => {
    const response = await request(server.App).get('/api/v1/sales?category=Games');
    expect(response.status).toBe(200);
    expect(response.body.Sales).toBeDefined();
    
  });

});

