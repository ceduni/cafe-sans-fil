import { useState, useEffect, useRef, MouseEvent } from 'react'
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
const width = 500
const height = 500


function Compass() {
  const [zoom, setZoom] = useState(3);
  const [angle, setAngle] = useState(0);
  const [userLocation, setUserLocation] = useState(user);
  const svgRef = useRef();

  const compass = d3.select(svgRef.current)
      .attr("viewBox", [0, 0, width, height])
      .attr("text-anchor", "middle")
      .style("display", "block")
      .style("padding", "5%")
      .style("overflow", "visible");

  const ringScale = d3.scaleLinear().domain([0, 5]).range([height/20, height/2]);

  compass.selectAll("g").remove();
  compass.select("svg")
    .attr("transform", `rotate(${angle}deg)`)
    .attr("transformOrigin", `${width/2} ${height/2}`);

  // Create ring groups (structure taken from polar clock on D3 examples)
  const rings = compass.append("g")
    .attr("transform", `translate(${width / 2},${height / 2})`)
    .selectAll("g")
    .data([1,2,3,4,5])
    .join("g");

  // Add actual rings
  rings.append("circle")
    .attr("class", "ring")
    .attr("fill", "none")
    .attr("stroke", "#222")
    .attr("stroke-width", 1.5)
    .attr("r", d => ringScale(d)); 

  // Tooltip
  const tooltip = compass.append("text")
    .attr("font-size", "14px")
    .attr("fill", "black")
    .attr("text-anchor", "middle")
    .style("visibility", "hidden"); 
  
  // Add landmarks on the rings
  compass.selectAll(".landmarks")
      .data(campusLocations)
      .join("circle")
      .attr("class", "landmarks")
      .attr("cx", width/2)
      .attr("cy", height/2)
      .attr("r", 10)
      .attr("fill", "red")
      .attr("transform", (d) => {
        const {r, theta} = toPolar(user, d);
        console.log(r)
        return `translate(${Math.cos(theta) * ringScale(r)}, ${Math.sin(theta) * ringScale(r)})`
      }) 
      .attr("overflow", "visible") 
      .on("mouseover", (event, d) => {
        tooltip.text(d.name)
          .attr("x", event.offsetX)
          .attr("y", event.offsetY - 10)
          .style("visibility", "visible");
      })
      .on("mouseout", () => tooltip.style("visibility", "hidden")); 

  // Get info from device
  useEffect(() => {
    // Get user location
    navigator.geolocation.getCurrentPosition((position) => {
      setUserLocation({
        lat: position.coords.latitude,
        lon: position.coords.longitude,
      });
    });

    // Listen to device orientation (compass heading)
    const handleOrientation = (event) => {
      if (event.alpha !== null) {
        setAngle(event.alpha); // Alpha is the compass heading
      }
    };

    window.addEventListener("deviceorientation", handleOrientation);
    return () => window.removeEventListener("deviceorientation", handleOrientation); 
  }, []);

  return (
    <>
      <svg ref={svgRef} ></svg>
      {/*Define controls for UI here*/}
      <div className="controls">
        <div className="zoom">
          <button onClick={() => setZoom((zoom) => zoom > 1 ? zoom - 1 : zoom = 1)}>
            -
          </button>
          <button onClick={() => setZoom((zoom) => zoom < 5 ? zoom + 1 : zoom = 5)}>
            +
          </button><p>zoom is {zoom}</p>
        </div>
        <div className="rotate">
          <button onClick={() => setAngle((angle) => (angle - 30))}>
            {"<"}
          </button>
          <button onClick={() => setAngle((angle) => (angle + 30))}>
            {">"}
          </button><p>angle is {angle}</p>
        </div>
      </div>
    </>
  )
}

function Control({name, state, setState, inc, dec}) {
  return (
    <div className={name}>
      <button onClick={setState}>
            {dec}
      </button> 
      <button onClick={setState}>
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

function toPolar(origin, destination) {
    let lat1 = origin.lat;
    let lat2 = destination.lat
    let lon1 = origin.lon
    let lon2 = destination.lon
    let r = haversine(lat1, lon1, lat2, lon2); // Distance as radius
    
    const phi1 = toRad(lat1);
    const phi2 = toRad(lat2);
    const dLon = toRad(lon2 - lon1);

    // Compute bearing angle
    let theta = Math.atan2(
        Math.sin(dLon) * Math.cos(phi2),
        Math.cos(phi1) * Math.sin(phi2) - Math.sin(phi1) * Math.cos(phi2) * Math.cos(dLon)
    );

    //theta = (theta * 180) / Math.PI; // Convert to degrees
    //if (theta < 0) theta += 360; // Normalize to 0-360 degrees
    r = r > 3000 ? 5 : Math.ceil(r/500); 
    return { r , theta };
}

export default Compass
