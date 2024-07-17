import request from "supertest";
import { MainController } from "../contollers/mainController";
import ShiftService from "../services/shiftServices";

let server: MainController;
let shiftService: ShiftService;

beforeAll(() => {
  server = new MainController();
  shiftService = new ShiftService();
});

afterAll(async () => {
  await server.closeDatabaseConnection();
});

describe("GET /api/v1/shifts", () => {
  it("should return a list of all shifts", async () => {
    const response = await request(server.App).get("/api/v1/shifts");
    expect(response.status).toBe(200);
    expect(response.body).toHaveProperty("Shifts");
    expect(response.body.Shifts).toBeInstanceOf(Array);
  });
});
