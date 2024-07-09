import useApi from '@/hooks/useApi';
import React, { useState } from 'react';

const NutriProfile = () => {
    const [activeTab, setActiveTab] = useState(1);

    const [diets, setDiets] = useState([
        { text: 'Cétogène', checked: false },
        { text: 'Méditéranéen', checked: false },
        { text: 'Atkins', checked: false },
        { text: 'Zone', checked: false },
        { text: 'Végétalisme', checked: false },
        { text: 'Weight watchers', checked: false },
        { text: 'Veganisme', checked: false },
        { text: 'Crudivore', checked: false },
        { text: 'Sans lactose', checked: false },
        { text: 'Sans gluten', checked: false },
    ]);

    const [nutriPreferences, setNutriPreferences] = useState([
        { text: "Calories", value: 0 },
        { text: "Proteins", value: 0 },
        { text: "Carbohydrates", value: 0 },
        { text: "Lipids", value: 0 },
        { text: "Saturated fat", value: 0 },
        { text: "Sodium", value: 0 },
        { text: "Sugar", value: 0 },
        { text: "Fiber", value: 0 },
        { text: "VItamins", value: 0 },
        { text: "Fruit-légumes-Noix", value: 0 },
    ]);

    const [categeries, setCategories] = useState([
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

    const handleTabChange = (index) => {
        setActiveTab(index);
    };

    const handleDietsCheckboxChange = (index) => {
        const newLabels = diets.slice();
        newLabels[index].checked = !newLabels[index].checked;
        setDiets(newLabels);
    };

    const handleCategeriesCheckboxChange = (index) => {
        const newCategeries = categeries.slice();
        newCategeries[index].checked = !newCategeries[index].checked;
        setCategories(newCategeries);
    };

    const handleAllergensCheckboxChange = (index) => {
        const newSelectedAllergens = selectedAllergens.slice();
        newSelectedAllergens[index].checked = !newSelectedAllergens[index].checked;
        setSelectedAllergens(newSelectedAllergens);
    };

    const handleNutriPreferences = (index, event) => {
        const newNutriPreferences = nutriPreferences.slice();
        newNutriPreferences[index].value = event.target.value;
        setNutriPreferences(newNutriPreferences);
    };

    const handleValidate = () => {

        alert("Informations sauvegardées");
    };

    return (
        <div className="w-full p-4">
        <div className="flex border-b border-gray-200 mb-4">
            <button
            className={`py-2 px-4 ${activeTab === 0 ? 'border-b-2 border-blue-500' : ''}`}
            onClick={() => handleTabChange(0)}
            >
            Régimes alimentaire
            </button>

            <button
            className={`py-2 px-4 ${activeTab === 1 ? 'border-b-2 border-blue-500' : ''}`}
            onClick={() => handleTabChange(1)}
            >
            Préférences nutritives
            </button>

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
                <div key={index} className="mb-2 flex items-center">
                <label className="mr-2 text-gray-700 font-bold w-36 ">{diet.text}</label>
                <input
                    type="checkbox"
                    checked={diet.checked}
                    onChange={() => handleDietsCheckboxChange(index)}
                    className="mr-2 align-middle"
                />
                </div>
            ))}
            </div>
        )}

        {activeTab === 1 && (
            <div className="grid grid-cols-2 gap-0">
                {nutriPreferences.map((nutriPreference, index) => (
                    <div key={index} className="mb-2 flex items-center">
                        <label className="mr-2 text-gray-700 font-bold w-32">{nutriPreference.text}</label>
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
        )}

        {activeTab === 2 && (
            <div>
                {categeries.map((category, index) => (
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
            className="bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-2 px-4 rounded mr-2"
            onClick={() => hanfleSubmit()}
            >
            Valider
            </button>
        </div>
        </div>
    );
};

export default NutriProfile;
