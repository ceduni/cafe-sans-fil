import CustomRadio from "@/components/Profile/CustomRadio";
import { useEffect } from "react";

const AllergenProfile = ({ selectedAllergens, setSelectedAllergens, setDisableSubmit, allergensNames }) => {
    return (
        <div className="border-b border-gray-900/10 pb-12 py-5">
            <h2 className="text-2xl font-semibold leading-7 text-gray-900">Allergènes</h2>
            <div className="grid grid-cols-2 gap-1 py-5">
                {selectedAllergens.map((allergen, index) => (
                    <div key={index} className="mb-2 flex items-center">
                        <label className="mr-2 text-gray-700 font-bold w-36">{allergen.name}</label>
                        <CustomRadio
                            name={allergen.name}
                            initElements={selectedAllergens}
                            setElements={setSelectedAllergens}
                            setDisableSubmit={setDisableSubmit}
                            initialColors={["bg-red-200", "bg-red-300", "bg-red-400"]}
                            onClickColors={["bg-red-700", "bg-red-700", "bg-red-700"]}
                            index={allergensNames.includes(allergen.name) ? allergen.value : null}
                        />
                    </div>
                ))}
            </div>
        </div>
    )
}

export default AllergenProfile;