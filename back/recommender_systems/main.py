import recommender_systems.routines.run_bot_recommendations as RunBotRec
import recommender_systems.routines.run_public_recommendations as RunPublicRec
import recommender_systems.routines.run_users_recommendations as RunUsersRec
import recommender_systems.routines.health_score as RunScoreUpdate
import recommender_systems.routines.clustering as RunClustering
import recommender_systems.routines.run_cafe_recommendations as RunCafeRec
import sys

def main(action: str) -> None:
    match action:
        case "clustering":
            RunClustering.update_item_cluster()

        case "health_score":
            RunScoreUpdate.update_items_health_score()

        case "bot":
            RunBotRec.update_bot_recommendations()

        case "public":
            RunPublicRec.update_public_recommendations()

        case "cafe":
            RunCafeRec.update_cafe_recommendations()

        case "users":
            RunUsersRec.update_users_recommendations()

        case "preprocess":
            RunClustering.update_item_cluster()
            RunScoreUpdate.update_items_health_score()

        case "recommenders":
            RunBotRec.update_bot_recommendations()
            RunPublicRec.update_public_recommendations()
            RunCafeRec.update_cafe_recommendations()
            RunUsersRec.update_users_recommendations()

        case "all" | _:
            print("Running all...")
            RunClustering.update_item_cluster()
            RunScoreUpdate.update_items_health_score()
            RunBotRec.update_bot_recommendations()
            RunPublicRec.update_public_recommendations()
            RunCafeRec.update_cafe_recommendations()
            RunUsersRec.update_users_recommendations()


if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else ""
    main(action)