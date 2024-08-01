import getCurrentUser from "@/utils/users";
import { useEffect, useState } from "react";
import EditDietModal from "@/components/Profile/EditDietModal";


const Diet = ({ index, handleDietsCheckboxChange, onDeleteDiet, name, description, checked, isStarter, forbidden_foods, diets, setDiets, desired_foods }) => {
    const [numberValidCafes, setNumberValidCafes] = useState(0);
    const [showEditModal, setShowEditModal] = useState(false);
    const diet = { name, description, forbidden_foods, valid_cafes: numberValidCafes, checked, isStarter, desired_foods };
    const getNumberValidCafes = async () => {
        const currentUser = await getCurrentUser();
        const diet = currentUser?.diet_profile?.diets.filter((diet) => diet.name === name)[0];
        if (diet) {
            return diet?.valid_cafes?.length;
        }
    }

    const handleDietClick = () => {
        setShowEditModal(true);
    }

    useEffect(() => {
        getNumberValidCafes().then((number) => setNumberValidCafes(number));
    }, []);

    return (
        <>
            <button 
                className="w-full max-w-lg p-4 border-2 flex-col justify-start hover:border-gray-400 hover:shadow-md border-gray-300 bg-gray-100 rounded-md"
                onClick={handleDietClick}
            >
                <div>
                    <div className="flex justify-between items-center mb-2">
                        <h2 className="text-xl font-bold">{name}</h2>
                        <input
                            type="checkbox"
                            checked={checked}
                            onClick={(e) => e.stopPropagation()}
                            onChange={() => handleDietsCheckboxChange(index)}
                            className="mr-2 align-middle rounded-full w-6 h-6"
                        />
                    </div>
                    <div className="text-left">
                        <div>
                            <h3 className="text-md font-bold">Description</h3>
                            <p className="text-md text-gray-700">{description}</p>
                        </div>
                        <div className="py-2">
                            <h3 className="text-md font-bold">Liste des aliments non désirés</h3>
                            <p className="text-md text-gray-700">{forbidden_foods.length > 0 ? forbidden_foods.join(", ") : "Aucun aliment spécifié"}</p>
                        </div>
                        <div className="py-2">
                            <h3 className="text-md font-bold">Liste des aliments désirés</h3>
                            <p className="text-md text-gray-700">{desired_foods.length > 0 ? desired_foods.join(", ") : "Aucun aliment spécifié"}</p>
                        </div>
                        <div>
                            <h3 className="text-md font-bold py-2">Cafés: {numberValidCafes}</h3>
                        </div>
                    </div>
                </div>
                {!isStarter && <div className="flex justify-end mt-4">
                    <button 
                    className="bg-red-600 hover:bg-red-500 text-white font-bold py-2 px-4 rounded"
                    onClick={(e) => { 
                        e.stopPropagation(); 
                        onDeleteDiet(index);
                    }}
                    >
                        Supprimer
                    </button>
                </div>}
            </button>
        <>
            {showEditModal && !isStarter && <EditDietModal isOpen={showEditModal} setIsOpen={setShowEditModal} diets={diets} diet={diet} setDiets={setDiets} />}
        </>
        </>
    );
};

export default Diet;
