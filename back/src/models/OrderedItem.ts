import { error } from "console";

export class OrderedItems{
    private type:string;
    private value:string;
    private fee:number;

    public constructor(type:string,value:string,fee:number){
        this.type = type;
        this.value = value;
        this.fee = fee;
    }

    public static  validateFee(fee:number){
        if(fee < 0.0){
            throw error("the fee can't be less than 0.0");
        }
        return fee;
    }

}
