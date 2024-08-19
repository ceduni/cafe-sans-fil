import { useEffect, useState } from "react";
import EmptyState from "@/components/EmptyState";
import { CafeCard, CafeCardLoading } from "@/components/Cafe/CafeCard";
import { PAYMENT_METHODS } from "@/utils/cafe";
import { CafeAPI } from "@/utils/api";
import getCurrentUser from "@/utils/users";


const isEmpty = (arr) => arr?.length === 0

/**
 * 
 * @param {Cafe} cafe 
 * @param {*} filters 
 * @returns 
 */
function filterCafe(cafe, filters, userDietProfile) {
    const { openOnly, pavillon, takesCash, takesCreditCard, takesDebitCard, diets } = filters;

    if (openOnly && !cafe.isOpen()) {
        return false;
    }

    if (pavillon !== "Tous les pavillons" && cafe.location.pavillon === pavillon) {
        return false;
    }

    if (takesCash && cafe.payment_methods.some((method) => method.method === PAYMENT_METHODS.CASH)) {
        return false;
    }

    if (takesCreditCard && cafe.payment_methods.some((method) => method.method === PAYMENT_METHODS.CREDIT_CARD)) {
        return false;
    }

    if (takesDebitCard && cafe.payment_methods.some((method) => method.method === PAYMENT_METHODS.DEBIT_CARD)) {
        return false;
    }

    if (!filterCafeByDiet(cafe, filters, userDietProfile)) {
        return false;
    }

    return true;
}
function filterCafeByDiet(cafe, filters, userDietProfile) {
    if (Object.keys(filters.diets).length === 0) {
        return true;
    }

    const validDiets = Object.keys(filters.diets).filter(
        (diet) => filters.diets[diet]
    );

    let validDietsItems = [];

    for (const validDiet of validDiets) {
        userDietProfile.diets.forEach((diet) => {
            if (diet.name === validDiet) {
                validDietsItems = [
                    ...validDietsItems,
                    diet.desired_foods.map((item) => item.toLowerCase()),
                ];
            }
        });
    }

    const itemsNameSet = new Set(cafe.menu.map((item) => item.name.toLowerCase()));

    const validItems = validDietsItems.filter((dietItem) => {
        const dietItemsSet = new Set(dietItem)
        return itemsNameSet.intersection(dietItemsSet).size > 0;
    });

    return validItems.length === validDietsItems.length;
}

function renderError(error) {
    return <div className="mt-20 mb-36"><EmptyState type="error" error={error} /></div>;
}

function renderEmpty() {
    return (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 py-8 animate-pulse duration-100">
            {Array.from({ length: 20 }).map((_, i) => (
                <CafeCardLoading key={i} />
            ))}
        </div>
    );
}

/**
 * 
 * @param {Cafe[]} cafes 
 * @param {*} filters 
 * @param {*} setFilters 
 * @returns 
 */
function renderCafe(cafes, filters, userDietProfile) {
    const filteredData = cafes.filter((cafe) => filterCafe(cafe, filters, userDietProfile));

    const sortedData = filteredData.sort((a, b) => {
        if (a.health_score > b.health_score) {
            return -1;
        }
        if (a.health_score < b.health_score) {
            return 1;
        }
        return 0;
    });

    return (
        <div className="relative bottom-4 xl:bottom-2">

            {isEmpty(sortedData) && (
                <div className="mt-20 mb-36">
                    <EmptyState name="café" />
                </div>
            )}

            <div className="grid animate-fade-in grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 py-8">
                {sortedData.map((cafe) => (
                    <CafeCard cafe={cafe} key={cafe.slug} />
                ))}
            </div>
        </div>
    );
}

const CafeList = ({ setStoredCafes, storedCafes, filters }) => {
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    const [userDietProfile, setUserDietProfile] = useState(null);

    // Fetching cafe
    useEffect(() => {
        CafeAPI.getAll(setIsLoading)
            .then((data) => {
                setStoredCafes(data);
            })
            .catch((error) => {
                setError(error)
            })

        getCurrentUser().then((user) => {
            setUserDietProfile(user.diet_profile)
        })

    }, []);


    if (error) {
        console.trace(error);
        return renderError(error);
    }

    if (isLoading && isEmpty(storedCafes)) {
        return renderEmpty();
    }

    return renderCafe(storedCafes, filters, userDietProfile);
};

export default CafeList;