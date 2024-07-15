import { CafeModel, ICafe } from "../src/models/DatabaseModels/cafeModel";
import { IUser, UserModel } from "../src/models/DatabaseModels/userModel";
import Database from "./DataBase";

export class CafeService {
  private database: Database | undefined;
  public static readonly DB_NAME = "sales";
  public constructor() {}
  public async getCafe(): Promise<ICafe[]> {
    this.database = await Database.getInstance(CafeService.DB_NAME);
    try {
      const result = await CafeModel.find().exec();
      return result;
    } catch (err) {
      console.error("Error fetching cafe data:", err);
      return [];
    } finally {
      this.database.close();
    }
  }

  public async getCafeByName(cafe_name: string): Promise<ICafe | null> {
    this.database = await Database.getInstance(CafeService.DB_NAME);
    try {
      const cafe: ICafe | null = await CafeModel.findOne({
        name: cafe_name,
      }).exec();
      return cafe;
    } catch (err) {
      console.error("Error fetching cafe data:", err);
      return null;
    } finally {
      this.database.close();
    }
  }

  public async getCafesVonlunteer(cafe_name: string): Promise<IUser[]> {
    this.database = await Database.getInstance(CafeService.DB_NAME);
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

        console.log(cafesVonlunteer);

        const volunteers: IUser[] | null = await UserModel.find({
          matricule: { $in: cafesVonlunteer },
        }).exec();

        return volunteers;
      }
      return []; // Return an empty array if cafeStaff is null
    } catch (error) {
      console.error(error);
      return [];
    } finally {
      this.database.close();
    }
  }
}

export default CafeService;
