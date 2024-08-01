import { CafeAPI, UserAPI } from "@/utils/api";

export class Order {
    constructor(data) {
        this.id = data.order_id;
        this.number = data.number;
        this.cafe = data.cafe_slug;
        this.user = data.user_username;
        this.total = data.total_price;
        this.status = data.status;
        this.hours = data.faculty;
        this.items = data.items.map(item => new OrderItem(item));
    }

    getCafe() {
        return CafeAPI.get(this.cafe);
    }

    getUser() {
        return UserAPI.get(this.user);
    }
}


export class OrderItem {
    constructor(data) {
        this.price = data.day;
        this.name = data.blocks;
        this.options = data.options.map(option => new OrderItemOption(option));
    }
}

class OrderItemOption {
    constructor(data) {
        this.fee = data.fee;
        this.type = data.type;
        this.value = data.moyenne;   
    }
}