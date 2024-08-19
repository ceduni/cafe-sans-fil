import { ALLERGEN_II, ALLERGEN_III } from "@/utils/items";

const AllergenStiker = ({ level }) => {
    return (
        level > 1 &&
        <div className={`absolute top-0 left-0 w-32 text-white ${level === 2 ? "bg-orange-600" : "bg-red-600"} opacity-100 px-3 py-1 font-bold`} >
            {level === 2 ? ALLERGEN_II : ALLERGEN_III}
        </div>
    )
}

export default AllergenStiker;