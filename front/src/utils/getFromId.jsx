import authenticatedRequest from "@/helpers/authenticatedRequest";

export const getCafeFromId = async (cafeSlug) => {
  const response = await fetch(`${import.meta.env.VITE_API_ENDPOINT}/api/cafes/${cafeSlug}`);
  if (response.status !== 200) {
    return null;
  }
  const cafe = await response.json();
  return cafe;
};

export const getUserFromUsername = async (username) => {
  const response = await authenticatedRequest.get(`/users/${username}`);
  if (response.status !== 200) {
    return null;
  }
  const user = response.data;
  return user;
};
