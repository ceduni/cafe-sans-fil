import React, { useState, useMemo, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Import Leaflet default icons via ES modules
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png';
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';
import { CafeAPI } from '@/utils/api';

const mapboxToken = import.meta.env.VITE_MAPBOX_TOKEN;

console.log("Mapbox token:", import.meta.env);

/**
 * Automatically adjust map bounds to given positions
 */
function FitBounds({ positions }) {
    const map = useMap();
    useEffect(() => {
        if (positions.length) {
            map.fitBounds(positions, { padding: [50, 50] });
        }
    }, [positions, map]);
    return null;
}


export default function CafesMap({ mapStyle = 'streets-v11' }) {

    const [cafes, setCafes] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    // Fetching cafe
    useEffect(() => {
        CafeAPI.getAll(setIsLoading)
            .then((data) => {
                setCafes(data);
            })
            .catch((error) => {
                setError(error)
            })
    }, []);

    // Search & filter state
    const [search, setSearch] = useState('');

    // Filtered cafes
    const filtered = useMemo(
        () =>
            cafes.filter((c) => {
                const matchesName = c.name.toLowerCase().includes(search.toLowerCase());
                return matchesName && c.coordinates; // Ensure coordinates exist
            }),
        [cafes, search]
    );

    // Positions for bounds
    const positions = filtered.map((c) => c.coordinates);

    return (
        <div style={{ display: 'flex', height: '100%' }}>
            {/* Sidebar */}
            <div style={{ width: 250, padding: 16, background: '#fff', overflowY: 'auto' }}>
                <h3>Filtres</h3>
                <input
                    type="text"
                    placeholder="Rechercher..."
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    style={{ width: '100%', marginBottom: 8, padding: 4 }}
                />
             
                {/* <ul style={{ listStyle: 'none', padding: 0 }}>
                    {filtered.map((c) => (
                        <li
                            key={c.id}
                            onClick={() => {
                                // Fly to selected cafe
                                const event = new CustomEvent('flyToCafe', { detail: [c.latitude, c.longitude] });
                                window.dispatchEvent(event);
                            }}
                            style={{ cursor: 'pointer', marginBottom: 8 }}
                        >
                            {c.name}
                        </li>
                    ))}
                </ul> */}
            </div>

            {/* Map */}
            <MapContainer style={{ flex: 1 }} zoom={13} center={[0, 0]}>
                <TileLayer
                    url={`https://api.mapbox.com/styles/v1/mapbox/${mapStyle}/tiles/{z}/{x}/{y}@2x?access_token=${mapboxToken}`}
                    tileSize={512}
                    zoomOffset={-1}
                    attribution='&copy; <a href="https://www.mapbox.com">Mapbox</a>'
                />
                <FitBounds positions={positions} />
                {filtered.map((cafe) => {
                    const icon = L.icon({
                        iconUrl: cafe.logo || cafe.image,
                        iconSize: [40, 40],
                        iconAnchor: [20, 40],
                        popupAnchor: [0, -40],
                    });
                    return (
                        <Marker key={cafe.id} position={cafe.coordinates} icon={icon}>
                            <Popup>
                                <div style={{ maxWidth: 200 }}>
                                    <img
                                        src={cafe.logo}
                                        alt={cafe.name}
                                        style={{ width: '100%', height: 'auto', marginBottom: 8, borderRadius: 4 }}
                                    />
                                    <h4 style={{ margin: '4px 0' }}>{cafe.name}</h4>
                                    {cafe.description && <p style={{ margin: '4px 0' }}>{cafe.description}</p>}
                                    <button
                                        style={{ marginTop: 8, padding: '6px 12px', border: 'none', borderRadius: 4, cursor: 'pointer' }}
                                        onClick={() => alert(`Plus d'infos sur ${cafe.name}`)}
                                    >
                                        Détails
                                    </button>
                                </div>
                            </Popup>
                        </Marker>
                    );
                })}
            </MapContainer>
        </div>
    );
}
