import moment from "moment-timezone";
import i18next from 'i18next'

const trad = (key, def) => i18next.t(key, { defaultValue: def });

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

const upper = (string, index = 0) => {
    return string.charAt(index).toUpperCase() + string.slice(1);
};

const lower = (string, index = 0) => {
    return string.charAt(index).toLowerCase() + string.slice(1);
};

export const displayCafeLocation = (location) => {
    if (!location || !location.pavillon) {
        return "";
    }

    return `${upper(location.pavillon)}, ${lower(location.local)}`;
};

export const shouldDisplayInfo = (object) => {
    if (!object) {
        return false;
    }

    const now = new Date();
    const defaultStartTime = new Date("1900-01-01T00:00:00.000Z");
    const defaultEndTime = new Date("9999-12-31T23:59:59.999Z");

    const start = object.start ? new Date(object.start) : defaultStartTime;
    const end = object.end ? new Date(object.end) : defaultEndTime;

    return object.value && now >= start && now <= end;
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
    if (!openingHours || openingHours.length === 0) {
        return "Indisponible";
    }

    const now = moment().tz("America/Montreal");
    const weekDays = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"];

    const todayIndex = weekDays.indexOf(mapDayEnglishToFrench(now.format("dddd").toLowerCase()));
    const daysInWeek = weekDays.length;

    const todaySchedule = openingHours.find((d) => d.day.toLowerCase() === weekDays[todayIndex]);
    if (todaySchedule && todaySchedule.blocks && todaySchedule.blocks.length > 0) {
        for (const block of todaySchedule.blocks) {
            const startTime = moment(block.start, "HH:mm");
            if (now.isBefore(startTime)) {
                return `Ouvre à ${block.start} ${weekDays[todayIndex].slice(0, 3)}.`;
            }
        }
    }

    for (let i = 1; i <= daysInWeek; i++) {
        const dayIndex = (todayIndex + i) % daysInWeek;
        const dayName = weekDays[dayIndex];

        const daySchedule = openingHours.find((d) => d.day.toLowerCase() === dayName);
        if (daySchedule && daySchedule.blocks && daySchedule.blocks.length > 0) {
            const firstBlock = daySchedule.blocks[0];
            return `Ouvre à ${firstBlock.start} ${dayName.slice(0, 3)}.`;
        }
    }

    return "Indisponible";
};

export const PAYMENT_METHODS = {
    CASH: trad("payment.cash", "Argent comptant"),
    CREDIT_CARD: trad("payment.credit", "Carte de crédit"),
    DEBIT_CARD: trad("payment.debit", "Carte de débit"),
};
