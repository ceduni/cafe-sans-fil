import request from "supertest";
import { MainController } from "../../contollers/mainController";
import CafeService from "../../services/cafeServices";

let server: MainController;
let cafeService: CafeService;

beforeAll(() => {
  server = new MainController();
  cafeService = new CafeService();
});

afterAll(async () => {
  await server.closeDatabaseConnection();
});

describe("GET /api/v1/cafes", () => {
  it("should return a list of all Cafes", async () => {
    const response = await request(server.App).get("/api/v1/cafes");
    expect(response.status).toBe(200);
    expect(response.body).toHaveProperty("cafes");
    expect(response.body.cafes).toBeInstanceOf(Array);
  });
});

describe("GET /api/v1/cafes/:cafeName", () => {
  it("should return a cafe by name", async () => {
    const cafeName = "CaféKine";
    const cafe = await cafeService.getCafeByName(cafeName);
    if (cafe) {
      const response = await request(server.App).get(
        `/api/v1/cafes/${cafeName}`
      );
      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty("cafe");
      expect(response.body.cafe.name).toEqual(cafeName);
    } else {
      expect(true).toBe(false); // Cafe not found, test should fail
    }
  });
});

describe("GET /api/v1/cafes/:cafeName/volunteer", () => {
  it("should return a list of volunteers by cafe name", async () => {
    const cafeName = "CaféKine";
    const volunteer = await cafeService.getCafesVonlunteer(cafeName);
    if (volunteer) {
      const response = await request(server.App).get(
        `/api/v1/cafes/${cafeName}/volunteer`
      );
      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty("volunteers");
      expect(response.body.volunteers).toBeInstanceOf(Array);
    } else {
      expect(true).toBe(false); // Cafe not found, test should fail
    }
  });
});


describe("POST /api/v1/cafes/:cafeName/", () => {
  it("should return a list of volunteers by cafe name", async () => {
    const response = await request(server.App).post(
      `/api/v1/cafes/Café-In/`
    ).send({
      userName: "20026633",
      Role: "Bénévole"
    }); 
    expect(response.body.message).toBe("User already exists");
    
  });
});

