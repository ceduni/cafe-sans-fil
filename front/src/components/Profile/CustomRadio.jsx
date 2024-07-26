import { useEffect, useState } from 'react';

const CustomRadio = ({ name, initElements, setElements, setDisableSubmit, initialColors, onClickColors, index }) => {
  const [activeButton, setActiveButton] = useState(null);

  const handleButtonClick = (buttonIndex) => {
    if (activeButton === buttonIndex) {
      setDisableSubmit(false);
      setActiveButton(null);
      const elementIndex = initElements.findIndex((elem) => elem.name === name);
      const newElements = [...initElements];
      newElements[elementIndex] = { name: name, value: null };
      setElements(newElements);
    } else {
      setDisableSubmit(false);
      setActiveButton(buttonIndex);
      const elementIndex = initElements.findIndex((elem) => elem.name === name);
      const newElements = [...initElements];
      newElements[elementIndex] = { name: name, value: buttonIndex };
      setElements(newElements);
    }
  };

  useEffect(() => {
    if (index){
      setActiveButton(index);
    }
  }, [index]);
  
  return (
    <div className="flex">
      <button
        key={1}
        onClick={() => handleButtonClick(1)}
        className={`px-4 py-2 font-bold ${
          activeButton === 1 ? `${onClickColors[0]} text-white` : `${initialColors[0]} text-black`
        }`}
      >
        Faible
      </button>
      <button
        key={2}
        onClick={() => handleButtonClick(2)}
        className={`px-4 py-2 font-bold ${
          activeButton === 2 ? `${onClickColors[1]} text-white` : `${initialColors[1]} text-black`
        }`}
      >
        Moyen
      </button>
      <button
        key={3}
        onClick={() => handleButtonClick(3)}
        className={`px-4 py-2 font-bold ${
          activeButton === 3 ? `${onClickColors[2]} text-white` : `${initialColors[2]} text-black`
        }`}
      >
        Élevé
      </button>
    </div>
  );
};

export default CustomRadio;