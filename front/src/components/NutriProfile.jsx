import React, { useEffect, useState } from "react";
import toast from "react-hot-toast";
import authenticatedRequest from "@/helpers/authenticatedRequest";
import getCurrentUser from "@/utils/users";
import Diet from "@/components/Diet";

const NutriProfile = () => {
    const [activeTab, setActiveTab] = useState(0);
    const [disableSubmit, setDisableSubmit] = useState(true);
    const [openModalIndex, setOpenModalIndex] = useState(null);

    const [diets, setDiets] = useState([
        { text: 'Cétogène', checked: false, description: 'La diète cétogène, souvent utilisée dans un contexte de perte de poids, est un régime faible en glucides et élevé en gras.' },
        { text: 'Méditéranéen', checked: false, description: 'Riche en légumes, fruits, grains entiers, huile d’olive, légumineuses, noix, graines, poisson et fruits de mer, le régime méditerranéen fait place à la volaille, aux œufs et aux produits laitiers. Il est pauvre en viande rouge et en aliments sucrés.' },
        { text: 'Atkins', checked: false, description: 'Atkins' },
        { text: 'Zone', checked: false, description: 'Zone' },
        { text: 'Végétalisme', checked: false, description: 'Végétalisme' },
        { text: 'Weight watchers', checked: false, description: 'Weight watchers' },
        { text: 'Veganisme', checked: false, description: 'Veganisme' },
        { text: 'Crudivore', checked: false, description: 'Crudivore' },
        { text: 'Sans lactose', checked: false, description: 'Sans lactose' },
        { text: 'Sans gluten', checked: false, description: 'Sans gluten' },
    ]);

    // const [nutriPreferences, setNutriPreferences] = useState([
    //     { text: "Calories", value: 0 },
    //     { text: "Proteins", value: 0 },
    //     { text: "Carbohydrates", value: 0 },
    //     { text: "Lipids", value: 0 },
    //     { text: "Saturated fat", value: 0 },
    //     { text: "Sodium", value: 0 },
    //     { text: "Sugar", value: 0 },
    //     { text: "Fiber", value: 0 },
    //     { text: "VItamins", value: 0 },
    //     { text: "Fruit-légumes-Noix", value: 0 },
    // ]);

    const [categories, setCategories] = useState([
        { text: "Grilled Cheese", checked: false },
        { text: "Boisson chaude", checked: false },
        { text: "Boisson froide", checked: false },
        { text: "Collation", checked: false },
    ]);

    const allergensList = [
        'Lait', 'Oeuf', 'Poisson', 'Crustacés', 'Noix', 'Cacahuètes', 'Blé', 
        'Soja', 'Sesame', 'Moutarde', 'Celery', 'Lupin', 'Sulfites',
    ];

    const [selectedAllergens, setSelectedAllergens] = useState(
        allergensList.map(allergen => ({ text: allergen, checked: false }))
    );

    const handleOpenModal = (index) => {
        setOpenModalIndex(index);
    };

    const handleCloseModal = () => {
        setOpenModalIndex(null);
    };

    const handleTabChange = (index) => {
        setActiveTab(index);
    };

    const handleDietsCheckboxChange = (index) => {
        const newLabels = diets.slice();
        newLabels[index].checked = !newLabels[index].checked;
        setDiets(newLabels);
        setDisableSubmit(false);
    };

    const handleCategeriesCheckboxChange = (index) => {
        const newCategeries = categories.slice();
        newCategeries[index].checked = !newCategeries[index].checked;
        setCategories(newCategeries);
        setDisableSubmit(false);
    };

    const handleAllergensCheckboxChange = (index) => {
        const newSelectedAllergens = selectedAllergens.slice();
        newSelectedAllergens[index].checked = !newSelectedAllergens[index].checked;
        setSelectedAllergens(newSelectedAllergens);
        setDisableSubmit(false);
    };

    // const handleNutriPreferences = (index, event) => {
    //     const newNutriPreferences = nutriPreferences.slice();
    //     newNutriPreferences[index].value = event.target.value;
    //     setNutriPreferences(newNutriPreferences);
    // };

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
        const slectedDiets = diets.filter((diet) => diet.checked).map((diet) => diet.text);
        const selectedCategories = categories.filter((category) => category.checked).map((category) => category.text);
        const listAllergensSelected = selectedAllergens.filter((allergen) => allergen.checked).map((allergen) => allergen.text);
        const allergens = listAllergensSelected.reduce((acc, key, index) => {
            acc[key] = 0;
            return acc;
        }, {});
        
        const data = {
            diet_profile: {
                diets: slectedDiets,
                food_categories: selectedCategories,
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
                const currentDiet = diets.map((diet) => ( currentUser.diet_profile.diets.includes(diet.text) ? { text: diet.text, checked: true, description: diet.description } : diet ));
                setDiets(currentDiet);
            }

            if (currentUser.diet_profile.food_categories.length !== 0) {
                const currentCategories = categories.map((category) => ( currentUser.diet_profile.food_categories.includes(category.text) ? { text: category.text, checked: true } : category ));
                setCategories(currentCategories);
            }

            if (Object.keys(currentUser.diet_profile.allergens).length !== 0) {
                const currentAllergens = allergensList.map((allergen) => ( Object.keys(currentUser.diet_profile.allergens).includes(allergen) ? { text: allergen, checked: true } : { text: allergen, checked: false } ));
                setSelectedAllergens(currentAllergens);
            }
        }
        
        setInitialValues();
    }, []);

    return (
        <div className="w-full p-4">
        <div className="flex border-b border-gray-200 mb-4">
            <button
            className={`py-2 px-4 ${activeTab === 0 ? 'border-b-2 border-blue-500' : ''}`}
            onClick={() => handleTabChange(0)}
            >
            Régimes alimentaire
            </button>

            {/* <button
            className={`py-2 px-4 ${activeTab === 1 ? 'border-b-2 border-blue-500' : ''}`}
            onClick={() => handleTabChange(1)}
            >
            Préférences nutritives
            </button> */}

            <button
            className={`py-2 px-4 ${activeTab === 2 ? 'border-b-2 border-blue-500' : ''}`}
            onClick={() => handleTabChange(2)}
            >
                Catégories
            </button>

            <button
            className={`py-2 px-4 ${activeTab === 3 ? 'border-b-2 border-blue-500' : ''}`}
            onClick={() => handleTabChange(3)}
            >
                Allergènes
            </button>

            {/* <button
            className={`py-2 px-4 ${activeTab === 4 ? 'border-b-2 border-blue-500' : ''}`}
            onClick={() => handleTabChange(4)}
            >
                Objectifs
            </button> */}

            {/* <button
            className={`py-2 px-4 ${activeTab === 4 ? 'border-b-2 border-blue-500' : ''}`}
            onClick={() => handleTabChange(4)}
            >
                Recommendations
            </button> */}
        </div>

        {activeTab === 0 && (
            <div className="grid grid-cols-2 gap-1">
            {diets.map((diet, index) => (
                <Diet
                key={index}
                index={index}
                openModalIndex={openModalIndex}
                handleOpenModal={handleOpenModal}
                handleCloseModal={handleCloseModal}
                handleDietsCheckboxChange={handleDietsCheckboxChange}
                name={diet.text}
                description={diet.description}
                checked={diet.checked}
                />
            ))}
            </div>
        )}

        {/* {activeTab === 1 && (
            <div className="grid grid-cols-2 gap-0">
                {nutriPreferences.map((nutriPreference, index) => (
                    <div key={index} className="mb-2 flex items-center">
                        <label 
                        className="mr-2 text-gray-700 font-bold w-32">{nutriPreference.text}</label>
                        <input
                        className='border border-gray-300 rounded w-16 h-8'
                        value={nutriPreference.value}
                        onChange={(event) => handleNutriPreferences(index, event)}
                        />
                        <div className='ml-2'>
                            {nutriPreference.text !== "Calories" && "g"}
                        </div>
                    </div>
                ))}
            </div>
        )} */}

        {activeTab === 2 && (
            <div>
                {categories.map((category, index) => (
                    <div key={index} className="mb-2 flex items-center">
                    <label className="mr-2 text-gray-700 font-bold w-36 ">{category.text}</label>
                    <input
                        type="checkbox"
                        checked={category.checked}
                        onChange={() => handleCategeriesCheckboxChange(index)}
                        className="mr-2 align-middle"
                    />
                    </div>
                ))}
            </div>
        )}

        {activeTab === 3 && (
            <div className="grid grid-cols-2 gap-1">
                {selectedAllergens.map((allergen, index) => (
                <div key={index} className="mb-2 flex items-center">
                    <label className="mr-2 text-gray-700 font-bold w-36">{allergen.text}</label>
                    <input
                        type="checkbox"
                        checked={allergen.checked}
                        onChange={() => handleAllergensCheckboxChange(index)}
                        className="mr-2"
                    />
                </div>
                ))}
            </div>
        )}

        {/* activeTab === 4 && <div></div> */}

        {/* activeTab === 5 && <div></div> */}

        <div className="flex justify-end mt-4">
            <button 
            className="bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-2 px-4 rounded mr-2 \
            disabled:bg-gray-300 disabled:text-gray-500 disabled:shadow-none"
            onClick={() => handleSubmit()}
            disabled={ disableSubmit
                // !( diets.some((diet) => diet.checked) ||
                // selectedAllergens.some((allergen) => allergen.checked) || 
                // categories.some((category) => category.checked) )
            }
            >
            Enregistrer 
            </button>
        </div>
        </div>
    );
};

export default NutriProfile;
