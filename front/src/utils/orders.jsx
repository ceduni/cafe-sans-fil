const isValidDate = (date) => {
  return date instanceof Date && !isNaN(date);
};

export const formatDate = (date) => {
  if (!isValidDate(date)) return "";
  return new Intl.DateTimeFormat("fr-FR", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(date));
};
