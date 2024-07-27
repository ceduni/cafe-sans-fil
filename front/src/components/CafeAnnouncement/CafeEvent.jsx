import { useState } from 'react';

const CafeEvent = ({ event }) => {
    // const { cafe, title, date, content, tags, likes } = event;

    const [reactions, setReactions] = useState(18);
    const [hasReacted, setHasReacted] = useState(false);

    const handleReaction = () => {
        if (hasReacted) {
            setReactions(reactions - 1);
        } else {
            setReactions(reactions + 1);
        }
        setHasReacted(!hasReacted);
    };

    return (
        <div className="card-container">
            <div className="photo-container">
                <div className="event-date">
                    <span className="day">14</span>
                    <span className="month">Février</span>
                    <span className="hour">19h30</span>
                </div>
                <div className="event-venue">
                    <span>7077 Ave du Parc</span>
                    <span>Agora du 5e etage</span>
                </div>
            </div>
            <div className="info-container">
                <h3 className="event-name">
                    Saint-Valentin
                </h3>
                <div className="event-description">
                    Plongez dans l'atmosphère romantique de la Saint-Valentin avec une soirée spécialement conçue pour célébrer l'amour sous toutes ses formes. 
                    Que vous soyez en couple, célibataire ou simplement en quête d'une bonne soirée entre amis, cette soirée est faite pour vous !
                </div>
            </div>
            <div className="event-media">
                <img className="event-image" src="assets/valentin.jpg" alt="" />
            </div>
            {/* <div className="event-actions">
                <button className="btn-action btn-action--support">
                    <svg className="btn-icon" stroke="currentColor" stroke-width="0" viewBox="0 0 576 512" height="200px" width="200px" xmlns="http://www.w3.org/2000/svg">
                        <path d="M275.3 250.5c7 7.4 18.4 7.4 25.5 0l108.9-114.2c31.6-33.2 29.8-88.2-5.6-118.8-30.8-26.7-76.7-21.9-104.9 7.7L288 36.9l-11.1-11.6C248.7-4.4 202.8-9.2 172 17.5c-35.3 30.6-37.2 85.6-5.6 118.8l108.9 114.2zm290 77.6c-11.8-10.7-30.2-10-42.6 0L430.3 402c-11.3 9.1-25.4 14-40 14H272c-8.8 0-16-7.2-16-16s7.2-16 16-16h78.3c15.9 0 30.7-10.9 33.3-26.6 3.3-20-12.1-37.4-31.6-37.4H192c-27 0-53.1 9.3-74.1 26.3L71.4 384H16c-8.8 0-16 7.2-16 16v96c0 8.8 7.2 16 16 16h356.8c14.5 0 28.6-4.9 40-14L564 377c15.2-12.1 16.4-35.3 1.3-48.9z"></path>
                    </svg>
                </button>
                <button className="btn-action btn-action--attend">
                    <svg className="btn-icon" stroke="currentColor" stroke-width="0" viewBox="0 0 512 512" height="200px" width="200px" xmlns="http://www.w3.org/2000/svg">
                        <path d="M429.58 209.08c-15.06-6.62-32.38 1.31-38.5 17.62L356 312h-11.27V80c0-17.6-13.3-32-29.55-32-16.26 0-29.55 14.4-29.55 32v151.75l-14.78.25V32c0-17.6-13.3-32-29.55-32s-29.55 14.4-29.55 32v199.75L197 232V64c0-17.6-13.3-32-29.55-32-16.26 0-29.55 14.4-29.55 32v183.75l-14.8.25V128c0-17.6-13.3-32-29.55-32S64 110.4 64 128v216c0 75.8 37.13 168 169 168 40.8 0 79.42-7 100.66-21a121.41 121.41 0 0 0 33.72-33.31 138 138 0 0 0 16-31.78l62.45-175.14c6.17-16.31-1.19-35.06-16.25-41.69z"></path>
                    </svg>
                </button>
            </div> */}
        </div>
    );
};

export default CafeEvent;
