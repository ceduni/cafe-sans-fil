export const getUserRole = (cafe, username) => {
  if (!cafe) return null;
  return cafe.staff.find((member) => member.username === username)?.role;
};

export const ROLES = {
  ADMIN: "Admin",
  MEMBER: "Bénévole",
};

export const isAdmin = (cafe, username) => {
  if (!cafe || !username) return false;
  return getUserRole(cafe, username) === ROLES.ADMIN;
};

export const isMember = (cafe, username) => {
  if (!cafe || !username) return false;
  return getUserRole(cafe, username) === ROLES.MEMBER;
};
