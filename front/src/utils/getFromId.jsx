export const getCafeFromId = async (cafeSlug) => {
  const response = await fetch(`${import.meta.env.VITE_API_ENDPOINT}/api/cafes/${cafeSlug}`);
  if (response.status !== 200) {
    return null;
  }
  const cafe = await response.json();
  return cafe;
};

export const getItemFromId = async (itemSlug, cafeSlug) => {
  const response = await fetch(`${import.meta.env.VITE_API_ENDPOINT}/api/cafes/${cafeSlug}/menu/${itemSlug}`);
  if (response.status !== 200) {
    return null;
  }
  const item = await response.json();
  return item;
};
