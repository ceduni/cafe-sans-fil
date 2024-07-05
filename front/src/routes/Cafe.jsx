import { useParams } from "react-router-dom";
import { Helmet } from "react-helmet-async";
import { useTranslation } from "react-i18next";
import { useState, useEffect } from "react";
import { CafeAPI } from "@/utils/api";
import EmptyState from "@/components/EmptyState";
import LogoInstagram from "@/assets/icons/logo-instagram.svg";
import LogoFacebook from "@/assets/icons/logo-facebook.svg";
import LogoX from "@/assets/icons/logo-x.svg";


const Cafe = () => {
    const { t } = useTranslation();

    const { id } = useParams();

    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    const [cafe, setCafe] = useState(null);

    // Fetching cafe
    useEffect(() => {
        CafeAPI.find(id, setIsLoading)
            .then((data) => {
                setCafe(data);
            })
            .catch((error) => {
                console.log(error);
                setError(error)
            })
    }, []);

    if (error) {
        if (error.status === 404) {
            throw new Response("Not found", { status: 404, statusText: t("error.404.cafe") });
        }

        return <EmptyState type="error" error={error} />;
    }

    if (isLoading) {
        return <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 py-8 animate-pulse duration-100"></div>
    }


    return (
        <>
            <Helmet>{cafe?.name && <title>{cafe.name} | {APP_NAME}</title>}</Helmet>
            <header className={`relative h-[400px] flex items-end justify-between overflow-hidden;`} style={{ background: `url(${cafe.image}) center / cover no-repeat` }}>
                <div className="cafe-brand">
                    <img className="cafe-logo" src="assets/logo_tore_fraction.jpg" alt="Logo du café" />
                        <ul className="bare-list socials">
                            <li className="social">
                                <a href="https://twitter.com" target="_blank">
                                    <img className="social-img" src={LogoX} alt="Logo de X (Twitter)" />
                                </a>
                            </li>
                            <li className="social">
                                <a href="https://www.facebook.com/CafeToreetFraction" target="_blank">
                                    <img className="social-img" src={LogoFacebook} alt="Logo de facebook" />
                                </a>
                            </li>
                            <li className="social">
                                <a href="https://www.instagram.com" target="_blank">
                                    <img className="social-img" src={LogoInstagram} alt="Logo de instagram" />
                                </a>
                            </li>
                        </ul>
                </div>
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
