const isValidTimestamp = (timestamp) => {
  return new Date(timestamp).getTime() > 0;
};

export const formatDate = (date) => {
  if (!isValidTimestamp(date)) return "";
  return new Intl.DateTimeFormat("fr-FR", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(date));
};
