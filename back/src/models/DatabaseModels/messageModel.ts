import { Schema, Document, model } from "mongoose";

interface IMessage extends Document {
  senderId: string;
  receiverId: string;
  content: string;
  timestamp: Date;
}

const MessageSchema: Schema = new Schema({
  senderId: { type: String, required: true },
  receiverId: { type: String, required: true },
  content: { type: String, required: true },
  timestamp: { type: Date, default: Date.now },
});

const MessageModel = model<IMessage>("Message", MessageSchema, "messages");
export { MessageModel, IMessage };
