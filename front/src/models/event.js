export class Event {
    constructor(data) {
        this.id = data.id;
        this.name = data.name;
        this.creator = data.creator_id;
        this.editors = data.editors.map(user => user.id);
        this.cafe_ids = data.cafes.map(cafe => cafe.id);        
        this.description = data.description;
        this.image_url = data.image_url;
        this.start_date = data.start_date;
        this.end_date = data.end_date;
        this.ticket = data.ticket;
        this.location = data.location;
        this.max_support = data.max_support;
        this.interactions = new Interactions(data.interactions);
    }
}

class Interactions {
    constructor(data) {
        data.map((interaction) => {
            switch(interaction.type){
                case "ATTEND":
                    this.ATTEND = {count: interaction.count, me: interaction.me}
                case "LIKE":
                    this.LIKE = {count: interaction.count, me: interaction.me};
                case "SUPPORT":
                    this.SUPPORT = {count: interaction.count, me: interaction.me};
            }
        })      
    }
}