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

export const getClosingTimeToday = (openingHours) => {
  if (!openingHours) return { closingTime: "", isBreak: false };

  const now = moment().tz("America/Montreal");
  const todayEnglish = now.format("dddd").toLowerCase();
  const todayFrench = mapDayEnglishToFrench(todayEnglish);

  const currentDay = openingHours.find((day) => day.day.toLowerCase() === todayFrench);
  if (!currentDay || !currentDay.blocks || currentDay.blocks.length === 0) return { closingTime: "", isBreak: false };

  for (let i = 0; i < currentDay.blocks.length; i++) {
    const block = currentDay.blocks[i];
    const startTime = moment(block.start, "HH:mm");
    const endTime = moment(block.end, "HH:mm");

    if (now.isBetween(startTime, endTime) || now.isSameOrBefore(startTime)) {
      const isBreak = i < currentDay.blocks.length - 1;
      return { closingTime: block.end, isBreak };
    }
  }

  return { closingTime: "", isBreak: false };
};

export const getNextOpeningTime = (openingHours) => {
  if (!openingHours || openingHours.length === 0) return "Indisponible";

  const now = moment().tz("America/Montreal");
  const weekDays = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"];

  const todayIndex = weekDays.indexOf(mapDayEnglishToFrench(now.format("dddd").toLowerCase()));
  const daysInWeek = weekDays.length;

  for (let i = 0; i < daysInWeek; i++) {
    const dayIndex = (todayIndex + i) % daysInWeek;
    const dayName = weekDays[dayIndex];

    const daySchedule = openingHours.find((d) => d.day.toLowerCase() === dayName);
    if (daySchedule && daySchedule.blocks && daySchedule.blocks.length > 0) {
      for (const block of daySchedule.blocks) {
        const startTime = moment(block.start, "HH:mm").day(dayIndex);

        if (dayIndex !== todayIndex || now.isBefore(startTime)) {
          return `Ouvre à ${block.start} ${dayName.slice(0, 3)}.`;
        }
      }
    }
  }

  return "Indisponible";
};





export const isCafeActuallyOpen = (isOpen, openingHours) => {
  return isOpen && isNowWithinOpeningHours(openingHours);
};

export const PAYMENT_METHODS = {
  CASH: "Argent comptant",
  CREDIT_CARD: "Carte de crédit",
  DEBIT_CARD: "Carte de débit",
};
