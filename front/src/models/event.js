export class Event {
    constructor(data) {
        this.id = data.id;
        this.name = data.name;
        this.creator = data.creator.id;
        this.cafes = data.cafes.map(cafe => cafe.id);        
        this.description = data.description;
        this.image_url = data.image_url;
        this.start_date = data.start_date;
        this.end_date = data.end_date;
        this.location = data.location;
        this.interactions = new Interactions(data.interactions);
        
        //these are undefined
        this.slug = data.slug;
        this.closed = !data.is_open;
        this.status = data.status_message;
        this.hours = data.faculty;
    }
}

class Interactions {
    constructor(data) {
        data.map((interaction) => {
            switch(interaction.type){
                case "ATTEND":
                    this.attend = {count: interaction.count, me: interaction.me}
                    break;
                case "LIKE":
                    this.likes = {count: interaction.count, me: interaction.me};
                    break;
                case "SUPPORT":
                    this.support = {count: interaction.count, me: interaction.me};
            }
        })      
    }
}