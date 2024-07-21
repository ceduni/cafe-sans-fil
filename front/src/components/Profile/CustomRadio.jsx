import { useState } from 'react';

const CustomRadio = ({ name, initElements, setElements, setDisableSubmit }) => {
  const [activeButton, setActiveButton] = useState(null);

  const handleButtonClick = (buttonIndex) => {
    setDisableSubmit(false);
    setActiveButton(buttonIndex);
    const elementIndex = initElements.findIndex((elem) => elem.name === name);
    const newElements = [...initElements];
    newElements[elementIndex] = { name: name, value: buttonIndex };
    setElements(newElements);
  };
  
  return (
    <div className="flex">
      <button
        key={1}
        onClick={() => handleButtonClick(1)}
        className={`px-4 py-2 rounded ${
          activeButton === 1 ? `bg-emerald-600 text-white` : `bg-red-200 text-black`
        }`}
      >
        Faible
      </button>
      <button
        key={2}
        onClick={() => handleButtonClick(2)}
        className={`px-4 py-2 rounded ${
          activeButton === 2 ? `bg-emerald-600 text-white` : `bg-red-300 text-black`
        }`}
      >
        Moyen
      </button>
      <button
        key={3}
        onClick={() => handleButtonClick(3)}
        className={`px-4 py-2 rounded ${
          activeButton === 3 ? `bg-emerald-600 text-white` : `bg-red-400 text-black`
        }`}
      >
        Élevé
      </button>
    </div>
  );
};

export default CustomRadio;