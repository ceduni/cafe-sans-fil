export class CafeMenu {
    constructor(data) {
        this.cafe = data.cafe;
        this.items = data.items.map(item => new CafeMenuItem(item));
    }
}

export class CafeMenuItem {
    constructor(data) {
        this.slug = data.slug;
        this.name = data.name;
        this.tags = data.tags;
        this.description = data.description;
        this.available = data.in_stock;
        this.category = data.category;
        this.image = data.image_url;
        this.price = Number(data.price);
        this.options = data.options;
    }
}

class MenuItemOption {
    constructor(data) {
        this.type = data.type;
        this.value = data.moyenne;
        this.fee = data.fee;
        
    }
}