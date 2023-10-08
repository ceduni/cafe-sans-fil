import { Outlet } from "react-router-dom";
import Navbar from "./Navbar";

const NavbarWrapper = () => {
  return (
    <>
      <Navbar />
      <main>
        <Outlet />
      </main>
    </>
  );
};

export default NavbarWrapper;
