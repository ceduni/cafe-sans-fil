// src/components/Modal.js
import React, { useState } from 'react';
import toast from 'react-hot-toast';
import TagInput from '@/components/TagInput';

const EditDietModal = ({ isOpen, setIsOpen, diets, diet, setDiets }) => {
    const [newDiet, setNewDiet] = useState(diet);
    const [forbiddenFoods, setForbiddenFoods] = useState(diet.forbidden_foods);
    const [desiredFoods, setDesiredFoods] = useState(diet.desired_foods);
    const handleSubmit = (e) => {
        e.preventDefault();
        if (newDiet.name !== "" && forbiddenFoods.length !== 0 && forbiddenFoods.includes("") === false) {
            const dietIndex = diets.findIndex((d) => d.name === diet.name);
            const dietsCopy = [...diets];
            const newDiet2 = { ...newDiet, forbidden_foods: forbiddenFoods, desired_foods: desiredFoods };
            dietsCopy[dietIndex] = newDiet2;
            setDiets(dietsCopy);
            setIsOpen(false)
            toast.success("Régime ajouté");
        } else {
            toast.error("Veuillez remplir au moins les deux premiers champs");
        }
    };

  return (
    isOpen && (
    <div className="fixed inset-0 z-50 flex items-center justify-center w-full h-full overflow-x-hidden overflow-y-auto bg-gray-800 bg-opacity-50">
        <div className="relative w-full max-w-xl p-4 bg-white rounded-lg shadow dark:bg-white-700">
        <div className="flex items-center justify-between p-4 border-b rounded-t dark:border-gray-600">
            <h3 className="text-2xl font-semibold text-gray-900 dark:text-dark">
                Modifer le régime {diet.name}
            </h3>
            <button 
            onClick={() => setIsOpen(false)} 
            className="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 inline-flex justify-center items-center dark:hover:bg-red-600 dark:hover:text-white"
            >
            <svg className="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
                <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/>
            </svg>
            <span className="sr-only">Close modal</span>
            </button>
        </div>
        <form className="p-4 md:p-5">
            <div className="grid gap-4 mb-4 grid-cols-2">
                <div 
                className="col-span-2"
                >
                    <label htmlFor="name" className="block mb-2 text-lg font-medium text-gray-900 dark:text-dark">
                        Nom
                    </label>
                    <input
                    type="text" 
                    name="name" 
                    id="name" 
                    className="bg-gray-50 border border-gray-300 text-gray-900 text-lg rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-white-600 dark:border-white-500 dark:placeholder-white-400 dark:text-dark dark:focus:ring-primary-500 dark:focus:border-primary-500" 
                    placeholder="Nouveau nom" 
                    defaultValue={diet.name}
                    onChange={(e) => setNewDiet({ ...newDiet, name: e.target.value })}
                    />
                </div>

                <div className="col-span-5">
                    <label htmlFor="name" className="block mb-2 text-lg font-medium text-gray-900 dark:text-dark">
                        Aliments non désirés
                    </label>
                    <TagInput 
                        tags={forbiddenFoods}
                        setTags={setForbiddenFoods}
                    />
                </div>

                <div className="col-span-5">
                    <label htmlFor="name" className="block mb-2 text-lg font-medium text-gray-900 dark:text-dark">
                        Aliments désirés
                    </label>
                    <TagInput 
                        tags={desiredFoods}
                        setTags={setDesiredFoods}
                    />
                </div>

                <div className="col-span-2">
                    <label htmlFor="description" className="block mb-2 text-lg font-medium text-gray-900 dark:text-dark">
                        Description du régime
                    </label>
                    <textarea 
                    id="description" 
                    rows="4" 
                    className="block p-2.5 w-full text-lg text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-white-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-dark dark:focus:ring-blue-500 dark:focus:border-blue-500" 
                    placeholder="Description"
                    defaultValue={diet.description}
                    onChange={(e) => setNewDiet({ ...newDiet, description: e.target.value })}
                    ></textarea>                    
                </div>
            </div>
            <button 
            type="submit" 
            className="text-white inline-flex items-center bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-lg px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
            onClick={handleSubmit}
            >
                Enrégistrer
            </button>
        </form>
        </div>
    </div>
    )
  );
};

export default EditDietModal;
