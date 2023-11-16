export const displayCafeLocation = (location) => {
  if (!location) return "";
  const exceptions = ["Campus", "Faculté", "Cepsum"];
  const fullLocation = location.pavillon + ", local " + location.local;
  return exceptions.some((exception) => fullLocation.startsWith(exception)) ? fullLocation : `Pavillon ${fullLocation}`;
};
