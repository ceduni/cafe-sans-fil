import { IUser, UserModel } from "../src/models/DatabaseModels/userModel";
import Database from "./DataBase";

export class UserService {
  private database: Database | undefined;
  public static readonly DB_NAME = "sales";
  public constructor() {}

  public async getUser(): Promise<IUser[]> {
    this.database = await Database.getInstance(UserService.DB_NAME);
    try {
      const result = await UserModel.find({});
      console.log(result);
      return result;
    } catch (err) {
      console.error("Error fetching user data:", err);
      return [];
    } finally {
      this.database.close();
    }
  }

  public async getUserByEmail(email: string): Promise<IUser | null> {
    this.database = await Database.getInstance(UserService.DB_NAME);
    try {
      const result = await UserModel.findOne({ email: email }).exec();
      return result;
    } catch (err) {
      console.error("Error fetching user data:", err);
      return null;
    } finally {
      this.database.close();
    }
  }

  public async getUserByMatricule(matricule: string): Promise<IUser | null> {
    this.database = await Database.getInstance(UserService.DB_NAME);
    try {
      const result = await UserModel.findOne({ matricule: matricule }).exec();
      return result;
    } catch (err) {
      console.error("Error fetching user data:", err);
      return null;
    } finally {
      this.database.close();
    }
  }
}

export default UserService;
