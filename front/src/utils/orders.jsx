export const ORDER_STATUS = {
  PLACED: "Placée",
  READY: "Prête",
  COMPLETED: "Complétée",
  CANCELED: "Annulée",
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
