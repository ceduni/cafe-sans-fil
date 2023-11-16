export const displayCafeLocation = (location) => {
  if (!location) return "";
  const fullLocation = location.pavillon + ", " + location.local;
  return fullLocation;
};

export const shouldDisplayInfo = (object) => {
  // Prend un objet de type
  // { "type": "string", "value": "string", "start": "string (YYYY-MM-DDTHH:mm:ss.ssssss)", "end": "string (YYYY-MM-DDTHH:mm:ss.ssssss)" }
  // et retourne true si on est dans la période de validité.
  if (!object) return false;
  // Si start ou end n'existent pas, on retourne true
  if (!object.start || !object.end) return true;
  const now = new Date();
  const start = new Date(object.start);
  const end = new Date(object.end);
  return object.value && start < now && now < end;
};

export const isNowWithinOpeningHours = (openingHours) => {
  // Prend un objet de type
  // [{ "day": "string", "blocks": [{"start": "string (HH:mm format)", "end": "string (HH:mm format)" }] }]
  // et retourne true si on est dans les horaires d'ouverture.
  if (!openingHours) return false;
  const now = new Date();
  const today = now.toLocaleString("fr-CA", { weekday: "long" });
  const hours = now.getHours();
  const minutes = now.getMinutes();
  const time = hours + ":" + minutes;
  // On cherche le jour actuel dans les horaires d'ouverture
  const currentDay = openingHours.find((day) => day.day.toLowerCase() === today.toLowerCase());
  if (!currentDay) return false;
  // On cherche le bloc horaire actuel dans les horaires d'ouverture
  const currentBlock = currentDay.blocks.find((block) => block.start <= time && time <= block.end);
  // Si on trouve un bloc horaire, on retourne true
  return currentBlock ? true : false;
};
