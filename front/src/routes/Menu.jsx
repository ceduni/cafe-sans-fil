import React, { useState, useRef, useEffect} from 'react';
import classNames from 'classnames';
import ItemCard from "@/components/Items/ItemCard";
import { getCafeCategories,getItemByCategory } from '@/utils/items';
import Container from "@/components/Container";


const Menu = ({ items }) => {
  
  const [activeCategory, setActiveCategory] = useState(null);
  const menuRef = useRef(null);


  const handleCategoryClick = (category) => {
    setActiveCategory(category === activeCategory ? null : category);
  };

  const handleClickOutside = (event) => {
    if (menuRef.current && !menuRef.current.contains(event.target)) {
      setActiveCategory(null);
    }
  };


  useEffect(() => {
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const categories = getCafeCategories(items);

  return (
    <Container className="pt-6 pb-24 rounded border-gray-200 bg-gray-200">
      <h2 className="text-4xl text-center font-bold text-gray-900 mb-10">Menu</h2>
      <div ref={menuRef} className="menu-container">
      <div className={`grid grid-cols-2 grid-rows-2 gap-4 p-4`}> 
        {categories.map((category) => (
          <div
            key={category}
            className={classNames( "bg-white shadow-lg rounded-lg overflow-hidden transition-all duration-300 relative ",
            { "col-span-2": activeCategory === category },"cursor-pointer hover:bg-slate-200")}
            onClick={() => handleCategoryClick(category)}
          >
            <h3 className="text-xl font-semibold text-gray-800 p-4 ">
              {category}
            </h3>
            <div className={classNames(
                "grid grid-cols-2 p-1 transition-all duration-500 ease-in-out",
                { "gap-4": activeCategory === category, "max-h-screen": activeCategory === category },
                { "gap-4": activeCategory !== category, "max-h-40 overflow-hidden": activeCategory !== category }
              )}>
              {getItemByCategory(items, category).map((item) => (
                <ItemCard key={item.item_id} item={item} showDescription={activeCategory === category} />
              ))}
            </div>
          </div>
        ))}
        </div>
      </div>
    </Container>
  );
};

export default Menu;
