// import Container from "@/components/Container";
// import { Helmet } from "react-helmet-async";
// // import SearchBar from "@/components/Search/SearchBar";
// import { useState } from "react";
// import CafeList from "@/components/Cafe/CafeList";
// import SearchResults from "@/components/Search/SearchResults";
// import { useSearchParams } from 'react-router-dom';



// const Home = () => {
//   let [searchParams] = useSearchParams();
//   const searchQuery = searchParams.get("search") || "";
//   console.log("Search query: ", searchQuery); // débug
//   const [storedCafes, setStoredCafes] = useState([]);
//   // const isSearching = searchQuery.length > 0;
//   // const [searchQuery, setSearchQuery] = useState("");
//   // const isSearching = searchQuery.length > 0;

 



//   return (
//     <>
//       <Helmet>
//         <title>Accueil | Café sans-fil</title>
//       </Helmet>
//       <Container className="pt-10 pb-[3.25rem] sm:py-14 space-y-6">
//         <div className="flex gap-2">
//           <h1 className="text-3xl sm:text-4xl text-opacity-90 font-secondary text-zinc-800 leading-7">
//             Cafés étudiants de l'UdeM
//           </h1>
//           {/* <a href="https://www.umontreal.ca/" target="_blank" rel="noopener noreferrer" className="my-auto sm:my-0">
//             <img src="/udem_logo.png" alt="UdeM Logo" className="h-9 object-contain" />
//           </a> */}
//         </div>
//         {/* <SearchBar searchQuery={searchQuery} setSearchQuery={setSearchQuery} /> */}
//       </Container>
//       <main>
//         {/* <Container>
//           {(!isSearching && <CafeList setStoredCafes={setStoredCafes} storedCafes={storedCafes} />) || (
//             <SearchResults searchQuery={searchQuery} storedCafes={storedCafes} />
//           )}
//         </Container> */}
//         <Container>
//         {searchQuery ? (
//             <SearchResults searchQuery={searchQuery} />
//           ) : (
//             <CafeList setStoredCafes={setStoredCafes} storedCafes={storedCafes} />
//           )}
//         </Container>
//       </main>
//     </>
//   );
// };

// export default Home;
