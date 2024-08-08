import request from "supertest";
import { MainController } from "../../src/contollers/mainController";
import ShiftService from "../../src/services/shiftServices";

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

describe("GET /api/v1/shifts/matricule/:matricule", () => {
  it("should return a shift by matricule", async () => {
    const matricule = "20281527"; // existing shift
    const shift = await shiftService.getShiftsByMatricule(matricule);
    if (shift) {
      const response = await request(server.App).get(
        `/api/v1/shifts/matricule/${matricule}`
      );
      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty("shifts");
      expect(response.body.shifts).toHaveProperty("shift");
      expect(response.body.shifts.shift).toBeInstanceOf(Array);
    } else {
      expect(true).toBe(false); // shift not found, test should fail
    }
  });
});

describe("GET /api/v1/shifts/matricule/:matricule", () => {
  it("should return a null because matricule not found", async () => {
    const matricule = "90000000"; // non existing shift
    const response = await request(server.App).get(
      `/api/v1/shifts/matricule/${matricule}`
    );
    expect(response.status).toBe(200);
    expect(response.body).toHaveProperty("shifts");
    expect(response.body.shifts).toEqual(null);
  });
});
