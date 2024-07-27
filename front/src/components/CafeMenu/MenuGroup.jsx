import { useRef } from 'react';
import PropTypes from 'prop-types';
import Item from './MenuItem';
import { isNull } from '@/utils/helpers';

function isChildOf(targetElement, ancestorSelector) {
    return !isNull(targetElement.closest(ancestorSelector));
}


const GroupBox = ({ category, items, onClick, onItemClick, activeItem, setActiveItem }) => {
    const groupBoxElement = useRef(null);

    const handleClick = (event) => {
        const target = event.target;

        if (groupBoxElement.current) {
            onClick(groupBoxElement.current);

            if (activeItem && !isChildOf(target, '.group-item')) {
                activeItem.classList.remove("active")
                setActiveItem(null);
            }
        }

    };

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

GroupBox.propTypes = {
    // category: PropTypes.shape({
    //     index: PropTypes.number.isRequired,
    //     name: PropTypes.string.isRequired,
    // }).isRequired,
    category: PropTypes.string.isRequired,
    items: PropTypes.arrayOf(PropTypes.object).isRequired,
    onClick: PropTypes.func.isRequired,
    onItemClick: PropTypes.func.isRequired,
    activeItem: PropTypes.object.isRequired,
    setActiveItem: PropTypes.func.isRequired,
};

export default GroupBox;
