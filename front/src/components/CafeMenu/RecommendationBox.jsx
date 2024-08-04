import { useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import Item from './MenuItem';
import { isNull } from '@/utils/helpers';
import EmptyState from '@/components/EmptyState';

function isChildOf(targetElement, ancestorSelector) {
    return !isNull(targetElement.closest(ancestorSelector));
}


const RecommendationBox = ({ category, items, onItemClick, activeItem, setActiveItem }) => {
    const groupBoxElement = useRef(null);

    const handleClick = (event) => {
        const target = event.target;
        if (activeItem && !isChildOf(target, '.group-item')) {
            activeItem.classList.remove("active")
            setActiveItem(null);
        }
    };

    useEffect(() => {
        if (groupBoxElement.current) {
            groupBoxElement.current.classList.add('active')
        }
    }, []);

    if (items.length === 0) {
        return (
            <div className="group-box" ref={groupBoxElement} data-index={category.index} tabIndex={0}>
                <h4 className="group-box-title">{category}</h4>
                <div className="group-box-items">
                <h2 className="text-lg font-semibold text-gray-500">Aucune recommendation n'a été trouvée...</h2>
                </div>
            </div>
        );
    }

    return (
        <div className="group-box" ref={groupBoxElement} data-index={category.index} onClick={handleClick} tabIndex={0}>
            <h4 className="group-box-title">{category}</h4>
            <div className="group-box-items">
                {items.map((item, index) => (
                    <Item key={index} data={item} onClick={onItemClick} />
                ))}
            </div>
        </div>
    );
};

RecommendationBox.propTypes = {
    // category: PropTypes.shape({
    //     index: PropTypes.number.isRequired,
    //     name: PropTypes.string.isRequired,
    // }).isRequired,
    category: PropTypes.string.isRequired,
    items: PropTypes.arrayOf(PropTypes.object).isRequired,
    onItemClick: PropTypes.func.isRequired,
    activeItem: PropTypes.object.isRequired,
    setActiveItem: PropTypes.func.isRequired,
};

export default RecommendationBox;
