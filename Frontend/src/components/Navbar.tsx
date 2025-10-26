import React from "react";

export interface NavbarProps {
  onToggleFilter: () => void;
  onToggleAlerts: () => void;
  onToggleDetails: () => void;
  isFilterOpen: boolean;
  isAlertsOpen: boolean;
  isDetailsOpen: boolean;
}

export const Navbar: React.FC<NavbarProps> = ({
  onToggleFilter,
  onToggleAlerts,
  onToggleDetails,
  isFilterOpen,
  isAlertsOpen,
  isDetailsOpen,
}) => {
  return (
    <div className="fixed left-0 top-0 h-full w-18 bg-rich-black z-50 flex flex-col items-center py-6">
      {/* Rotated REACH Logo */}
      <div className="mb-12">
        <div
          className="text-white font-bold text-lg tracking-wider opacity-60"
          style={{
            writingMode: "vertical-rl",
            textOrientation: "mixed",
            transform: "rotate(180deg)",
          }}
        >
          REACH
        </div>
      </div>

      {/* Navigation Buttons - Centered */}
      <div className="flex-1 flex flex-col justify-center space-y-6">
        {/* Filter Panel Toggle */}
        <button
          onClick={onToggleFilter}
          className={`nav-button w-12 h-12 flex items-center justify-center transition-all duration-200 ${
            isFilterOpen
              ? "nav-button-active text-white"
              : "text-white opacity-60 hover:opacity-100"
          }`}
          title="Toggle Filter Panel"
        >
          <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
            <path d="M3 7V5a2 2 0 012-2h14a2 2 0 012 2v2l-8 8v6l-4-2v-4L3 7z" />
          </svg>
        </button>

        {/* Recent Alerts Toggle */}
        <button
          onClick={onToggleAlerts}
          className={`nav-button w-12 h-12 flex items-center justify-center transition-all duration-200 ${
            isAlertsOpen
              ? "nav-button-active text-white"
              : "text-white opacity-60 hover:opacity-100"
          }`}
          title="Toggle Recent Alerts"
        >
          <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 2C13.1 2 14 2.9 14 4V8L15.5 9.5C15.8 9.8 16 10.2 16 10.6V19C16 20.1 15.1 21 14 21H6C4.9 21 4 20.1 4 19V10.6C4 10.2 4.2 9.8 4.5 9.5L6 8V4C6 2.9 6.9 2 8 2H12M10 4V7.5L8.5 9H11.5L10 7.5V4M12 11V13H8V11H12M12 15V17H8V15H12M18 14L16.5 12.5L18 11L22 15L18 19L16.5 17.5L18 16H18V14Z" />
          </svg>
        </button>

        {/* Details Panel Toggle */}
        <button
          onClick={onToggleDetails}
          className={`nav-button w-12 h-12 flex items-center justify-center transition-all duration-200 ${
            isDetailsOpen
              ? "nav-button-active text-white"
              : "text-white opacity-60 hover:opacity-100"
          }`}
          title="Toggle Details Panel"
        >
          <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
            <path d="M14 2H6C4.9 2 4 2.9 4 4V20C4 21.1 4.9 22 6 22H18C19.1 22 20 21.1 20 20V8L14 2M18 20H6V4H13V9H18V20M8 12V14H16V12H8M8 16V18H13V16H8Z" />
          </svg>
        </button>
      </div>

      {/* Copyright Text */}
      <div className="mt-auto">
        <div
          className="text-white text-xs opacity-40 tracking-wide"
          style={{
            writingMode: "vertical-rl",
            textOrientation: "mixed",
            transform: "rotate(180deg)",
          }}
        >
          Team REACH © 2025
        </div>
      </div>
    </div>
  );
};
