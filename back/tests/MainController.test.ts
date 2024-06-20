import {MainController} from '../contollers/mainController';
import request from 'supertest';

describe('Get /', () => {
    let server: MainController;

    beforeAll(() => {

        server = new MainController();
        server.getIndex('/');

    });


    it('should respond with a 200 status ', async () => {
        const response = await request(server.App).get('/');
        expect(response.status).toBe(200);
    });

});

describe('GET /api/v1/cafe/sales/:id', () => {
    let server: MainController;
  
    beforeAll(() => {
      server = new MainController();
    });
  
    it('should display the number of sales for a product', async () => {
      const response = await request(server.App).get('/api/v1/cafe/sales/1');
      expect(response.status).toBe(201);
      expect(response.body.NumSales).toBe(-1);
    });
  
    it('should return -1 for a non-existing product', async () => {
      const response = await request(server.App).get('/api/v1/cafe/sales/999');
      expect(response.status).toBe(201);
      expect(response.body.NumSales).toBe(-1);
    });
  });