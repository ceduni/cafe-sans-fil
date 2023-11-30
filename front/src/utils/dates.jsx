import moment from "moment-timezone";

export const UTCToMontrealTime = (date) => {
  return moment.utc(date).local().format("YYYY-MM-DDTHH:mm:ss");
};
