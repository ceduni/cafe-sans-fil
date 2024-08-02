import { useState, useRef, useEffect } from 'react';
import { getRoot } from '@/utils/globals';
import { PublicRecommendationAPI } from '@/utils/api';
import './styles.css'
import GroupBox from './MenuGroup';

function renderError(error) {
    return <div className="mt-20 mb-36"><EmptyState type="error" error={error} /></div>;
  }

const CafeMenu = ({ items: menuItems, cafeSlug }) => {
    const [activeGroup, setActiveGroup] = useState(null);
    const [activeItem, setActiveItem] = useState(null);
    const menuElement = useRef(null);
    const [publicRecommendation, setPublicRecommendation] = useState([]);
    const categories = [...new Set(menuItems.map(item => item.category))];


    const handleGroupClick = (group) => {
        if (activeGroup && group !== activeGroup) {
            activeGroup.classList.remove("active");
        }

        setActiveGroup(group);
        group.classList.add("active");

        const groupBoxRect = group.getBoundingClientRect();
        const distanceFromTop = 240;
        const topPositionToScroll = window.scrollY + groupBoxRect.top - distanceFromTop;

        window.scrollTo({
            top: topPositionToScroll,
            behavior: 'smooth'
        });
    };

    const handleItemClick = (item) => {
        if (activeItem && item !== activeItem) {
            activeItem.classList.remove("active")
        }

        setActiveItem(item);
        item.classList.add("active");
    }

    getRoot().addEventListener("click", (event) => {
        const target = event.target;
        const menu = menuElement.current;

        if (!menu) {
            return;
        }
        if (!menu.contains(target) || target === menu) {
            menu.classList.remove("active");
            menu.dataset.selected = "";

            if (activeGroup) {
                activeGroup.classList.remove("active");
                setActiveGroup(null)
            }
            if (activeItem) {
                activeItem.classList.remove("active");
                setActiveItem(null)
            }
        }
    });

    const [error, setError] = useState(null);

    useEffect(() => {
        PublicRecommendationAPI.get(cafeSlug)
            .then((data) => {
                setPublicRecommendation(menuItems.filter((item) => data.includes(item.slug)));
            })
            .catch((error) => {
                setError(error);
            })
    }, []);

    if (error) {
        console.trace(error);
        return renderError(error);
      }

    return (
        <div ref={menuElement} className="menu">
            <GroupBox
                category='Produits recommendés'
                items={publicRecommendation}
                onClick={handleGroupClick}
                onItemClick={handleItemClick}
                activeItem={activeItem}
                setActiveItem={setActiveItem}

            ></GroupBox>
            {categories.map((category, index) => (
                <GroupBox
                    key={index}
                    category={category}
                    activeItem={activeItem}
                    setActiveItem={setActiveItem}
                    items={menuItems.filter((item) => item.category === category)}
                    onClick={handleGroupClick}
                    onItemClick={handleItemClick}
                />
            ))}
        </div>
    );
};

export default CafeMenu;
