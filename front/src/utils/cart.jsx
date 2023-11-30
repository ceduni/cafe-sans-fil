export const formatPrice = (price) => {
  return new Intl.NumberFormat("fr-CA", {
    style: "currency",
    currency: "CAD",
  }).format(price);
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

const capitalizeFirstLetter = (string) => {
  return string.charAt(0).toUpperCase() + string.slice(1);
};

export const DEFAULT_OPTION_NAME = "Régulier";

export const displayOptions = (selectedOptions) => {
  if (!selectedOptions) return "";
  const options = [];
  Object.entries(selectedOptions).forEach(([type, obj]) => {
    const { value } = obj;
    if (value === DEFAULT_OPTION_NAME) return;
    options.push(`${capitalizeFirstLetter(value)}`);
  });
  return options.length === 0 ? "" : options.join(", ");
};
const isAdditionalOptionSelected = (selectedOptions) => {
  return Object.entries(selectedOptions).some(([type, obj]) => {
    const { value } = obj;
    return value !== DEFAULT_OPTION_NAME;
  });
};
export const getIdFromSelectedOptions = (selectedOptions) => {
  if (!selectedOptions || !isAdditionalOptionSelected(selectedOptions)) return "";
  return (
    "+" +
    Object.entries(selectedOptions)
      .map(([type, obj]) => {
        const { value } = obj;
        return `${type}:${value}`;
      })
      .join("+")
      .replace(/é/g, "e")
      .toLowerCase()
  );
};

export const getAdditionalPriceFromOptions = (options) => {
  let additionalPrice = 0;
  options.forEach((option) => {
    additionalPrice += parseFloat(option.fee);
  });
  return additionalPrice;
};

export const arrayToOptionsByType = (options) => {
  // On prend un tableau d'options de l'API et on le transforme en objet d'options par type
  // ex input: [{type: "sirop", value: "vanille", fee: "0.50"}, {type: "sirop", value: "caramel", fee: "0.50"}]
  // ex output: {sirop: [{type: "sirop", value: "vanille", fee: "0.50"}, {type: "sirop", value: "caramel", fee: "0.50"}]}
  // On ajout une option "Régulier" pour chaque type
  const optionsByType = {};
  options.forEach((option) => {
    if (!optionsByType[option.type]) {
      optionsByType[option.type] = [];
    }
    optionsByType[option.type].push(option);
  });

  // On ajoute une option "Régulier" pour chaque type
  Object.keys(optionsByType).forEach((type) => {
    optionsByType[type].unshift({
      type: type,
      value: DEFAULT_OPTION_NAME,
      fee: "0",
    });
  });

  return optionsByType;
};

export const optionsByTypeToArray = (optionsByType) => {
  // On prend un objet d'options par type et on le transforme en tableau d'options comme dans l'API
  // Si l'option est "Régulier", on ne l'ajoute pas
  const options = [];
  Object.entries(optionsByType).forEach(([type, obj]) => {
    const { value } = obj;
    if (value === DEFAULT_OPTION_NAME) return;
    options.push({
      fee: obj.fee,
      type: type,
      value: value,
    });
  });
  return options;
};
