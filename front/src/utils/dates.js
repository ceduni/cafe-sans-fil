import dayjs from "dayjs";

export const UTCToMontrealTime = (date) => {
  const localDate = new Date(date); // date is assumed to be in UTC
  return dayjs(localDate).format("YYYY-MM-DDTHH:mm:ss");
};

const isValidTimestamp = (timestamp) => {
  return new Date(timestamp).getTime() > 0;
};

export const formatDate = (dateString) => {
  if (!isValidTimestamp(dateString)) return "";

  const date = new Date(UTCToMontrealTime(dateString));

  const formattedDate = date.toLocaleDateString("fr-CA", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });

  const formattedTime = date.toLocaleTimeString("fr-FR", {
    hour: "2-digit",
    minute: "2-digit",
  });

  return `${formattedDate}, ${formattedTime}`;
};
