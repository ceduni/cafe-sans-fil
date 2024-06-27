import useApi from "@/hooks/useApi";
import Container from "@/components/Container";
import ItemCard from "./Items/ItemCard";

const Recommandations = async ({ cafeSlug }) => {
    const { data } = useApi(`/recommendations/${cafeSlug}`)
    const recommendations = data.recommendations
    return (
        <>
            <Container className="pt-12 border-t border-gray-200">
                <h2 className=" text-4xl text-center font-bold text-gray-900 tracking-wide">Recommandations</h2>
            </Container>
            <div className="mt-6 grid grid-cols-2 gap-x-6 gap-y-10 sm:grid-cols-3 lg:grid-cols-4 lg:gap-x-8 items-start">
                {recommendations.map((product) => (
                    <ItemCard key={product.item_id} item={product} cafeSlug={cafeSlug} />
                ))}
            </div>
        </>
    );
}

export default Recommandations;