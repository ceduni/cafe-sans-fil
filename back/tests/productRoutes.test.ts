import request from 'supertest';
import {MainController} from '../contollers/mainController';

describe('GET /api/v1/cafe/sales', () => {
    let server: MainController;
  
    beforeAll(() => {
      server = new MainController();
    });
  
    it('should display the number of sales for a product', async () => {
      const response = await request(server.App).get('/api/v1/cafe/sales');
      expect(response.status).toBe(200);
      expect(response.body.Sales.length).toBe(5000);
    });
  
});

describe('GET /api/v1/cafe/sales/productName', () => {
    let server: MainController;
  
    beforeAll(() => {
      server = new MainController();
    });
  
    it('should display the number of sales for a product', async () => {
      const response = await request(server.App).get('/api/v1/cafe/sales/pain');
      expect(response.status).toBe(200);
      expect(response.body.Sales.length).toBeGreaterThan(0)
      
    });
  
});

