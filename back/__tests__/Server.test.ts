import {Server} from '../src/Server';
import request from 'supertest';

describe('Get /', () => {
    let server: Server;

    beforeAll(() => {

        server = new Server();
        server.getIndex('/');

    });


    it('should respond with a 200 status ', async () => {
        const response = await request(server.App).get('/');
        expect(response.status).toBe(200);
      });
});
