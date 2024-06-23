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

