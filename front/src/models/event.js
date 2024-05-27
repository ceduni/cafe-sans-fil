export class Event {
    constructor(data) {
        this.id = data.cafe_id;
        this.name = data.name;
        this.slug = data.slug;
        this.description = data.description;
        this.image = data.image_url;
        this.closed = !data.is_open;
        this.status = data.status_message;
        this.hours = data.faculty;
    }
}
