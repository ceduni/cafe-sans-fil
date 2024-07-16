import mongoose from "mongoose";

export class Database {
  private uri: string;

  constructor(uri: string) {
    this.uri = uri;
  }

  public async connect(): Promise<void> {
    try {
      await mongoose.connect(this.uri, {});
      console.log("Connected to the database");
    } catch (error) {
      console.error("Database connection error:", error);
      process.exit(1); // Exit the process with failure
    }
  }

  public async disconnect(): Promise<void> {
    try {
      await mongoose.disconnect();
      console.log("Disconnected from the database");
    } catch (error) {
      console.error("Database disconnection error:", error);
    }
  }
}
