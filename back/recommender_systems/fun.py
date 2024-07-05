from recommender_systems.api.cafe_api import CafeApi as CafeAPI

def main():
    response, status = CafeAPI.get_cafes( params = {'sort_by': 'name', 'page': 1, 'limit': 40} )
    print(response)

if __name__ == "__main__":
    main()