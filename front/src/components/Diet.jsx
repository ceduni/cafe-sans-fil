
const Diet = ({ index, handleDietsCheckboxChange, onDeleteDiet, name, description, checked, isStarter }) => {
    return (
        <div className="w-full max-w-md p-4 border-2 border-gray-300 bg-gray-100 rounded-md flex flex-col justify-between h-full">
            <div>
                <div className="flex justify-between items-center mb-2">
                    <h2 className="text-xl font-bold">{name}</h2>
                    <input
                        type="checkbox"
                        checked={checked}
                        onChange={() => handleDietsCheckboxChange(index)}
                        className="mr-2 align-middle rounded-full w-6 h-6"
                    />
                </div>
                <div>
                    <div>
                        <h3 className="text-md font-bold">Description</h3>
                        <p className="text-md text-gray-700">{description}</p>
                    </div>
                    <div className="py-2">
                        <h3 className="text-md font-bold">Liste des aliments non désirés</h3>
                        <p className="text-md text-gray-700">Poisson, viande</p>
                    </div>
                    <div>
                        <h3 className="text-md font-bold">Cafés</h3>
                        <p className="text-md text-gray-700">5 cafés vendent vendent des items respectant ces contraintes.</p>
                    </div>
                </div>
            </div>
            {!isStarter && <div className="flex justify-end mt-4">
                <button 
                className="bg-red-600 hover:bg-red-500 text-white font-bold py-2 px-4 rounded"
                onClick={() => onDeleteDiet(index)}
                >
                    supprimer
                </button>
            </div>}
        </div>
    );
};

export default Diet;