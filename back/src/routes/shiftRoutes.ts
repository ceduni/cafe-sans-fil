import { Router, Request, Response } from "express";

import { IUser } from "../models/DatabaseModels/userModel";
import ShiftService from "../services/shiftServices";
import { IShift } from "../models/DatabaseModels/shiftModel";

export class ShiftRoutes {
  private _router: Router;
  private ShiftService: ShiftService;
  constructor() {
    this._router = Router();
    this.ShiftService = new ShiftService();
    this.init();
  }

  private init() {
    this._router.get("/shifts", this.getShift.bind(this));
    this._router.get(
      "/shifts/matricule/:matricule",
      this.getShiftByMatricule.bind(this)
    );
  }

  public get router(): Router {
    return this._router;
  }

  public async getShift(req: Request, res: Response): Promise<void> {
    try {
      const Shifts: IShift[] | null = await this.ShiftService.getShifts();
      res.status(200).send({
        message: "Success",
        Shifts: Shifts,
      });
    } catch (error) {
      console.log("Error in the getShift:", error);
      res.status(500).send({
        message: "Internal Server Error",
        error: error,
      });
    }
  }

  public async getShiftByMatricule(req: Request, res: Response): Promise<void> {
    try {
      const matricule = req.params.matricule;
      const shifts: IShift | null =
        await this.ShiftService.getShiftsByMatricule(matricule);
      res.status(200).send({
        message: "Success",
        shifts: shifts,
      });
    } catch (err) {
      console.log("Error in the getShiftByMatricule:", err);
      res.status(500).send({
        message: "Internal Server Error",
        error: err,
      });
    }
  }
}
