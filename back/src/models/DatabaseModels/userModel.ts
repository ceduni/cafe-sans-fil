import { Schema, Document, model, Collection } from "mongoose";

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
});

const UserModel = model<IUser>("User", UserSchema, "users"); // for selecting the collection
export { UserModel, IUser };
