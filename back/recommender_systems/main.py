import recommender_systems.routines.run_public_recommendations as RunPublicRec
import recommender_systems.routines.run_users_recommendations as RunUsersRec
import recommender_systems.routines.health_score as RunScoreUpdate
import recommender_systems.routines.clustering as RunClustering
import recommender_systems.routines.run_cafe_recommendations as RunCafeRec
import recommender_systems.routines.cafe_health_score as RunCafeHealth
import sys

def main(action: str) -> None:
    match action:
        case "cafe_health_score":
            RunCafeHealth.update_cafes_health_score()

        case "clustering":
            RunClustering.update_item_cluster()

        case "item_health_score":
            RunScoreUpdate.update_items_health_score()

        case "public":
            RunPublicRec.update_public_recommendations()

        case "cafe":
            RunCafeRec.update_cafe_recommendations()

        case "users":
            RunUsersRec.update_users_recommendations()

        case "item_full_update":
            RunClustering.update_item_cluster()
            RunScoreUpdate.update_items_health_score()

        case "cafe_full_update":
            RunCafeHealth.update_cafes_health_score()
            RunPublicRec.update_public_recommendations()

        case "preprocess":
            RunClustering.update_item_cluster()
            RunScoreUpdate.update_items_health_score()

        case "recommenders":
            RunPublicRec.update_public_recommendations()
            RunCafeRec.update_cafe_recommendations()
            RunUsersRec.update_users_recommendations()

        case "all":
            print("Running all...")
            RunClustering.update_item_cluster()
            RunCafeHealth.update_cafes_health_score()
            RunScoreUpdate.update_items_health_score()
            RunPublicRec.update_public_recommendations()
            RunCafeRec.update_cafe_recommendations()
            RunUsersRec.update_users_recommendations()

        case _:
            print("This action is not valid")


if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else ""
    main(action)