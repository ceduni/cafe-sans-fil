import Diet from "@/components/Profile/Diet";
import AddDietCard from "@/components/Profile/AddDietCard";


const DietProfile = ({ diets, setDiets, setDisableSubmit }) => {
    const handleDietsCheckboxChange = (index) => {
        const newLabels = diets.slice();
        newLabels[index].checked = !newLabels[index].checked;
        setDiets(newLabels);
        setDisableSubmit(false);
    };

    const onDeleteDiet = (index) => {
        const newDiets = diets.slice();
        newDiets.splice(index, 1);
        localStorage.setItem("updatedDiets", JSON.stringify(newDiets));
        setDiets(newDiets);
        setDisableSubmit(false);
    };

    return (
        <div className="border-b border-gray-900/10 pb-12">
            <h2 
            className="text-2xl font-semibold leading-7 text-gray-900"
            >
                Régimes alimentaire
            </h2>

            <div className="grid grid-cols-4 gap-y-12 w-10/12 py-5">
                {diets.map((diet, index) => (
                    <Diet
                        key={index}
                        index={index}
                        handleDietsCheckboxChange={handleDietsCheckboxChange}
                        onDeleteDiet={onDeleteDiet}
                        name={diet.name}
                        description={diet.description}
                        checked={diet.checked}
                        isStarter={diet.isStarter}
                        forbiddenFoods={diet.forbiddenFoods}
                        diets={diets}
                        setDiets={setDiets}
                    />
                ))}
                <AddDietCard
                    diets={diets}
                    setDiets={setDiets}
                />
            </div>
        </div>
    );
}

export default DietProfile;