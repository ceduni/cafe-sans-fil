import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import { UserModel } from '../models/DatabaseModels/userModel';

export const authMiddleware = async (req: Request, res: Response, next: NextFunction) => {
    const token = req.header("Authorization")?.replace("Bearer ", "");
    if (!token) return res.status(401).json({ message: "Token not provided" });

    try {
        const decoded: any = jwt.verify(token, process.env.PHRASE_PASS!);
        const user = await UserModel.findOne({ _id: decoded._id, "authTokens.authToken": token }).exec();
        if (!user) return res.status(401).json({ message: "User not found" });
        req.user = user; // Store user information in the request
        next(); // Move to the next middleware or route handler
    } catch (err) {
        res.status(401).json({ message: "Invalid token", error: err });
    }
};