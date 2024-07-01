import { error } from "console";

export class OrderedItem{
   public itemPrice: number;
   public itemSlug: string;
   public options: { fee: number; type: string; value: string }[];
   public quantity: number;

   constructor(itemPrice: number, itemSlug: string, options: { fee: number; type: string; value: string }[], quantity: number) {
    this.itemPrice = itemPrice;
    this.itemSlug = itemSlug;
    this.options = options;
    this.quantity = quantity;
}

    public static  validateFee(fee:number){
        if(fee < 0.0){
            throw error("the fee can't be less than 0.0");
        }
        return fee;
    }

}
