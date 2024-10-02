import { NextFunction, Router, Request, Response } from "express";
import { ProductService } from "../services/productService";
import { authMiddleware } from '../middleware/authMiddleware';

export class ProductRoutes {
  getOrders(id: any): number {
    throw new Error("Method not implemented.");
  }

  private _router: Router;
  private productService: ProductService;
  private readonly STOCK = "stocks";

  constructor() {
    this._router = Router();
    this.productService = new ProductService();
    this.init();
  }

  public async getSales(req: Request, res: Response, next: NextFunction) {
    try {
      let productName: string = req.params.productName;
      console.log("productName Route", productName);
      let category = req.query.category as string;
      const sales = await this.productService.getSales(productName);
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

  public async addOrder(req: Request, res: Response, next: NextFunction) {
    try {
      const order = req.body;
      const newOrder = await this.productService.addOrder(order);
      res.status(200).send({
        message: newOrder.message,
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
    // orders
    this._router.get("/orders", this.getSales.bind(this));
    this._router.post("/orders", authMiddleware,this.addOrder.bind(this));

    this._router.get("/orders/:productName", this.getSales.bind(this));
    this._router.get("/stocks", this.getStock.bind(this));
  }
  public get router(): Router {
    return this._router;
  }
}
