export const getCafeFromId = async (cafeId) => {
  const response = await fetch(`${import.meta.env.VITE_API_ENDPOINT}/api/cafes/${cafeId}`);
  const cafe = await response.json();
  return cafe;
};

export const getItemFromId = async (itemId, cafeId) => {
  const response = await fetch(`${import.meta.env.VITE_API_ENDPOINT}/api/cafes/${cafeId}/menu/${itemId}`);
  const item = await response.json();
  return item;
};
