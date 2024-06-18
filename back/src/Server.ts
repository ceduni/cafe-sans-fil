import express, {Application} from 'express';

export class Server {

    private app: Application;
    private readonly PORT;

    public  constructor(){
        this.app = express();
        this.PORT = process.env.PORT || 3000;

    }

    public getIndex(path:string):void{
        this.app.get(path, (req, res) =>{
            res.status(200).send("Hello World");
        });
    }

    public   listen(){
        this.app.listen(this.PORT, () =>{
            console.log(`Server is running on port ${this.PORT}`);
        });

    }

    public get App():Application{
        return this.app;

    }




   
}

