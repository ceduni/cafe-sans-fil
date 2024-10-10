import { Router, Request, Response } from "express";
import { MessageService } from "../services/messageServices";
import { authMiddleware } from '../middleware/authMiddleware';

export class MessageRoutes {
  private _router: Router;
  private messageService: MessageService;

  constructor() {
    this._router = Router();
    this.messageService = new MessageService();
    this.init();
  }
  
  private init() {
    this._router.post("/messages", this.sendMessage.bind(this));
    this._router.get("/messages/:senderId/:receiverId", this.getMessages.bind(this));
  }

  public get router(): Router {
    return this._router;
  }

  public async sendMessage(req: Request, res: Response) {
    const { receiverIds, content } = req.body;
    const senderId = req.user._id; // Assuming user ID is in req.user after token verification

    try {
      await this.messageService.sendMessage(senderId, receiverIds, content);
      res.status(201).json({ message: "Message sent successfully" });
    } catch (err) {
      res.status(500).json({ message: "Internal Server Error", error: err });
    }
  }

  public async getMessages(req: Request, res: Response) {
    const { senderId, receiverId } = req.params;

    try {
      const messages = await this.messageService.fetchMessagesBetween(senderId, receiverId);
      res.status(200).json({ messages });
    } catch (err) {
      res.status(500).json({ message: "Internal Server Error", error: err });
    }
  }
}
