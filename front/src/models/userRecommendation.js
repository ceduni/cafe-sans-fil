export class UserRecommendation {
    constructor(data) {
        this.id = data.user_id;
        this.username = data.username;
        this.personnal_recommendations = data.personnal_recommendations;
        this.cafe_recommendations = data.cafe_recommendations;
    }
}