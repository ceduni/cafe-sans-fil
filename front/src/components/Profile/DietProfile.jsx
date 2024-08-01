import Diet from "@/components/Profile/Diet";
import AddDietButton from "@/components/Profile/AddDietButton";


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
        //localStorage.setItem("diets", JSON.stringify(newDiets));
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

            <div className="grid grid-cols-5 gap-y-6 gap-x-10 py-5">
                {diets.map((diet, index) => (
                    <Diet
                        key={index}
                        index={index}
                        handleDietsCheckboxChange={handleDietsCheckboxChange}
                        onDeleteDiet={onDeleteDiet}
                        name={diet.name}
                        description={diet.description}
                        checked={diet.checked}
                        isStarter={diet.is_starter}
                        forbidden_foods={diet.forbidden_foods}
                        diets={diets}
                        setDiets={setDiets}
                        desired_foods={diet.desired_foods}
                    />
                ))}
                <AddDietButton
                    diets={diets}
                    setDiets={setDiets}
                />
            </div>
        </div>
    );
}

export default DietProfile;