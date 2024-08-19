import { useState } from 'react';

const TagInput = ({ tags, setTags }) => {
    const [inputValue, setInputValue] = useState('');

    if (tags === undefined || tags === null) {
        return (
            <div></div>
        )
    }
    const handleKeyDown = (event) => {
        if (event.key === ',' || event.key === 'Enter' || event.key === 'Tab') {
            event.preventDefault();
            if (inputValue.trim() !== '') {
                setTags([...tags, inputValue.trim()]);
                setInputValue('');
            }
        }
    };

    const handleInputChange = (event) => {
        setInputValue(event.target.value);
    };

    const handleTagRemove = (indexToRemove, e) => {
        e.preventDefault();
        setTags(tags.filter((_, index) => index !== indexToRemove));
    };

    return (
        <div className="w-full max-w-md bg-white">
            <input
                type="text"
                value={inputValue}
                onChange={handleInputChange}
                onKeyDown={handleKeyDown}
                className="w-full p-2 border text-lg border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
                placeholder="Ajoutez un aliment"
            />
            <div className="flex flex-wrap mb-4">
                {tags.map((tag, index) => (
                    <div key={index} className="flex items-center bg-gray-200 rounded-full px-4 py-1 m-1">
                        <span className="text-lg text-gray-900">{tag}</span>
                        <button
                            className="ml-2 text-red-500 hover:text-red-700"
                            onClick={(e) => handleTagRemove(index, e)}
                        >
                            &times;
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default TagInput;