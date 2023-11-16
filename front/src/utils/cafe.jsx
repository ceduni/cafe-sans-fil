export const displayCafeLocation = (location) => {
  if (!location) return "";
  const exceptions = ["Campus", "Faculté", "Cepsum"];
  const fullLocation = location.pavillon + ", local " + location.local;
  return exceptions.some((exception) => fullLocation.startsWith(exception)) ? fullLocation : `Pavillon ${fullLocation}`;
};

export const shouldDisplayInfo = (object) => {
  // Prend un objet de type
  // { "type": "string", "value": "string", "start": "string (YYYY-MM-DDTHH:mm:ss.ssssss)", "end": "string (YYYY-MM-DDTHH:mm:ss.ssssss)" }
  // et retourne true si l'objet est valide et qu'il est dans la période de validité.
  if (!object) return false;
  const now = new Date();
  const start = new Date(object.start);
  const end = new Date(object.end);
  return object.value && start < now && now < end;
};
