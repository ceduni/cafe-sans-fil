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

    public async getSales(req: Request, res: Response, next: NextFunction){
        
        try{
            let product:string = req.params.productName;
            console.log("this is the product:",product);
            
            const sales = await this.productService.getSales(product);
            res.status(200).send({
                message: 'Success',
                Sales: sales,
            });
           
        }
        catch(err){
            console.log('Error in the getSales:',err);
            res.status(500).send({
                message: 'Internal Server Error',
                error: err,
            });
        }

    }
  
            //  req.flash('info',`this is the number of sales for product  ${productID}`);



    init() {
        this._router.get('/sales',this.getSales.bind(this));
        this._router.get('/sales/:productName',this.getSales.bind(this));
    }

    public get router(): Router{
        return this._router;
    }



  

}