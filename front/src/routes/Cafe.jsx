import { useParams } from "react-router-dom";
// import { Helmet } from "react-helmet-async";
import { useTranslation } from "react-i18next";
import { useState, useEffect } from "react";
import { CafeAPI } from "@/utils/api";
import EmptyState from "@/components/Error/EmptyState";
import SocialLink from "@/components/Cafe/SocialLink";
import CafeIdentification from "@/components/CafeIdentification/CafeIdentification";
import PaymentType from "@/components/Cafe/PaymentType";
import CafeMenu from "@/components/CafeMenu/Menu";
import CafeAnnouncement from "@/components/CafeAnnouncement/CafeAnnouncement";
import CafePost from "@/components/CafeAnnouncement/CafePost";
import '@/assets/styles/cafe.css';
import useTitle from "@/hooks/useTitle";

const _lst = Object.entries;


const Cafe = () => {
    const { t } = useTranslation();

    

    const { id } = useParams();

    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    const [cafe, setCafe] = useState(null);

    // Fetching cafe
    useEffect(() => {
        CafeAPI.get(id, setIsLoading)
            .then((data) => {
                setCafe(data);
            })
            .catch((error) => {
                console.error(error);
                setError(error)
            })
    }, []);

    console.log(cafe);

    useTitle(cafe?.name && `${cafe.name} | ${APP_NAME}`)
    
    if (error) {
        if (error.status === 404) {
            throw new Response("Not found", { status: 404, statusText: t("error.404.cafe_not_found") });
        }

        return <EmptyState type="error" error={error} />;
    }

    if (isLoading) {
        return <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 py-8 animate-pulse duration-100"></div>
    }

    return (
        <>
            <header className={`relative h-[400px] flex items-end justify-between overflow-hidden;`} style={{ background: `url(${cafe.image}) center / cover no-repeat` }}>
                <div className="cafe-brand">
                    <img className="cafe-logo" src={cafe?.logo} alt={t("alt.cafe_logo")} />
                    <ul className="bare-list socials">
                        {_lst(cafe?.socials).map(([key, value], index) => (
                            <SocialLink key={index} platform={key} url={value} />
                        ))}
                    </ul>
                </div>
            </header>
            <section className="main-body">
                <div className="menu-section">
                    <div>
                        <h2 className="text-center my-0 text-3xl font-bold">Menu</h2>
                    </div>
                    {/* <div className="accepted-payments">
                        {cafe?.paymentMethods.map((p) => (
                            <PaymentType name={p.method} />
                        ))}
                    </div> */}
                    <CafeMenu items={cafe?.menu} />
                </div>
                <div className="cafe-identification">
                    <CafeIdentification cafe={cafe} />
                </div>
                {/* <div className="cafe-communication">
                    <div>
                        <h2 className="text-center my-0 text-3xl font-bold">Annonces</h2>
                    </div>
                    <ul className="bare-list posts">
                        {cafe?.announcements.map((value, index) => (
                            <CafeAnnouncement  key={index} announcement={value} />
                        ))}
                    </ul>
                </div> */}
            </section>
            <section className="cafe-event">
                <h3 className="title">{t("cafe.bulletin_board.title")}</h3>
                <ul className="bare-list grid-content">
                    {cafe?.announcements.map((value) => (
                        <CafePost  key={value.id} post={value} />
                    ))}
                </ul>
            </section>
        </>
    );
};

export default Cafe;
