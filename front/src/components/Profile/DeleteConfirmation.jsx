import React, { useState } from 'react';

const DeleteConfirmation = ({ isModalOpen, setIsModalOpen, handleDeleteClick }) => {

  const toggleModal = () => {
    setIsModalOpen(!isModalOpen);
  };

  const deleteConfirmed = () => {
    toggleModal();
    handleDeleteClick();
  };

  return (
    <div className="flex justify-center items-center bg-gray-100">
        {isModalOpen && (
            <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
                <div className="relative w-full max-w-lg rounded-lg shadow bg-white" onClick={(e) => e.stopPropagation()}>
                    <div className="flex justify-between items-center p-5 border-b rounded-t dark:border-gray-700">
                        <h3 className="text-xl font-mediumt text-black dark:text-gray-900">
                            Confirmation suppression du compte
                        </h3>
                        <button
                            onClick={toggleModal}
                            className="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm p-1.5 ml-auto inline-flex items-center dark:hover:bg-red-600 dark:hover:text-white"
                        >
                            <svg
                            aria-hidden="true"
                            className="w-5 h-5"
                            fill="currentColor"
                            viewBox="0 0 20 20"
                            xmlns="http://www.w3.org/2000/svg"
                            >
                            <path
                                fillRule="evenodd"
                                d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                                clipRule="evenodd"
                            ></path>
                            </svg>
                            <span className="sr-only">Close modal</span>
                        </button>
                    </div>
                    <div className="p-6 space-y-6">
                    <p className="text-base leading-relaxed text-gray-500 dark:text-gray-600">
                        Êtes-vous sûr de vouloir supprimer votre compte ?
                    </p>
                    <div className="flex items-center p-4 mb-4 text-sm text-yellow-700 bg-yellow-100 rounded-lg dark:bg-yellow-200 dark:text-yellow-800" role="alert">
                        <svg aria-hidden="true" className="w-5 h-5 mr-3" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                            <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.748-1.36 3.514 0l4.286 7.623c.741 1.318-.195 2.928-1.757 2.928H5.728c-1.562 0-2.498-1.61-1.757-2.928l4.286-7.623zM11 14a1 1 0 10-2 0 1 1 0 002 0zM9 8a1 1 0 012 0v3a1 1 0 11-2 0V8z" clipRule="evenodd"></path>
                        </svg>
                        <span className="sr-only">Avertissement</span>
                        <div>
                            <span className="font-medium">Avertissement:</span> Cette action est irreversible.
                        </div>
                    </div>
                </div>
                <div className="flex justify-end p-6 space-x-2 border-t border-gray-200 rounded-b dark:border-gray-700">
                    <button
                        onClick={toggleModal}
                        className="text-black hover:bg-gray-300 focus:ring-4 focus:outline-none focus:ring-blue-300 rounded-lg border border-gray-700 text-sm font-medium px-5 py-2.5 hover:text-gray-900 focus:z-10"
                    >
                        Non, annuler
                    </button>
                    <button
                        type="button"
                        className="text-white bg-red-600 hover:bg-red-700 focus:ring-4 focus:outline-none focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-red-500 dark:hover:bg-red-600 dark:focus:ring-red-900"
                        onClick={deleteConfirmed}
                    >
                        <svg
                        className="w-5 h-5 mr-2 inline"
                        fill="currentColor"
                        viewBox="0 0 20 20"
                        xmlns="http://www.w3.org/2000/svg"
                        >
                        <path
                            fillRule="evenodd"
                            d="M8.257 3.099c.765-1.36 2.748-1.36 3.514 0l4.286 7.623c.741 1.318-.195 2.928-1.757 2.928H5.728c-1.562 0-2.498-1.61-1.757-2.928l4.286-7.623zM11 14a1 1 0 10-2 0 1 1 0 002 0zM9 8a1 1 0 012 0v3a1 1 0 11-2 0V8z"
                            clipRule="evenodd"
                        ></path>
                        </svg>
                        Oui, confirmer
                    </button>
                </div>
            </div>
        </div>
        )}
    </div>
  );
};

export default DeleteConfirmation;
