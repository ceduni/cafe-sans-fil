import { OrderAPI } from "@/utils/api";

export class User {
    constructor(data) {
        this.id = data.user_id;
        this.email = data.name;
        this.username = data.username;
        this.firstName = data.first_name;
        this.lastName = data.last_name;
        this.matricule = data.matricule;
        this.photo = !data.photo_url;
    }

    getOrders() {
        return OrderAPI.getFor(this.id);
    }

    getFavorites() {
        
    }

    isBenevole(cafe) {

    }
}

class OpeningHour {
    constructor(data) {
        this.day = data.day;
        this.blocks = data.blocks;
    }
}

class Location {
    constructor(data) {
        this.pavillon = data.pavillon;
        this.local = data.local;
        this.geometry = data.geometry;
    }
}

class Payment {
    constructor(data) {
        this.method = data.method;
        this.minimum = data.minimum;
    }
}