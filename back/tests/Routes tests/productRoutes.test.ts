import request from "supertest";
import { MainController } from "../../src/contollers/mainController";

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
    // expect(response.body.Sales.length).toBe(200);
  });
});

describe("GET /api/v1/orders/productName", () => {
  it("should display the number of sales for a product", async () => {
    const response = await request(server.App).get(
      "/api/v1/orders/Barre Kirkland"
    );
    expect(response.status).toBe(200);
    expect(response.body.Sales.length).toBeGreaterThanOrEqual(0);
  });
});

describe("GET /api/v1/stock", () => {
  it("should have a 200 status code for the end point ", async () => {
    const response = await request(server.App).get("/api/v1/stocks");
    expect(response.status).toBe(200); // Check if the status code is 200
    expect(response.body).toHaveProperty("Stock"); // Check if the Stock property exists
    expect(response.body.Stock.length).toBeGreaterThan(0); // Check if the Stock array is not empty
  });
});

describe("GET /api/v1/orders", () => {
  it("should  add a product to the collections of products ", async () => {
    const response = await request(server.App)
      .post("/api/v1/orders")
      .send({
        order_id: "7167979b-7889-494a-a810-9017755771eb",
        order_number: 4,
        cafe_name: "Pill Pub",
        cafe_slug: "pill-pub",
        cafe_image_url:
          "https://imagedelivery.net/70kpvhLybTnH06xFu8o2DQ/db42a0f6-6e3c-4507-eb1",
        user_username: "7802085",
        items: [
          {
            item_name: "Barre de chocolat",
            item_slug: "barre-de-chocolat",
            item_image_url:
              "https://tsel1.mm.bing.net/th?id=OIP.9LxtNeX56JCCLca0HKfBAgHaHa&pid=Api",
            quantity: 1,
            item_price: 1.5,
            options: [],
          },
          {
            item_name: "Brookside",
            item_slug: "brookside",
            item_image_url:
              "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2F.bp.blogs.com",
            quantity: 3,
            item_price: 0.5,
            options: [],
          },
        ],
        total_price: 3.0,
        status: "Complétée",
        created_at: "2024-01-05T20:30:38.093Z",
        updated_at: "2024-02-02T01:30:38.253Z",
      });
    expect(response.status).toBe(200);
    expect(response.body.message).toBe("Order added successfully");
  });
});
