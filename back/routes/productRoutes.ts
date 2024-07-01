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
            let category = req.query.category as string;
            if(category){
                const sales = await this.productService.getSalesByCategory(category); 
                res.status(200).send({
                    message: 'Success',
                    Sales: sales,
                });
                
            }
            else{
                const sales = await this.productService.getSales(product); 
                res.status(200).send({
                    message: 'Success',
                    Sales: sales,
                });
                
            }
           
           
        }
        catch(err){
            console.log('Error in the getSales:',err);
            res.status(500).send({
                message: 'Internal Server Error',
                error: err,
            });
        }

    }

    



    /**
     * this method initializes all the product routes
     */
    private init():void {
        this._router.get('/orders',this.getSales.bind(this));
        this._router.get('/orders/:productName',this.getSales.bind(this));
        
        
    }
    public get router(): Router{
        return this._router;
    }



  

}