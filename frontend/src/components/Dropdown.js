import React, { useState, useEffect, useRef } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faChevronDown, faChevronUp } from "@fortawesome/free-solid-svg-icons";
import "./css/dropdown.css";

const Dropdown = ({ label, children }) => {
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const dropdownRef = useRef(null);

  const toggleDropdown = () => {
    setDropdownOpen(!dropdownOpen);
  };

  const handleClickOutside = (event) => {
    if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
      setDropdownOpen(false);
    }
  };

  useEffect(() => {
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  return (
    <div
      ref={dropdownRef}
      className={`dropdown ${dropdownOpen ? "open" : ""}`}
      onClick={toggleDropdown}
    >
      <span>
        {label}
        <span className="arrow">
          <FontAwesomeIcon icon={dropdownOpen ? faChevronUp : faChevronDown} />
        </span>
      </span>
      {dropdownOpen && <ul className="dropdown-menu">{children}</ul>}
    </div>
  );
};

export default Dropdown;
