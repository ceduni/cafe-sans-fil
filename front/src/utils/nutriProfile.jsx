export const DEFAULT_NUTRI_PROFILE = [
    {
        name: 'Méditéranéen', 
        description: 'Riche en légumes, fruits, grains entiers, huile d’olive, légumineuses, noix, graines, poisson et fruits de mer, le régime méditerranéen fait place à la volaille, aux œufs et aux produits laitiers. Il est pauvre en viande rouge et en aliments sucrés.',
        forbiddenFoods: ['Sucre', 'Viande rouge'],
        checked: false, 
        isStarter: true,
        visited_cafes: [],
    },
  
    {
        name: 'Végétarisme', 
        description: 'Le végétarisme est une pratique alimentaire qui exclut la consommation de chair animale. Elle est associée à la cuisine végétarienne.',
        forbiddenFoods: ['Viande', 'Poisson', 'Fruits de mer'],
        checked: false, 
        isStarter: true, 
        visited_cafes: [],
    },
  
    {
        name: 'Cétogène', 
        description: 'La diète cétogène, souvent utilisée dans un contexte de perte de poids, est un régime faible en glucides et élevé en gras.',
        forbiddenFoods: ['Sucre', 'Légume', 'Alcool'], 
        checked: false, 
        isStarter: true, 
        visited_cafes: [], 
    },
];

export const ALLERGENS_LIST = [
    'Lactose', 'Oeuf', 'Poisson', 'Crustacés', 'Cacahuètes', 'Soja', 'Sésame', 'Moutarde', 'Celery',
];

export const NUTRI_PREFERENCES_LIST = [
    { name: "Calories", value: null },
    { name: "Protéines", value: null },
    { name: "Glucides", value: null },
    { name: "Lipides", value: null },
    { name: "Gras saturés", value: null },
    { name: "Sodium", value: null },
    { name: "Sucre", value: null },
    { name: "Fibres", value: null },
    { name: "zinc", value: null },
    { name: "Fer", value: null },
    { name: "Calcium", value: null },
    { name: "Magnésium", value: null },
    { name: "Potassium", value: null },
    { name: "Vitamine A", value: null },
    { name: "Vitamine C", value: null },
    { name: "Vitamine D", value: null },
    { name: "Vitamine E", value: null },
    { name: "Vitamine K", value: null },
    { name: "Vitamine B6", value: null },
    { name: "Vitamine B12", value: null },

];

export const NUTRI_NAME_CONVERTER_FR_TO_EN = {
    "Zinc": "zinc",
    "Fer": "Iron",
    "Calcium": "Calcium",
    "Magnésium": "Magnesium",
    "Potassium": "Potassium",
    "Vitamine A": "VitaminA",
    "Vitamine C": "VitaminC",
    "Vitamine D": "VitaminD",
    "Vitamine E": "VitaminE",
    "Vitamine K": "VitaminK",
    "Vitamine B6": "VitaminB6",
    "Vitamine B12": "VitaminB12",   
    "Calories": "calories",   
    "Lipides": "lipid",   
    "Protéines": "protein",   
    "Glucides": "carbohydrates",   
    "Sucre": "sugar",   
    "Sodium": "sodium",   
    "Fibres": "fiber",   
    "Gras saturés": "saturated_fat",
};
 
export const NUTRI_NAME_CONVERTER_EN_TO_FR = {
    "zinc": "Zinc",
    "iron": "Fer",
    "calcium": "Calcium",
    "magnesium": "Magnésium",
    "potassium": "Potassium",
    "vitaminA": "Vitamine A",
    "vitaminC": "Vitamine C",
    "vitaminD": "Vitamine D",
    "vitaminE": "Vitamine E",
    "vitaminK": "Vitamine K",
    "vitaminB6": "Vitamine B6",
    "vitaminB12": "Vitamine B12",
    "calories": "Calories",
    "lipid": "Lipides",
    "protein": "Protéines",
    "carbohydrates": "Glucides",
    "sugar": "Sucre",
    "sodium": "Sodium",
    "fiber": "Fibres",
    "vitamins": "Vitamines",
    "saturated_fat": "Gras saturés",
};
