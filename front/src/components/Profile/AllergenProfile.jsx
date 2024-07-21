import CustomRadio from "@/components/Profile/CustomRadio";

const AllergenProfile = ({ selectedAllergens, setSelectedAllergens, setDisableSubmit }) => {

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
                        />
                    </div>
                ))}
            </div>
        </div>
    )
}

export default AllergenProfile;