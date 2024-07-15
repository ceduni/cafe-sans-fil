import { NextFunction, Router, Request, Response } from "express";
import { ProductService } from "../services/productService";
import OrdersModel from "../src/models/OrdersModel";

export class ProductRoutes {
  getOrders(id: any): number {
    throw new Error("Method not implemented.");
  }

  private _router: Router;
  private productService: ProductService;
  private readonly STOCK = "stocks";
  private readonly ORDERS = "orders";

  constructor() {
    this._router = Router();
    this.productService = new ProductService();
    this.init();
  }

  public async getSales(req: Request, res: Response, next: NextFunction) {
    try {
      let product: string = req.params.productName;
      let category = req.query.category as string;
      const sales: OrdersModel[] = await this.productService.getSales(
        this.ORDERS,
        product
      );
      res.status(200).send({
        message: "Success",
        Sales: sales,
      });
    } catch (err) {
      console.log("Error in the getSales:", err);
      res.status(500).send({
        message: "Internal Server Error",
        error: err,
      });
    }
  }

  public async getStock(req: Request, res: Response, next: NextFunction) {
    try {
      const stock = await this.productService.getStock();
      res.status(200).send({
        message: "Success",
        Stock: stock,
      });
    } catch (err) {
      console.log("Error in the getSales:", err);
      res.status(500).send({
        message: "Internal Server Error",
        error: err,
      });
    }
  }

  /**
   * this method initializes all the product routes
   */
  private init(): void {
    this._router.get("/orders", this.getSales.bind(this));
    this._router.get("/orders/:productName", this.getSales.bind(this));
    this._router.get("/stock", this.getStock.bind(this));
  }
  public get router(): Router {
    return this._router;
  }
}
