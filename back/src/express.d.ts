import { UserModel } from'back/src/models/DatabaseModels/userModel';
declare global {
    namespace Express {
        interface Request {
            user?: UserModel;
        }
    }
}