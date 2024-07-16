import request from "supertest";
import { MainController } from "../contollers/mainController";

let server: MainController;
beforeAll(() => {
  server = new MainController();
});

afterAll(async () => {
  await server.closeDatabaseConnection();
});

describe("GET /api/v1/orders", () => {
  it("should display the number of sales for a product", async () => {
    const response = await request(server.App).get("/api/v1/orders");
    expect(response.status).toBe(200);
    expect(response.body.Sales.length).toBe(200);
  });
});

describe("GET /api/v1/orders/productName", () => {
  it("should display the number of sales for a product", async () => {
    const response = await request(server.App).get("/api/v1/orders/saepe");
    expect(response.status).toBe(200);
    expect(response.body.Sales.length).toBeGreaterThanOrEqual(0);
  });
});

describe("GET /api/v1/stock", () => {
  it("should have a 200 status code for the end point ", async () => {
    const response = await request(server.App).get("/api/v1/stock");
    expect(response.status).toBe(200); // Check if the status code is 200
    expect(response.body).toHaveProperty("Stock"); // Check if the Stock property exists
    expect(response.body.Stock.length).toBeGreaterThan(0); // Check if the Stock array is not empty
  });
});
