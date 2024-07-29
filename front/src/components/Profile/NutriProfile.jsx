import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import authenticatedRequest from "@/helpers/authenticatedRequest";
import getCurrentUser from "@/utils/users";
import DietProfile from "@/components/Profile/DietProfile";
import NutriPreferencesProfile from "@/components/Profile/NutriPreferencesProfile";
import AllergenProfile from "@/components/Profile/AllergenProfile";
import { useLocalStorage } from "@/hooks/useLocalStorage";
import { 
    DEFAULT_NUTRI_PROFILE, 
    NUTRI_NAME_CONVERTER_FR_TO_EN,
    ALLERGENS_LIST,
    NUTRI_PREFERENCES_LIST
} from "@/utils/nutriProfile";

const NutriProfile = () => {
    const [disableSubmit, setDisableSubmit] = useState(true);
    const [diets, setDiets] = useLocalStorage("diets", DEFAULT_NUTRI_PROFILE);
    const [nutriPreferences, setNutriPreferences] = useLocalStorage("nutriPreferences", NUTRI_PREFERENCES_LIST);
    const [selectedAllergens, setSelectedAllergens] = useLocalStorage("allergens", ALLERGENS_LIST.map(allergen => ({ name: allergen, value: null })));
    const userNutriPreferencesNames = nutriPreferences.map(nutri => nutri.name);
    const userAllergensNames = selectedAllergens.map(allergen => allergen.name);

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
                        toast.error("Accès interdit");
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
        setDisableSubmit(true);
        const selectedDiets = diets.map((diet) => ({
            name: diet.name,
            description: diet.description,
            forbidden_foods: diet.forbidden_foods,
            valid_cafes: diet.valid_cafes,
            checked: diet.checked,
            is_starter: diet.is_starter,
            desired_foods: diet.desired_foods
        }));
        const listAllergensSelected = selectedAllergens.filter((allergen) => allergen.value !== null);
        const listNutriPreferencesSelected = nutriPreferences.filter((nutriPreference) => nutriPreference.value !== null);

        const nutriPreferred = listNutriPreferencesSelected.reduce((acc, nutrient) => {
            const enName = NUTRI_NAME_CONVERTER_FR_TO_EN[nutrient.name];
            acc[enName] = nutrient.value;
            return acc;
        }, {});

        const allergens = listAllergensSelected.reduce((acc, allergen) => {
            acc[allergen.name] = allergen.value;
            return acc;
        }, {});

        const data = {
            diet_profile: {
                diets: selectedDiets,
                prefered_nutrients: nutriPreferred,
                allergens: allergens
            }
        }
        await updateUser(data);
    }

    useEffect(() => {
        handleSubmit();
    }, [diets, nutriPreferences, selectedAllergens]);

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
        </>
    );
};

export default NutriProfile;

