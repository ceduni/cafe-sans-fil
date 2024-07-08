import express, {
  Application,
  NextFunction,
  Router,
  Request,
  Response,
} from "express";
import { ProductRoutes } from "../routes/productRoutes";

export class MainController {
  private app: Application;
  private readonly PORT;
  private productRoute: ProductRoutes;

  public constructor() {
    this.app = express();
    this.PORT = process.env.PORT || 3000;
    this.productRoute = new ProductRoutes();
    this.init();

    // this.router = Router()
  }

  private init() {
    this.getSales();
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

  /**
   *
   * @returns
   */

  public getSales() {
    // console.log(`this is my Routes ${this.productRoute.router}`);
    this.app.use("/api/v1", this.productRoute.router);
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
