import { useState } from "react";
import { useSearchParams } from 'react-router-dom';


const SearchBar = ({ onSearch }) => {
  let [searchParams] = useSearchParams();
  const [query, setQuery] = useState(searchParams.get("search") || "");

  const handleInputChange = (event) => {
    setQuery(event.target.value);
  };

  const handleSearch = () => {
    onSearch(query);
  };

  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <>
      <label htmlFor="default-search" className="mb-2 text-sm font-medium text-gray-900 sr-only">
        Rechercher
      </label>
      <div className="relative">
        <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
          <svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="28" height="28" viewBox="0 0 72 72" className="fill-[#777]">
                <path d="M 31 11 C 19.973 11 11 19.973 11 31 C 11 42.027 19.973 51 31 51 C 34.974166 51 38.672385 49.821569 41.789062 47.814453 L 54.726562 60.751953 C 56.390563 62.415953 59.088953 62.415953 60.751953 60.751953 C 62.415953 59.087953 62.415953 56.390563 60.751953 54.726562 L 47.814453 41.789062 C 49.821569 38.672385 51 34.974166 51 31 C 51 19.973 42.027 11 31 11 z M 31 19 C 37.616 19 43 24.384 43 31 C 43 37.616 37.616 43 31 43 C 24.384 43 19 37.616 19 31 C 19 24.384 24.384 19 31 19 z"></path>
          </svg>
        </div>
        <input type="search" id="default-search"
          className="
            block w-full text-[1.4em] font-bold text-[#555] pl-12 px-3 py-2 rounded-[180px] border-[#e5e4e2]
            bg-[#e5e4e2]
          "
          placeholder="Rechercher un café"
          autoComplete="off"
          autoCorrect="off"
          spellCheck="false"
          value={query}
          onKeyDown={handleKeyDown}
          onInput={handleInputChange}
        />
      </div>
    </>
  );
};

export default SearchBar;
