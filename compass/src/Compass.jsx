import { useState, MouseEvent } from 'react'
import * as d3 from "d3"
import './Compass.css'

const campusLocations = [
  {name: "3200 rue Jean-Brillant", lat: 45.4986961521,lon: -73.61837733088691},
  {name: "Campus MIL",lat: 45.52321560692185, lon: -73.61964977321544},
  {name: "Campus de Saint-Hyacinthe",lat: 45.620964331491415, lon: -72.96657098855336},
  {name: "Cepsum",lat: 45.50879970900878, lon: -73.61327768855713},
  {name: "Pavillon André-Aisenstadt",lat: 45.50124930434351, lon: -73.61573488671026},
  {name: "Pavillon Jean-Coutu",lat: 45.50045997347204, lon: -73.6147671986653},
  {name: "Pavillon Liliane-De-Stewart",lat: 45.50980130660043, lon: -73.61925130205117},
  {name: "Pavillon Lionel-Groulx",lat: 45.49953769180418, lon: -73.6183292597221},
  {name: "Pavillon Marie-Victorin",lat: 45.51079917407623, lon: -73.61159104184188},
  {name: "Pavillon Maximilien-Caron",lat: 45.49876641300788, lon: -73.61699093088687},
  {name: "Pavillon Roger-Gaudry",lat: 45.50281677249842, lon: -73.61509567465617},
  {name: "Pavillon de la Faculté de Musique",lat: 45.509379713232626, lon: -73.60866752165107},
  {name: "Pavillon de la Faculté de l’Aménagement",lat: 45.50491025275026, lon: -73.62126301300778},
];

const user = {lat: 45.502869750762905, lon: -73.61833155386769};

function Compass() {
  const [zoom, setZoom] = useState(3);
  const [angle, setAngle] = useState(0);

  

  return (
    <>
      {/*Define compass wheels here*/}
      <div className='compass'>
        <svg height="1000" width="1000"  style={{
          transform: `rotate(${angle}deg)`,
          transformOrigin: "50% 90%",
          transition: "transform 0.5s ease-in-out",
          overflow: "visible"
        }}>

          {/*Render wheels of the compass*/}
          {Array.from({length: zoom}).map((_, i) =>(
            <circle 
              key={i} 
              cx="50%" 
              cy="90%"
              r={(50/zoom)*(i+1)+"%"}
              fill="none" 
              stroke="red"
            />
          ))}

          {/*This circle is to test bearing placement*/}
          {/*
          <circle 
            cx="50%" 
            cy="77%"
            r="5%" 
            fill="blue" 
            style={{
              transform: `rotate(0deg)`,
              transformOrigin: "50% 90%",
              transition: "transform 0.5s ease-in-out",
              overflow: "visible"}}/>
          */}

          {campusLocations.map((campus) => (
            <Waypoint 
              key={campus.name}
              origin={user}
              destination={campus}
              threshold={zoom}
            />
          ))}


          {/*This circle represents user current/start location*/}
          <circle cx="50%" cy="90%" r={(10/zoom)+"%"} fill="red" />
        </svg>
      </div>


      {/*Define controls for UI here*/}
      <div className="controls">
        <div className="zoom">
          <button 
            onClick={() => setZoom(
              (zoom) => zoom > 1 ? zoom - 1 : zoom = 1
            )}>
            -
          </button>
          <button 
            onClick={() => setZoom(
              (zoom) => zoom < 5 ? zoom + 1 : zoom = 5
            )}>
            +
          </button><p>zoom is {zoom}</p>
        </div>
        <div className="rotate">
          <button 
            onClick={() => setAngle(
              (angle) => (angle - 30)
            )}>
            {"<"}
          </button>
          <button 
            onClick={() => setAngle(
              (angle) => (angle + 30)
            )}>
            {">"}
          </button><p>angle is {angle}</p>
        </div>
      </div>
    </>
  )
}

function Waypoint({origin, destination, threshold}) {
  let {r, theta} = toPolar(origin.lat, origin.lon, destination.lat, destination.lon);
  r = r > 3000 ? 5 : Math.floor(r/500);
  let n = destination.name;
  console.log({r, n, theta, threshold});
  
  if (r > threshold){
  } else {
    return (
      <>
        <circle 
          cx="50%"
          cy={(90-(50/threshold*2)-(50/threshold)*r)+"%"}
          r={(10/threshold)+"%"}
          fill="none"
          stroke="red"
          style={{
              transform: `rotate(${theta}deg)`,
              transformOrigin: "50% 90%",
              transition: "transform 0.5s ease-in-out",
              overflow: "visible"}}
        />
      </>
    )
  }
}

function Control({state, incState, decState, inc, dec, name}) {
  return (
    <div className={name}>
      <button onClick={decState}>
            {dec}
      </button> 
      <button onClick={incState}>
            {inc}
      </button>
      <p>state is {state}</p>
    </div>
  )
}

function toRad(deg) {
  return (deg * Math.PI) / 180
}

function haversine(lat1, lon1, lat2, lon2) {
    const R = 6371e3; // Radius of Earth in meters

    const dLat = toRad(lat2 - lat1);
    const dLon = toRad(lon2 - lon1);

    const a =
        Math.sin(dLat / 2) ** 2 +
        Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLon / 2) ** 2;

    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c; // Distance in meters
}

function toPolar(lat1, lon1, lat2, lon2) {
    const r = haversine(lat1, lon1, lat2, lon2); // Distance as radius
    
    const phi1 = toRad(lat1);
    const phi2 = toRad(lat2);
    const dLon = toRad(lon2 - lon1);

    // Compute bearing angle
    let theta = Math.atan2(
        Math.sin(dLon) * Math.cos(phi2),
        Math.cos(phi1) * Math.sin(phi2) - Math.sin(phi1) * Math.cos(phi2) * Math.cos(dLon)
    );

    theta = (theta * 180) / Math.PI; // Convert to degrees
    if (theta < 0) theta += 360; // Normalize to 0-360 degrees
    return { r, theta };
}

export default Compass
