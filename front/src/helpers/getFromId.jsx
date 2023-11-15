export const getCafeFromId = async (cafeId) => {
  const response = await fetch(`${import.meta.env.VITE_API_ENDPOINT}/api/cafes/${cafeId}`);
  if (response.status !== 200) {
    return null;
  }
  const cafe = await response.json();
  return cafe;
};

export const getItemFromId = async (itemId, cafeId) => {
  const response = await fetch(`${import.meta.env.VITE_API_ENDPOINT}/api/cafes/${cafeId}/menu/${itemId}`);
  if (response.status !== 200) {
    return null;
  }
  const item = await response.json();
  return item;
};
