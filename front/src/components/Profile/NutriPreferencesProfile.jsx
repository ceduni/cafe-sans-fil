import CustomRadio from "@/components/Profile/CustomRadio";
import { useState } from "react";

const NutriPreferences = ({ nutriPreferences, setNutriPreferences, setDisableSubmit }) => {

    const handleNutriPreferences = (index, event) => {
        const newNutriPreferences = nutriPreferences.slice();
        newNutriPreferences[index].value = event.target.value;
        setNutriPreferences(newNutriPreferences);
    };

    return (
        <div className="border-b border-gray-900/10 pb-12 py-5">
            <h2 className="text-2xl font-semibold leading-7 text-gray-900">Préférences nutritives</h2>
            <div className="grid grid-cols-2 gap-0 py-5">
                {nutriPreferences.map((nutriPreference, index) => (
                    <div key={index} className="mb-2 flex items-center">
                        <label 
                            className="mr-2 text-gray-700 font-bold w-32"
                        >{nutriPreference.name}</label>
                        <CustomRadio 
                            name={nutriPreference.name}
                            initElements={nutriPreferences}
                            setElements={setNutriPreferences}
                            setDisableSubmit={setDisableSubmit}
                        />
                    </div>
                ))}
            </div>
        </div>
    )
}

export default NutriPreferences;