// src/components/Modal.js
import React, { useState } from 'react';
import toast from 'react-hot-toast';

const AddDietModal = ({ isOpen, setIsOpen, diets, setDiets }) => {

    const [newDiet, setNewDiet] = useState({
        name: "",
        checked: false,
        isStarter: false,
        description: "",
        ingredients: []
    });

    const toggleModal = () => {
        setIsOpen(!isOpen);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (newDiet.name !== "" && newDiet.ingredients.length !== 0 && newDiet.ingredients.includes("") === false) {
            if (diets.some((diet) => diet.name === newDiet.name)) {
                toast.error("Ce régime existe déjà");
                return;
            }
            //toast.loading("Ajout du nouveau régime...");
            //console.log(newDiet.ingredients);
            localStorage.setItem("updatedDiets", JSON.stringify(
                [...diets, newDiet]
            ));
            
            setDiets([...diets, newDiet]);
            toast.success("Votre profil a été mis à jour");
        } else {
            toast.error("Veuillez remplir au moins les deux premiers champs");
        }
    };

    const formatIngredients = (ingredientsInput) => {
        const splittedIngrdients = ingredientsInput.split(",");
        setNewDiet({ ...newDiet, ingredients: splittedIngrdients.map((ingredient) => ingredient.trim().toLowerCase()) });
    };

  return (
    isOpen && (
    <div className="fixed inset-0 z-50 flex items-center justify-center w-full h-full overflow-x-hidden overflow-y-auto bg-gray-800 bg-opacity-50">
        <div className="relative w-full max-w-md p-4 bg-white rounded-lg shadow dark:bg-white-700">
        <div className="flex items-center justify-between p-4 border-b rounded-t dark:border-gray-600">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-dark">
            Ajouter un nouveau régime
            </h3>
            <button 
            onClick={toggleModal} 
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
                    <label htmlFor="name" className="block mb-2 text-sm font-medium text-gray-900 dark:text-dark">
                        Nom
                    </label>
                    <input
                    type="text" 
                    name="name" 
                    id="name" 
                    className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-white-600 dark:border-white-500 dark:placeholder-white-400 dark:text-dark dark:focus:ring-primary-500 dark:focus:border-primary-500" 
                    placeholder="Nom du nouveau régime" 
                    onChange={(e) => setNewDiet({ ...newDiet, name: e.target.value })}
                    required 
                    />
                </div>

                <div 
                className="col-span-2"
                >
                    <label htmlFor="name" className="block mb-2 text-sm font-medium text-gray-900 dark:text-dark">
                        Aliments non désirés
                    </label>
                    <input
                    type="text" 
                    name="name" 
                    id="name" 
                    className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-white-600 dark:border-white-500 dark:placeholder-white-400 dark:text-dark dark:focus:ring-primary-500 dark:focus:border-primary-500" 
                    placeholder="Exemple: Poisson, Oeuf, Fromage"
                    onChange={(e) => formatIngredients(e.target.value)} 
                    required 
                    />
                </div>

                <div 
                className="col-span-2"
                >
                    <label htmlFor="name" className="block mb-2 text-sm font-medium text-gray-900 dark:text-dark">
                        Aliments désirés
                    </label>
                    <input
                    type="text" 
                    name="name" 
                    id="name" 
                    className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-white-600 dark:border-white-500 dark:placeholder-white-400 dark:text-dark dark:focus:ring-primary-500 dark:focus:border-primary-500" 
                    placeholder="Exemple: Poisson, Oeuf, Fromage"
                    onChange={(e) => formatIngredients(e.target.value)} 
                    required 
                    />
                </div>

                <div className="col-span-2">
                    <label htmlFor="description" className="block mb-2 text-sm font-medium text-gray-900 dark:text-dark">
                        Description du régime
                    </label>
                    <textarea 
                    id="description" 
                    rows="4" 
                    className="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-white-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-dark dark:focus:ring-blue-500 dark:focus:border-blue-500" 
                    placeholder="Description"
                    onChange={(e) => setNewDiet({ ...newDiet, description: e.target.value })}
                    ></textarea>                    
                </div>
            </div>
            <button 
            type="submit" 
            className="text-white inline-flex items-center bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
            onClick={handleSubmit}
            >
                <svg className="me-1 -ms-1 w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fillRule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clipRule="evenodd">
                    </path>
                </svg>
                Ajouter
            </button>
        </form>
        </div>
    </div>
    )
  );
};

export default AddDietModal;
