import { useParams } from "react-router-dom";
import EmptyState from "@/components/EmptyState";
import { Helmet } from "react-helmet-async";
import { useState, useEffect } from "react";
import { CafeAPI } from "@/utils/api";


const Cafe = () => {
    const { id } = useParams();

    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    const [cafe, setCafe] = useState(null);

    // Fetching cafe
    useEffect(() => {
        CafeAPI.find(id, setIsLoading)
            .then((data) => {
                console.log(data);
                setCafe(data);
            })
            .catch((error) => {
                console.log(error);
                setError(error)
            })
    }, []);

    if (error) {
        if (error.status === 404) {
            throw new Response("Not found", { status: 404, statusText: "Ce café n'existe pas" });
        }
        return <EmptyState type="error" error={error} />;
    }

    if (isLoading) {
        return <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 py-8 animate-pulse duration-100"></div>
    }


    return (
        <>
            <Helmet>{cafe?.name && <title>{cafe.name} | Café sans-fil</title>}</Helmet>
            <header className={`relative h-[400px] flex items-end justify-between overflow-hidden;`} style={{background: `url(${cafe.image}) center / cover no-repeat`}}>
                
            </header>
            <section className="grid gap-[1vw] mt-6 px-[2vw] pb-6 lg:grid-cols-[1.5fr_1fr] lg:grid-rows-[auto_1fr]">
                <div className="menu-section">

                </div>
                <div className="cafe-identi">

                </div>
                <div className="menu-section">

                </div>
            </section>
        </>
    );
};

export default Cafe;
