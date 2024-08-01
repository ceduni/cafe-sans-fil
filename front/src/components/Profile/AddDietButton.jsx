import AddDietModal from "@/components/Profile/AddDietModal";
import { useState } from "react";

const AddDietCard = ({ diets, setDiets }) => {
    const [showModal, setShowModal] = useState(false);

    const handleAddDiet = () => {
        setShowModal(true);
    }

    return (
        <div className="py-20 px-40">
            <button
                className="w-32 h-32 border-2 border-gray-300 bg-emerald-600 hover:bg-emerald-500 rounded-full flex justify-center "
                onClick={handleAddDiet}
            >
                <h2 className="text-6xl text-white font-bold py-7">+</h2>
            </button>
            <AddDietModal
                isOpen={showModal}
                setIsOpen={setShowModal}
                diets={diets}
                setDiets={setDiets}
            />
        </div>
    )
}

export default AddDietCard;