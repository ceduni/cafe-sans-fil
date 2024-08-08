import request from "supertest";
import { MainController } from "../../src/contollers/mainController";
import CafeService from "../../src/services/cafeServices";

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

describe("POST /api/v1/cafes/:cafeName/volunteer", () => {
  it("should add a volunteer to the list of a specific cafe ", async () => {
    const response = await request(server.App)
      .post(`/api/v1/cafes/Acquis de droit/volunteer`)
      .send({
        userName: "20151109",
        Role: "Bénévole",
      });
    expect(response.body.message).toBe("User already exists");
  });
});

describe("DELETE /api/v1/cafes/:cafeName/:matricule", () => {
  it("should delete a specific volunteer from a specific list of volunteer in a cafe ", async () => {
    const response = await request(server.App).delete(
      `/api/v1/cafes/Acquis de droit/20201552`
    );
    expect(response.body.message).toBe("User not found");
  });
});
