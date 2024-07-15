import { Schema, Document, model } from "mongoose";

// Interface for a single shift
interface IShiftDetail extends Document {
  date: Date;
  startTime: string;
  endTime: string;
}

// Interface for the main Shift document
interface IShift extends Document {
  cafe_name: string;
  matricule: string;
  shift: IShiftDetail[];
}

// Schema for a single shift detail
const ShiftDetailSchema: Schema = new Schema({
  date: { type: Date, required: true },
  startTime: { type: String, required: true },
  endTime: { type: String, required: true },
});

// Main Shift schema
const ShiftSchema: Schema = new Schema({
  cafe_name: { type: String, required: true },
  matricule: { type: String, required: true },
  shift: { type: [ShiftDetailSchema], required: true },
});

// Creating the models
const ShiftDetailModel = model<IShiftDetail>("ShiftDetail", ShiftDetailSchema);
const ShiftModel = model<IShift>("Shift", ShiftSchema, "shifts"); // for selecting the collection

export { ShiftModel, IShift, ShiftDetailModel, IShiftDetail };
