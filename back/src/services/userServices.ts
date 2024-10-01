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
    try {
      const decoded: any = jwt.verify(token, process.env.PHRASE_PASS!);
      return await UserModel.findOne({ _id: decoded._id, "authTokens.authToken": token }).exec();
    } catch (error) {
        console.error("Error verifying token:", error);
        return null;
    }
  }
  public async logout(authToken: string): Promise<boolean> {
    try {
        const decoded: any = jwt.verify(authToken, process.env.PHRASE_PASS!);
        const user = await UserModel.findOne({ _id: decoded._id }).exec();

        if (!user) {
            console.error("User not found");
            return false;
        }

        user.authTokens = user.authTokens.filter(token => token.authToken !== authToken);
        await user.save();
        return true;
    } catch (err) {
        console.error("Error logging out user:", err);
        return false;
    }
  }

}

export default UserService;
