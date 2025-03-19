import { useState, useRef } from 'react';
import { getRoot } from '@/utils/globals';

import './styles.css'
import GroupBox from './MenuGroup';


const CafeMenu = ({ menu }) => {
    const [activeGroup, setActiveGroup] = useState(null);
    const [activeItem, setActiveItem] = useState(null);
    const menuElement = useRef(null);

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

    return (
        <div ref={menuElement} className="menu">
              {/* <GroupBox
                    key="0"
                    category="Produits recommandés"
                    open={true}
                    activeItem={activeItem}
                    setActiveItem={setActiveItem}
                    items={menuItems.filter((item) => item.category === categories[0])}
                    onClick={handleGroupClick}
                    onItemClick={handleItemClick}
                /> */}
            {menu.categories.map((category, index) => (
                <GroupBox
                    key={index}
                    category={category}
                    activeItem={activeItem}
                    setActiveItem={setActiveItem}
                    onClick={handleGroupClick}
                    onItemClick={handleItemClick}
                />
            ))}
        </div>
    );
};

export default CafeMenu;
