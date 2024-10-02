import { Router, Request, Response } from "express";
import { CafeService } from "../services/cafeServices";
import { ICafe } from "../models/DatabaseModels/cafeModel";
import { IUser } from "../models/DatabaseModels/userModel";
import { authMiddleware } from '../middleware/authMiddleware';

export class CafeRoutes {
  private _router: Router;
  private cafeService: CafeService;
  constructor() {
    this._router = Router();
    this.cafeService = new CafeService();
    this.init();
  }

  private init() {
    this._router.get("/cafes", this.getCafe.bind(this));
    this._router.get("/cafes/:cafeName", this.getCafeByName.bind(this));
    this._router.get(
      "/cafes/:cafeName/volunteer",
      this.getCafesVonlunteer.bind(this)
    );
    this._router.post(
      "/cafes/:cafeName/volunteer", authMiddleware,
      this.addVolunteer.bind(this)
    );
    this._router.delete(
      "/cafes/:cafeName/:matricule", authMiddleware,
      this.deleteVolunteer.bind(this)
    );
  }

  public get router(): Router {
    return this._router;
  }

  public async deleteVolunteer(req: Request, res: Response): Promise<void> {
    try {
      const cafeName = req.params.cafeName;
      const matricule = req.params.matricule;
      const message = await this.cafeService.deleteVolunteer(
        cafeName,
        matricule
      );
      res.status(200).send({
        message: message.message,
      });
    } catch (error) {
      console.log("Error in the deleteVolunteer:", error);
      res.status(500).send({
        message: "Internal Server Error",
        error: error,
      });
    }
  }

  public async getCafe(req: Request, res: Response): Promise<void> {
    try {
      const cafes: ICafe[] | null = await this.cafeService.getCafe();
      res.status(200).send({
        message: "Success",
        cafes: cafes,
      });
    } catch (error) {
      console.log("Error in the getCafe:", error);
      res.status(500).send({
        message: "Internal Server Error",
        error: error,
      });
    }
  }

  public async addVolunteer(req: Request, res: Response): Promise<void> {
    try {
      console.log("this is the body:", req.body);
      const cafeName: string = req.params.cafeName;
      const userName: string = req.body.userName;
      const Role: string = req.body.Role;
      const message = await this.cafeService.addVolunteer(
        cafeName,
        userName,
        Role
      );
      res.status(200).send({
        message: message.message,
      });
    } catch (error) {
      console.log("Error in the addVolunteer:", error);
      res.status(500).send({
        message: "Internal Server Error",
        error: error,
      });
    }
  }

  public async getCafeByName(req: Request, res: Response): Promise<void> {
    try {
      const cafeName = req.params.cafeName;
      const cafe: ICafe | null = await this.cafeService.getCafeByName(cafeName);
      res.status(200).send({
        message: "Success",
        cafe: cafe,
      });
    } catch (error) {
      console.log("Error in the getCafeByName:", error);
      res.status(500).send({
        message: "Internal Server Error",
        error: error,
      });
    }
  }

  public async getCafesVonlunteer(req: Request, res: Response): Promise<void> {
    try {
      const cafeName = req.params.cafeName;
      const cafesVonlunteer: IUser[] =
        await this.cafeService.getCafesVonlunteer(cafeName);
      res.status(200).send({
        message: "Success",
        volunteers: cafesVonlunteer,
      });
    } catch (err) {
      console.log("Error in the getCafesVonlunteer:", err);
      res.status(500).send({
        message: "Internal Server Error",
        error: err,
      });
    }
  }
}
