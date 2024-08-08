import { Router, Request, Response } from "express";
import { UserService } from "../services/userServices";
import { IUser } from "../models/DatabaseModels/userModel";

export class UserRoutes {
  private _router: Router;
  private userService: UserService;
  constructor() {
    this._router = Router();
    this.userService = new UserService();
    this.init();
  }

  private init() {
    this._router.get("/users", this.getUser.bind(this));
    this._router.get("/users/email/:email", this.getUserByEmail.bind(this));
    this._router.get(
      "/users/matricule/:matricule",
      this.getUserByMatricule.bind(this)
    );
  }

  public get router(): Router {
    return this._router;
  }

  public async getUser(req: Request, res: Response) {
    try {
      const users = await this.userService.getUser();

      res.status(200).send({
        message: "Success",
        Users: users,
      });
    } catch (err) {
      console.log("Error in the getUser:", err);
      res.status(500).send({
        message: "Internal Server Error",
        error: err,
      });
    }
  }

  public async getUserByEmail(req: Request, res: Response) {
    try {
      const email = req.params.email;
      const user: IUser | null = await this.userService.getUserByEmail(email);
      res.status(200).send({
        message: "Success",
        User: user,
      });
    } catch (err) {
      console.log("Error in the getUser:", err);
      res.status(500).send({
        message: "Internal Server Error",
        error: err,
      });
    }
  }

  public async getUserByMatricule(req: Request, res: Response) {
    try {
      const matricule = req.params.matricule;
      const user: IUser | null = await this.userService.getUserByMatricule(
        matricule
      );
      res.status(200).send({
        message: "Success",
        User: user,
      });
    } catch (err) {
      console.log("Error in the getUserByMatricule:", err);
      res.status(500).send({
        message: "Internal Server Error",
        error: err,
      });
    }
  }
}
