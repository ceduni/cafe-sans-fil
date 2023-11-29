import moment from "moment-timezone";

const mapDayEnglishToFrench = (englishDayName) => {
  const dayMap = {
    monday: "lundi",
    tuesday: "mardi",
    wednesday: "mercredi",
    thursday: "jeudi",
    friday: "vendredi",
    saturday: "samedi",
    sunday: "dimanche",
  };
  return dayMap[englishDayName.toLowerCase()] || "";
};

export const toMontrealTime = (date) => {
  return moment(date).tz("America/Montreal").format("YYYY-MM-DDTHH:mm:ss");
};

export const displayCafeLocation = (location) => {
  if (!location || !location.pavillon) return "";
  return `${location.pavillon}, ${location.local}`;
};

export const shouldDisplayInfo = (object) => {
  if (!object) return false;

  const defaultStartTime = "1900-01-01T00:00:00.000Z";
  const defaultEndTime = "9999-12-31T23:59:59.999Z";

  const now = moment().tz("America/Montreal");
  const start = object.start
    ? moment(object.start).tz("America/Montreal")
    : moment(defaultStartTime).tz("America/Montreal");
  const end = object.end ? moment(object.end).tz("America/Montreal") : moment(defaultEndTime).tz("America/Montreal");

  return object.value && now.isBetween(start, end);
};

export const isNowWithinOpeningHours = (openingHours) => {
  if (!openingHours) return false;

  const now = moment().tz("America/Montreal");
  const todayEnglish = now.format("dddd").toLowerCase();
  const todayFrench = mapDayEnglishToFrench(todayEnglish);

  const currentDay = openingHours.find((day) => day.day.toLowerCase() === todayFrench);
  if (!currentDay) return false;

  return currentDay.blocks.some((block) => {
    const startTime = moment(block.start, "HH:mm");
    const endTime = moment(block.end, "HH:mm");
    return now.isBetween(startTime, endTime);
  });
};

export const isCafeActuallyOpen = (isOpen, openingHours) => {
  return isOpen && isNowWithinOpeningHours(openingHours);
};

export const PAYMENT_METHODS = {
  CASH: "Argent comptant",
  CREDIT_CARD: "Carte de crédit",
  DEBIT_CARD: "Carte de débit",
};
