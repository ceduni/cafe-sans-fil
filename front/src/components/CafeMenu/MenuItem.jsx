import { useRef } from 'react';
import PropTypes from 'prop-types';

const Item = ({ data, onClick }) => {
    const { image, name, price, description, available } = data;
    const itemElement = useRef(null);

    const handleClick = () => {
        if (itemElement.current) {
            onClick(itemElement.current, data);
        }
    };

    return (
        <div className={`group-item ${available ? 'in' : 'out'}`} ref={itemElement} onClick={handleClick}>
            <img className="group-item-image" src={image} alt={name} />
            <div className="group-item-info">
                <div className="group-item-info-main">
                    <span className="group-item-name">{name}</span>
                    <span className="group-item-price">${(price).toFixed(2)}</span>
                </div>
                <div className="group-item-info-details">
                    <span className="group-item-desc">{description}</span>
                    {/* <ul className="bare-list group-item-variants">
            {variants.map((variant, index) => (
              <li key={index} className="group-item-variant">
                {variant}
              </li>
            ))}
          </ul> */}
                </div>
                <div className="group-item-reactions">
                    <button className="btn btn-reaction">
                        <svg className="btn-reaction-icon" stroke="currentColor" fill="currentColor" strokeWidth="0" viewBox="0 0 512 512" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg">
                            <path d="M313.4 32.9c26 5.2 42.9 30.5 37.7 56.5l-2.3 11.4c-5.3 26.7-15.1 52.1-28.8 75.2H464c26.5 0 48 21.5 48 48c0 18.5-10.5 34.6-25.9 42.6C497 275.4 504 288.9 504 304c0 23.4-16.8 42.9-38.9 47.1c4.4 7.3 6.9 15.8 6.9 24.9c0 21.3-13.9 39.4-33.1 45.6c.7 3.3 1.1 6.8 1.1 10.4c0 26.5-21.5 48-48 48H294.5c-19 0-37.5-5.6-53.3-16.1l-38.5-25.7C176 420.4 160 390.4 160 358.3V320 272 247.1c0-29.2 13.3-56.7 36-75l7.4-5.9c26.5-21.2 44.6-51 51.2-84.2l2.3-11.4c5.2-26 30.5-42.9 56.5-37.7zM32 192H96c17.7 0 32 14.3 32 32V448c0 17.7-14.3 32-32 32H32c-17.7 0-32-14.3-32-32V224c0-17.7 14.3-32 32-32z"></path>
                        </svg>
                        {Math.floor(Math.random() * (100 - 70 + 1)) + 70}%
                    </button>
                </div>
            </div>
        </div>
    );
};

Item.propTypes = {
    data: PropTypes.shape({
        image: PropTypes.string.isRequired,
        name: PropTypes.string.isRequired,
        price: PropTypes.number.isRequired,
        description: PropTypes.string.isRequired,
        // variants: PropTypes.arrayOf(PropTypes.string).isRequired,
        available: PropTypes.bool.isRequired,
    }).isRequired,
    onClick: PropTypes.func.isRequired,
};

export default Item;
