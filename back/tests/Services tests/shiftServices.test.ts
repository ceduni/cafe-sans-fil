import { MainController } from "../../src/contollers/mainController";
import ShiftService from "../../src/services/shiftServices";
import { IShift } from "../../src/models/DatabaseModels/shiftModel";

let server: MainController;
let shiftService: ShiftService;

beforeAll(() => {
  server = new MainController();
  shiftService = new ShiftService();
});

afterAll(async () => {
  await server.closeDatabaseConnection();
});

describe("ShiftService Tests", () => {
  it("getShifts should return an array of shifts", async () => {
    const shifts: IShift[] = await shiftService.getShifts();
    expect(shifts).toBeInstanceOf(Array);
  });

  it("getShiftsByMatricule should return a shift by matricule", async () => {
    const matricule = "20281527"; // existing shift
    const shift: IShift | null = await shiftService.getShiftsByMatricule(
      matricule
    );
    if (shift) {
      expect(shift.matricule).toBe(matricule);
    } else {
      expect(true).toBe(false); // Shift not found, test should fail
    }
  });
});
