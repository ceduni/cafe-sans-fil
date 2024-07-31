import { CafeModel, ICafe } from "../src/models/DatabaseModels/cafeModel";
import { IUser, UserModel } from "../src/models/DatabaseModels/userModel";

export class CafeService {
  public constructor() {}
  public async getCafe(): Promise<ICafe[]> {
    try {
      const result = await CafeModel.find().exec();
      return result;
    } catch (err) {
      console.error("Error fetching cafe data:", err);
      return [];
    }
  }

  public async getCafeByName(cafe_name: string): Promise<ICafe | null> {
    try {
      const cafe: ICafe | null = await CafeModel.findOne({
        name: cafe_name,
      }).exec();
      return cafe;
    } catch (err) {
      console.error("Error fetching cafe data:", err);
      return null;
    }
  }

  public async getCafesVonlunteer(cafe_name: string): Promise<IUser[]> {
    try {
      const cafe: ICafe | null = await CafeModel.findOne({
        name: cafe_name,
      }).exec();
      const cafeStaff = cafe?.staff;
      const cafesVonlunteer = [];
      // finding all the matricules of the volunteers
      if (cafeStaff) {
        for (let i = 0; i < cafe?.staff.length; i++) {
          if (cafeStaff[i].role === "Bénévole") {
            cafesVonlunteer.push(cafeStaff[i].username);
          }
        }

        //console.log(cafesVonlunteer);

        const volunteers: IUser[] | null = await UserModel.find({
          matricule: { $in: cafesVonlunteer },
        }).exec();

        return volunteers;
      }
      return []; // Return an empty array if cafeStaff is null
    } catch (error) {
      console.error(error);
      return [];
    }
  }

  public async addVolunteerToCafeBy(cafe_name: string, matricule: string) {
    /* {
        "_id": "6696877b77e4709670766eaf",
        "username": "20140716",
        "role": "Admin"
      } */
  }


  /**
   * this function add a volunteer to the list of a staff in a specific cafe
   * @param cafeName 
   * @param matricule 
   * @param role 
   * @returns 
   */
  public async addVolunteer(cafeName: string, matricule: string, role: string): Promise<{ message: string }> {
    try {
      const cafe: ICafe | null = await CafeModel.findOne({ name: cafeName });
      if (!cafe) {
        return Promise.resolve({ message: "Cafe not found" });
      }
      else { 
        for (let i = 0; i < cafe.staff.length; i++) {
          if (cafe.staff[i].username === matricule) {
            return Promise.resolve({ message: "User already exists" });
          }
        }
        
        cafe.staff.push({ username: matricule, role: role });
        await cafe.save();
        return Promise.resolve({ message: "Success" });
      }
    } catch (error) {
      console.error(error);
      return Promise.resolve({ message: "Error occur" });
    }
  }
}






export default CafeService;
