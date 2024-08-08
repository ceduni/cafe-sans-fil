import { IShift, ShiftModel } from "../models/DatabaseModels/shiftModel";

export class ShiftService {
  public constructor() {}
  public async getShifts(): Promise<IShift[]> {
    try {
      const result = await ShiftModel.find().exec();
      return result;
    } catch (err) {
      console.error("Error fetching shift data:", err);
      return [];
    }
  }

  public async getShiftsByMatricule(matricule: string): Promise<IShift | null> {
    try {
      const result = await ShiftModel.findOne({ matricule: matricule }).exec();
      return result;
    } catch (err) {
      console.error("Error fetching shift data:", err);
      return null;
    }
  }
}

export default ShiftService;
