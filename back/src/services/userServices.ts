import { IUser, UserModel } from "../models/DatabaseModels/userModel";
import jwt from "jsonwebtoken";

export class UserService {
  public constructor() {}

  public async getUser(): Promise<IUser[]> {
    try {
      const result = await UserModel.find({});
      return result;
    } catch (err) {
      console.error("Error fetching user data:", err);
      return [];
    }
  }

  public async getUserByEmail(email: string): Promise<IUser | null> {
    try {
      const result = await UserModel.findOne({ email: email }).exec();
      return result;
    } catch (err) {
      console.error("Error fetching user data:", err);
      return null;
    }
  }

  public async getUserByMatricule(matricule: string): Promise<IUser | null> {
    // this.database.connect();
    try {
      const result = await UserModel.findOne({ matricule: matricule }).exec();
      return result;
    } catch (err) {
      console.error("Error fetching user data:", err);
      return null;
    }
  }
  // Nouvelle méthode pour trouver un utilisateur par jeton
  public async getUserByToken(token: string): Promise<IUser | null> {
    const decoded: any = jwt.verify(token, process.env.PHRASE_PASS!);
    return await UserModel.findOne({ _id: decoded._id, "authTokens.authToken": token }).exec();
  }
}

export default UserService;
