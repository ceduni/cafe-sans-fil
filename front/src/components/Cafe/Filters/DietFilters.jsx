import getCurrentUser from "@/utils/users";
import { useEffect, useState } from "react";
import DietFilterButton from "./DietFIlterButton";

const DietFilters = ({ setFilters }) => {
    const [diets, setDiets] = useState([]);
    const [activeDiets, setActiveDiets] = useState({});

    useEffect(() => {
        const init = async () => {
            const user = await getCurrentUser();
            const diets = user?.diet_profile?.diets
            setDiets(diets);

            const dictDiets = diets.reduce((acc, diet) => 
                ({ ...acc, [diet.name]: false }), {}
            );

            setActiveDiets(dictDiets);
        }
        init();
    }, []);

    useEffect(() => {
        const updateFilters = () => {
            setFilters({ ...setFilters, diets: activeDiets });
        }

        updateFilters();
    }, [activeDiets]);

    const isActive = (dietName) => {
        return dietName in activeDiets ? activeDiets[dietName] : false
    }

    return (
        <>
            {diets.map((diet) => (
                <DietFilterButton
                    key={diet.name}
                    name={diet.name}
                    active={isActive(diet.name)}
                    activeDiets={activeDiets}
                    setActiveDiets={setActiveDiets}
                    label={diet.name}
                />
            ))}
        </>
    );

}

export default DietFilters;