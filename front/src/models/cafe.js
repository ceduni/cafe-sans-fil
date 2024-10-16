import { CafeMenuItem } from "./menu";

export class Cafe {
    constructor(data) {
        this.id = data.cafe_id;
        this.name = data.name;
        this.slug = data.slug;
        this.description = data.description;
        this.logo = data.logo_url;
        this.image = data.image_url;
        this.closed = !data.is_open;
        this.status = data.status_message;
        this.socials = data.social_media;
        this.hours = data.faculty;
        this.location = new Location(data.location);
        this.openingHours = data.opening_hours.map(x => new OpeningHour(x));
        this.paymentMethods = data.payment_methods.map(x => new Payment(x));
        if(data.menu_items) {
            this.menu = data.menu_items.map(x => new CafeMenuItem(x));
        }
        // this.announcements = data.announcements.map(x => new Announcement(x));
    }

    isOpen() {
        if (this.closed) {
            return false;
        }

        const now = new Date();
        const today = now.toLocaleString('en-US', { weekday: 'long' }).toLowerCase();
        const currentDay = this.openingHours.find((openingHour) => openingHour.day.toLowerCase() === today);

        if (!currentDay) {
            return false;
        }

        const currentTime = now.getHours() * 60 + now.getMinutes();
        return currentDay.blocks.some((block) => {
            const startTime = block.start.split(':').map(Number);
            const endTime = block.end.split(':').map(Number);
            const startMinutes = startTime[0] * 60 + startTime[1];
            const endMinutes = endTime[0] * 60 + endTime[1];
            return currentTime >= startMinutes && currentTime <= endMinutes;
        });
    }
}


// class Social {
//     constructor(data) {
//         this.name = data.platform_name;
//         this.url = data.link;
//     }

//     get logo() {
//         return Logo[this.name.toLowerCase()];
//     }
// }

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

    toString() {
        return `${this.pavillon}, ${this.local}`;
    }
}

class Payment {
    constructor(data) {
        this.method = data.method;
        this.minimum = data.minimum;
    }
}

class Announcement {
    constructor(data) {
        this.title = data.title;
        this.content = data.content;
        this.creationDate = data.created_at;
        this.likes = data.likes;
        this.tags = data.tags;
    }
}