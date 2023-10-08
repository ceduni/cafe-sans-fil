import { Outlet } from "react-router-dom";
import Navbar from "./Navbar";

const NavbarWrapper = () => {
  return (
    <>
      <Navbar />
      <div id="content">
        <Outlet />
      </div>
    </>
  );
};

export default NavbarWrapper;
