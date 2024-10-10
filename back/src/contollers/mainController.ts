import express, { Application } from "express";
import { ProductRoutes } from "../routes/productRoutes";
import { UserRoutes } from "../routes/userRoutes";
import { CafeRoutes } from "../routes/cafeRoutes";
import { ShiftRoutes } from "../routes/shiftRoutes";
import { Database } from "../database/DataBase";
import { MessageService } from "../services/messageServices";
import { MessageRoutes } from "../routes/messageRoutes";

// Charger les variables d'environnement
require("dotenv").config({ path: ".env" });

export class MainController {
  private app: Application;
  private readonly PORT;
  private database: Database;
  private productRoute: ProductRoutes;
  private userRoute: UserRoutes;
  private shiftRoute: ShiftRoutes;
  private cafeRoute: CafeRoutes;
  private messageRoute: MessageRoutes;

  public constructor() {
    this.app = express();
    this.PORT = process.env.PORT || 3000;
    this.database = new Database(`${process.env.MONGODB_URI}` || "");
    this.productRoute = new ProductRoutes();
    this.userRoute = new UserRoutes();
    this.shiftRoute = new ShiftRoutes();
    this.cafeRoute = new CafeRoutes();
    this.messageRoute = new MessageRoutes();

    this.init();
  }

  private init() {
    this.database.connect();
    this.app.use(express.json());
    this.getAllRoutes();
  }

  public getIndex(path: string): void {
    this.app.get(path, (req, res) => {
      res.status(200).send("Hello World");
    });
  }

  public listen() {
    this.app.listen(this.PORT, () => {
      console.log(`the server is running on http://localhost:${this.PORT}`);
    });
  }

  public async closeDatabaseConnection() {
    await this.database.disconnect();
  }

  /**
   * @returns
   */

  public getAllRoutes() {
    // console.log(`this is my Routes ${this.productRoute.router}`);
    this.app.use("/api/v1", this.productRoute.router);
    this.app.use("/api/v1", this.cafeRoute.router);
    this.app.use("/api/v1", this.userRoute.router);
    this.app.use("/api/v1", this.shiftRoute.router);
    this.app.use("/api/v1", this.messageRoute.router);
  }
  /**
   * this method will call the Productcontroller class to
   * get the amount of orders made for a specific product.
   * @param product the product we are looking to get the amount of orders
   * @returns the amount of orders for a specific product
   */
  public getOrders(productID: number): number {
    return this.productRoute.getOrders(productID);
  }
  /**
   *
   */
  public get App(): Application {
    return this.app;
  }
}
