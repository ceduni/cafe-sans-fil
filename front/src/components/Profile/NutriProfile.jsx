import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import authenticatedRequest from "@/helpers/authenticatedRequest";
import getCurrentUser from "@/utils/users";
import DietProfile from "@/components/Profile/DietProfile";
import NutriPreferencesProfile from "@/components/Profile/NutriPreferencesProfile";
import AllergenProfile from "@/components/Profile/AllergenProfile";
import { all } from "axios";

const NutriProfile = () => {
    const [disableSubmit, setDisableSubmit] = useState(true);

    const [diets, setDiets] = useState(
        localStorage.getItem("updatedDiets") ? JSON.parse(localStorage.getItem("updatedDiets")) :
        [ 
            { name: 'Méditéranéen', checked: false, isStarter: true, description: 'Riche en légumes, fruits, grains entiers, huile d’olive, légumineuses, noix, graines, poisson et fruits de mer, le régime méditerranéen fait place à la volaille, aux œufs et aux produits laitiers. Il est pauvre en viande rouge et en aliments sucrés.' },
            { name: 'Végétarisme', checked: false, isStarter: true, description: 'Le végétarisme est une pratique alimentaire qui exclut la consommation de chair animale. Elle est associée à la cuisine végétarienne.' },
            { name: 'Cétogène', checked: false, isStarter: true, description: 'La diète cétogène, souvent utilisée dans un contexte de perte de poids, est un régime faible en glucides et élevé en gras.' },
        ]
    );

    const allergensList = [
        'Lactose', 'Oeuf', 'Poisson', 'Crustacés', 'Cacahuètes', 'gluten', 
        'Soja', 'Sésame', 'Moutarde', 'Celery', 'Lupin', 'Sulfites',
    ];

    const [selectedAllergens, setSelectedAllergens] = useState(
        allergensList.map(allergen => ({ name: allergen, value: null }))
    );

    const [nutriPreferences, setNutriPreferences] = useState([
        { name: "Calories", value: 0 },
        { name: "Proteins", value: 0 },
        { name: "Carbohydrates", value: 0 },
        { name: "Lipids", value: 0 },
        { name: "Saturated fat", value: 0 },
        { name: "Sodium", value: 0 },
        { name: "Sugar", value: 0 },
        { name: "Fiber", value: 0 },
        { name: "VItamins", value: 0 },
        { name: "Fruit-légumes-Noix", value: 0 },
    ]);

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
        const slectedDiets = diets.filter((diet) => diet.checked).map((diet) => diet.name);
        const listAllergensSelected = selectedAllergens.filter((allergen) => allergen.value !== null);
        const allergens = listAllergensSelected.reduce((acc, allergen) => {
            acc[allergen.name] = allergen.value
            return acc;
        }, {});
        
        const data = {
            diet_profile: {
                diets: slectedDiets,
                prefered_nutrients: [],
                allergens: allergens
            }
        }
        updateUser(data);
    }

    useEffect(() => {
        const setInitialValues = async () => {
            const currentUser = await getCurrentUser();

            if (currentUser.diet_profile.diets.length !== 0) {
                const currentDiet = diets.map((diet) => ( currentUser.diet_profile.diets.includes(diet.name) ? { name: diet.name, checked: true, description: diet.description } : diet ));
                setDiets(currentDiet);
            }

            if (Object.keys(currentUser.diet_profile.prefered_nutrients).length !== 0) {
                const currentPreferedNutrients = nutriPreferences.map((nutrient) => ( Object.keys(currentUser.diet_profile.prefered_nutrients).includes(nutrient.name) ? { name: nutrient.name, checked: true } : { name: nutrient.name, checked: false } ));
                setNutriPreferences(currentPreferedNutrients);
            }

            if (Object.keys(currentUser.diet_profile.allergens).length !== 0) {
                const currentAllergens = allergensList.map((allergen) => ( Object.keys(currentUser.diet_profile.allergens).includes(allergen) ? { name: allergen, checked: true } : { name: allergen, checked: false } ));
                setSelectedAllergens(currentAllergens);
            }
        }
        
        setInitialValues();
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
            />

            <AllergenProfile 
                selectedAllergens={selectedAllergens}
                setSelectedAllergens={setSelectedAllergens}
                setDisableSubmit={setDisableSubmit}
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
