import { ListCollectionsCursor, UUID } from "mongodb";
import { OrderedItems } from "./OrderedItem";
import { v4 as uuidv4 } from 'uuid';
import { OrderStatus } from "./OrderStatus";

class SalesModel{
    private orderID:string;
    private orderNumber:number;
    private cafeName:string;
    private cafeSlug:string;
    private cafeImageUrl:string;
    private items:OrderedItems[];
    private totalPrice:number;
    private status:OrderStatus 
    private createAt:Date;
    private updatedAt:Date

    public constructor(
        orderID:string,
        orderNumber:number,
        cafeName:string,
        cafeSlug:string,
        cafeImageUrl:string,
        items:OrderedItems[],
        totalPrice:number,
        status:OrderStatus,
        createAt:Date,
        updatedAt:Date
       )
       {
            this.orderID = orderID;
            this.orderNumber = orderNumber
            this.cafeName = cafeName;
            this.cafeSlug  = cafeSlug;
            this.cafeImageUrl = cafeImageUrl;
            this.items = items;
            this.totalPrice = totalPrice;
            this.status = status;
            this.createAt =createAt;
            this.updatedAt = updatedAt;
        }

}