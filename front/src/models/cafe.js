import { CafeMenu } from "./menu";

const isAdmin = (user) => user.role === "Admin";
const isVolunteer = (user) => user.role === "Bénévole";

export class Cafe {
    constructor(data) {
        this.id = data.id;
        this.name = data.name;
        this.slug = data.slug;
        this.description = data.description;
        this.logo = data.logo_url;
        this.image = data.banner_url;
        this.closed = !data.is_open;
        this.status = data.status_message;
        this.socials = data.social_media;
        this.location = new Location(data.location);
        this.openingHours = data.opening_hours.map(x => new OpeningHour(x));
        this.owner = data.owner;
        this.features = data.features ?? [];

        if (data.menu) {
            this.menu = new CafeMenu(data.menu);
        }
        if (data.staff) {
            this.staff = data.staff;
        }
        if (data.contact) {
            this.contact = data.contact;
        }
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

    get coordinates() {
        return this.location.coordinates;
    }

    get managers() {
        return this.staff.admins;
    }
    get volunteers() {
        return this.staff.volunteers;
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
        console.log("Creating Location with data:", data);
        this.pavillon = data.pavillon;
        this.local = data.local;
        this.floor = data.floor;
        if (data.geometry) {
            this.coordinates = [data.geometry?.coordinates[1], data.geometry?.coordinates[0]];
        }
    }

    toString() {
        return `${this.pavillon}, ${this.local} (${this.floor})`;
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