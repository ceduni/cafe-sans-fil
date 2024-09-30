import { Schema, Document, model, Collection } from "mongoose";
import bcrypt from "bcrypt";
import jwt from "jsonwebtoken";

interface IAuthToken {
  authToken: string;
}
interface IUser extends Document {
  user_id: String;
  email: string;
  matricule: string;
  username: string;
  hashed_password: string;
  first_name: string;
  last_name: string;
  photo_url: string;
  failed_login_attempts: number;
  last_failed_login_attempt: Date | null;
  lockout_until: Date | null;
  is_active: boolean;
  work_at: string;
  authTokens: IAuthToken[];
  comparePassword(password: string): Promise<boolean>;
  generateAuthToken(): Promise<string>;
}

const UserSchema: Schema = new Schema({
  user_id: { type: String, required: true, unique: true },
  email: { type: String, required: true, unique: true },
  matricule: { type: String, required: true, unique: true },
  username: { type: String, required: true, unique: true },
  hashed_password: { type: String, required: true },
  first_name: { type: String, required: true },
  last_name: { type: String, required: true },
  photo_url: { type: String },
  failed_login_attempts: { type: Number, default: 0 },
  last_failed_login_attempt: { type: Date, default: null },
  lockout_until: { type: Date, default: null },
  is_active: { type: Boolean, default: true },
  work_at: { type: String },
  authTokens: [{
    authToken: {
      type: String,
      required: true 
    }
  }],
  
});

// Méthodes de comparaison de mot de passe
UserSchema.methods.comparePassword = async function (password: string): Promise<boolean> {
  return bcrypt.compare(password, this.hashed_password);
};

// Méthode pour générer un jeton JWT
UserSchema.methods.generateAuthToken = async function (): Promise<string> {
  const token = jwt.sign({ _id: this._id }, process.env.PHRASE_PASS!, {
    expiresIn: "1h",
  });
  this.authTokens.push({ authToken: token });
  await this.save();
  return token;
};

const UserModel = model<IUser>("User", UserSchema, "users"); // for selecting the collection
export { UserModel, IUser };
