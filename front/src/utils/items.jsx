export const IN_STOCK_TEXT = "En stock";
export const OUT_OF_STOCK_TEXT = "Épuisé";

// On récupère les catégories de produits proposées par le café, sans doublons
export const getCafeCategories = (menuItems) => {
  return [...new Set(menuItems?.map((product) => product.category || "Autres"))];
};

// On récupère les produits d'une catégorie donnée
export const getItemByCategory = (menuItems, category) => {
  return menuItems.filter((product) => {
    if (category === "Autres") {
      return !product.category;
    } else {
      return product.category === category;
    }
  });
};
