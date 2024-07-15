import { trace } from "console";
import { IShift, ShiftModel } from "../src/models/DatabaseModels/shiftModel";
import Database from "./DataBase";

export class ShiftService {
  private database: Database | undefined;
  public static readonly DB_NAME = "sales";
  public constructor() {}
  public async getShifts(): Promise<IShift[]> {
    this.database = await Database.getInstance(ShiftService.DB_NAME);
    try {
      const result = await ShiftModel.find().exec();
      return result;
    } catch (err) {
      console.error("Error fetching shift data:", err);
      return [];
    } finally {
      this.database.close();
    }
  }

  public async getShiftsByMatricule(matricule: string): Promise<IShift | null> {
    this.database = await Database.getInstance(ShiftService.DB_NAME);
    try {
      const result = await ShiftModel.findOne({ matricule: matricule }).exec();
      return result;
    } catch (err) {
      console.error("Error fetching shift data:", err);
      return null;
    } finally {
      this.database.close();
    }
  }
}

export default ShiftService;
