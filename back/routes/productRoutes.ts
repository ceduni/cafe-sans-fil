import  { NextFunction, Router,Request, Response } from "express"
import { ProductService } from "../services/productService";

export class ProductRoutes {
    getOrders(id: any): number {
        throw new Error('Method not implemented.');
    }
    

    private _router: Router
    private productService: ProductService;

    constructor() {
        this._router = Router();
        this.productService = new ProductService();
        this.init();
    }

    public getSales(req: Request, res: Response, next: NextFunction){
        const productID:string = req.params.id;
        try{
            const num = this.productService.getSales(productID);
            const resNumber = parseInt(num, 10);
            //  req.flash('info',`this is the number of sales for product  ${productID}`);
            res.status(201)
            .send(
                {
                    message:'Success',
                    status: res.status,
                    NumSales: resNumber

                });
        }
        catch(err){
            console.log(err);
        }

    }


    init() {
        this._router.get('/sales/:id',this.getSales.bind(this));
    }

    public get router(): Router{
        return this._router;
    }



  

}