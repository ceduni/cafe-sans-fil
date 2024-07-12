import InfoModal from "@/components/InfoModal";

const Diet = ({ index, openModalIndex, handleOpenModal, handleCloseModal, handleDietsCheckboxChange, name, description, checked }) => {

    const handleButtonInfoClick = () => {
        handleOpenModal(index);
    };

    return (
        <div key={index} className="mb-2 flex items-center">
            <button
                type="button"
                className="w-5 h-5 pr flex items-center justify-center bg-blue-300 text-white rounded-full hover:bg-blue-600"
                onClick={handleButtonInfoClick}
            >
                i
            </button>
            <InfoModal 
                isOpen={openModalIndex === index} 
                onClose={handleCloseModal}
            >
                <p>{description}</p>
            </InfoModal>
            <label 
                className="mr-2 pl-2 text-gray-700 font-bold w-36 "
                title={description}
            >{name}</label>
            <input
                type="checkbox"
                checked={checked}
                onChange={() => handleDietsCheckboxChange(index)}
                className="mr-2 align-middle"
            />
        </div>
    );
};

export default Diet;
