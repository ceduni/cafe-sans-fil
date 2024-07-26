import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import authenticatedRequest from "@/helpers/authenticatedRequest";
import getCurrentUser from "@/utils/users";
import DietProfile from "@/components/Profile/DietProfile";
import NutriPreferencesProfile from "@/components/Profile/NutriPreferencesProfile";
import AllergenProfile from "@/components/Profile/AllergenProfile";
import { 
    DEFAULT_NUTRI_PROFILE, 
    NUTRI_NAME_CONVERTER_FR_TO_EN,
    ALLERGENS_LIST,
    NUTRI_PREFERENCES_LIST,
    NUTRI_NAME_CONVERTER_EN_TO_FR
} from "@/utils/nutriProfile";

const NutriProfile = () => {
    const [disableSubmit, setDisableSubmit] = useState(true);

    const [diets, setDiets] = useState(DEFAULT_NUTRI_PROFILE);

    const [selectedAllergens, setSelectedAllergens] = useState(
        ALLERGENS_LIST.map(allergen => ({ name: allergen, value: null }))
    );

    const [userAllergensNames, setUserAllergensNames] = useState([]);
    const [userNutriPreferencesNames, setUserNutriPreferencesNames] = useState([]);

    const [nutriPreferences, setNutriPreferences] = useState(NUTRI_PREFERENCES_LIST);

    const updateUser = async (payload) => {
        const currentUser = await getCurrentUser();
        const toastId = toast.loading("Mise à jour du profil...");
        authenticatedRequest
            .put(`/users/${currentUser.username}`, payload)
            .then((response) => {
                toast.success("Profil mis à jour");
            })
            .catch((error) => {
                setDisableSubmit(false);
                switch (error.response?.status) {
                    case 404:
                        toast.error("Utilisateur introuvable");
                        break;

                    case 403:
                        toast.error("Accès interdit");
                        break;

                    default:
                        toast.error("Erreur lors de la mise à jour du profil");
                }
            })
            .finally(() => {
                toast.dismiss(toastId);
            });
    }

    const handleSubmit = async () => {
        setDisableSubmit(true)
        
        const slectedDiets = diets.map((diet) => {
            return {
                name: diet.name,
                description: diet.description,
                forbidden_foods: diet.forbiddenFoods,
                valid_cafes: diet.valid_cafes,
                checked: diet.checked
            };
        });
        const listAllergensSelected = selectedAllergens.filter((allergen) => allergen.value !== null);
        const listNutriPreferencesSelected = nutriPreferences.filter((nutriPreference) => nutriPreference.value !== null);
        
        const nutriPrefered = listNutriPreferencesSelected.reduce((acc, nutrient) => {
            const enName = NUTRI_NAME_CONVERTER_FR_TO_EN[nutrient.name];
            acc[enName] = nutrient.value
            return acc;
        }, {});
        
        const allergens = listAllergensSelected.reduce((acc, allergen) => {
            acc[allergen.name] = allergen.value
            return acc;
        }, {});
        
        const data = {
            diet_profile: {
                diets: slectedDiets,
                prefered_nutrients: nutriPrefered,
                allergens: allergens
            }
        }

        updateUser(data);
    }

    useEffect(() => {
        const setInitialValues = async () => {
            const currentUser = await getCurrentUser();
            if (currentUser.diet_profile?.diets?.length !== 0) {
                
                const currentDiets = currentUser.diet_profile.diets.map((diet) => {
                    if (['Méditéranéen','Végétarisme','Cétogène'].includes(diet.name)) {   
                        return { 
                            name: diet.name, 
                            checked: diet.checked, 
                            isStarter: true,
                            description: diet.description,
                            forbiddenFoods: diet.forbidden_foods,
                            valid_cafes: diet.valid_cafes
                        };
                    } else {
                        return { 
                            name: diet.name, 
                            checked: diet.checked, 
                            isStarter: false,
                            description: diet.description,
                            forbiddenFoods: diet.forbidden_foods,
                            valid_cafes: diet.valid_cafes
                        };
                    }
                });

                setDiets(currentDiets);
            }

            if (Object.keys(currentUser.diet_profile.prefered_nutrients).length !== 0) {
                const userPreferedNutrientsNames = Object.keys(currentUser.diet_profile.prefered_nutrients)
                                                            .map((key) => NUTRI_NAME_CONVERTER_EN_TO_FR[key]);
                setUserNutriPreferencesNames(userPreferedNutrientsNames);
                const userPreferedNutrientsValues = Object.values(currentUser.diet_profile.prefered_nutrients);

                const initPreferedNutrients = [...nutriPreferences]
                console.log(userPreferedNutrientsNames);
                for (let i = 0; i < userPreferedNutrientsNames.length; i++) {
                    const preferedNutrientIndex = initPreferedNutrients.findIndex((nutrient) => nutrient.name === userPreferedNutrientsNames[i]);
                    //console.log(initPreferedNutrients[preferedNutrientIndex]['value'])
                    initPreferedNutrients[preferedNutrientIndex]['value'] = userPreferedNutrientsValues[i];
                }
                
                setNutriPreferences(initPreferedNutrients);
                console.log(nutriPreferences);
            }

            if (Object.keys(currentUser.diet_profile.allergens).length !== 0) {
                const userAllergensNames = Object.keys(currentUser.diet_profile.allergens);
                setUserAllergensNames(userAllergensNames);
                const userAllergensValues = Object.values(currentUser.diet_profile.allergens);

                const initAllergens = [...selectedAllergens]

                for (let i = 0; i < userAllergensNames.length; i++) {
                    const allergenIndex = initAllergens.findIndex((allergen) => allergen.name === userAllergensNames[i]);
                    initAllergens[allergenIndex].value = userAllergensValues[i];
                }

                setSelectedAllergens(initAllergens);
            }
        }
        //const toastInit = toast.loading("Chargement du profile nutritif...");
        setInitialValues();
        //toast.dismiss(toastInit);
    }, []);

    return (
        <>
            <DietProfile 
                diets={diets}
                setDiets={setDiets}
                setDisableSubmit={setDisableSubmit}
            />

            <NutriPreferencesProfile 
                nutriPreferences={nutriPreferences}
                setNutriPreferences={setNutriPreferences}
                setDisableSubmit={setDisableSubmit}
                preferencesNames={userNutriPreferencesNames}
            />

            <AllergenProfile 
                selectedAllergens={selectedAllergens}
                setSelectedAllergens={setSelectedAllergens}
                setDisableSubmit={setDisableSubmit}
                allergensNames={userAllergensNames}
            />

            <div className="flex justify-end mt-4">
                <button 
                    className="bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-2 px-4 rounded mr-2 \
                    disabled:bg-gray-300 disabled:text-gray-500 disabled:shadow-none"
                    onClick={() => handleSubmit()}
                    disabled={ disableSubmit }
                >
                    Enregistrer 
                </button>
            </div>
        </>
    );
};

export default NutriProfile;
