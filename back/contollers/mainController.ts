import express, { Application } from "express";
import { ProductRoutes } from "../routes/productRoutes";
import { UserRoutes } from "../routes/userRoutes";
import { CafeRoutes } from "../routes/cafeRoutes";
import { ShiftRoutes } from "../routes/shiftRoutes";
import { Database } from "../src/database/DataBase";

export class MainController {
  private app: Application;
  private readonly PORT;
  private database: Database;
  private productRoute: ProductRoutes;
  private userRoute: UserRoutes;
  private shiftRoute: ShiftRoutes;
  private cafeRoute: CafeRoutes;

  public constructor() {
    this.app = express();
    this.PORT = process.env.PORT || 3000;
    this.database = new Database(
      "mongodb+srv://cafe:sans-fil@cluster0.ti5co91.mongodb.net/sales?retryWrites=true&w=majority"
    );

    this.productRoute = new ProductRoutes();
    this.userRoute = new UserRoutes();
    this.shiftRoute = new ShiftRoutes();
    this.cafeRoute = new CafeRoutes();

    this.init();
  }

  private init() {
    this.database.connect();
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
