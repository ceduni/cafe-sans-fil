export const formatPrice = (price) => {
  return parseFloat(price).toFixed(2);
};

export const areItemsFromMoreThanOneCafe = (items) => {
  const cafeNames = [...new Set(items.map((item) => item.cafe?.name))];
  return cafeNames.length > 1;
};
export const displayCafeNames = (items) => {
  const cafeNames = [...new Set(items.map((item) => item.cafe?.name))];
  if (cafeNames.length > 1) {
    return `${cafeNames.slice(0, -1).join(", ")} et ${cafeNames.slice(-1)}`;
  } else {
    return cafeNames[0];
  }
};
