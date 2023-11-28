export const ORDER_STATUS = {
  PLACED: "Placée",
  READY: "Prête",
  COMPLETED: "Complétée",
  CANCELED: "Annulée",
};

export const formatDate = (dateString) => {
  if (!isValidTimestamp(dateString)) return "";

  const date = new Date(dateString);

  const isDST = (date) => {
    const jan = new Date(date.getFullYear(), 0, 1).getTimezoneOffset();
    const jul = new Date(date.getFullYear(), 6, 1).getTimezoneOffset();
    return Math.max(jan, jul) !== date.getTimezoneOffset();
  };

  const offset = isDST(date) ? -4 : -5;
  date.setHours(date.getHours() + offset);

  const formattedDate = date.toLocaleDateString('fr-CA', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });

  const formattedTime = date.toLocaleTimeString('en-CA', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: true,
  });

  return `${formattedDate}, ${formattedTime}`;
};

const isValidTimestamp = (timestamp) => {
  return new Date(timestamp).getTime() > 0;
};

export const isOldOrder = (status) => {
  return status === ORDER_STATUS.CANCELED || status === ORDER_STATUS.COMPLETED;
};

export const isPendingOrder = (status) => {
  return status === ORDER_STATUS.PLACED;
};

export const getBadgeVariant = (status) => {
  switch (status) {
    case ORDER_STATUS.PLACED:
      return "warning";
    case ORDER_STATUS.READY:
      return "success";
    case ORDER_STATUS.COMPLETED:
      return "neutral";
    case ORDER_STATUS.CANCELED:
      return "danger";
  }
};
