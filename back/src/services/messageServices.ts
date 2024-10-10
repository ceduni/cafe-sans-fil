import { MessageModel, IMessage } from '../models/DatabaseModels/messageModel';

export class MessageService {
  public async sendMessage(senderId: string, receiverIds: string[], content: string): Promise<IMessage> {
    const message = new MessageModel({
      senderId,
      content,
      timestamp: new Date(),
    });

    // Here you could handle sending the message to multiple receivers
    const promises = receiverIds.map(receiverId => {
      const newMessage = new MessageModel({
        senderId,
        receiverId,
        content,
        timestamp: new Date(), // If you want to keep all timestamps independent
      });
      return newMessage.save();
    });

    await Promise.all(promises); // Wait for all messages to be saved
    return message; // Or return something meaningful
  }

  public async fetchMessagesBetween(senderId: string, receiverId: string): Promise<IMessage[]> {
    return await MessageModel.find({
      $or: [
        { senderId, receiverId },
        { senderId: receiverId, receiverId: senderId }
      ]
    }).sort({ timestamp: 1 }).exec(); // Sort messages by timestamp
  }
}
