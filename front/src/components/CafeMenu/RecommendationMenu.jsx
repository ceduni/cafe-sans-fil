import { useState, useRef, useEffect } from 'react';
import { PublicRecommendationAPI, PersonnnalRecommendationAPI } from '@/utils/api';
import { useAuth } from '@/hooks/useAuth';
import EmptyState from '@/components/EmptyState';
import RecommendationBox from './RecommendationBox';

function renderError(error) {
    return <div className="mt-20 mb-36"><EmptyState type="error" error={error} /></div>;
}

const RecommendationMenu = ({ cafeSlug, menuItems }) => {
    const [activeItem, setActiveItem] = useState(null);
    const [publicRecommendation, setPublicRecommendation] = useState([]);
    const [personnalRecommendation, setPersonnalRecommendation] = useState([]);
    const { isLoggedIn } = useAuth();

    const handleItemClick = (item) => {
        if (activeItem && item !== activeItem) {
            activeItem.classList.remove("active")
        }

        setActiveItem(item);
        item.classList.add("active");
    }

    const [error, setError] = useState(null);
    const [personnalError, setPersonnalError] = useState(null);

    useEffect(() => {
        PublicRecommendationAPI.get(cafeSlug)
            .then((data) => {
                setPublicRecommendation(menuItems.filter((item) => data.includes(item.slug)));
            })
            .catch((error) => {
                setError(error);
            })

        if (isLoggedIn) {
            PersonnnalRecommendationAPI.get(isLoggedIn.user_id, cafeSlug)
                .then((data) => {
                    setPersonnalRecommendation(menuItems.filter((item) => data.includes(item.slug)));
                })
                .catch((error) => {
                    setPersonnalError(error);
                })
        }
    }, []);

    if (error) {
        console.trace(error);
        return renderError(error);
    }

    if (personnalError) {
        console.trace(personnalError);
        return renderError(personnalError);
    }

    return (
        <div className="menu">
            {/* <h2 className="text-center my-0 text-3xl font-bold">Pour toi</h2> */}
            {isLoggedIn && <RecommendationBox
                category='Pour toi'
                items={personnalRecommendation}
                onItemClick={handleItemClick}
                activeItem={activeItem}
                setActiveItem={setActiveItem}
            />}
            {/* <h2 className="text-center my-0 text-3xl font-bold">Produit recommdés</h2> */}
            <RecommendationBox
                category='Produits recommendés'
                items={publicRecommendation}
                onItemClick={handleItemClick}
                activeItem={activeItem}
                setActiveItem={setActiveItem}
            />
        </div>
    );
}

export default RecommendationMenu;