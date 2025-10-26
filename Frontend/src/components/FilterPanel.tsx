import React from "react";
import { DateRangeSelector } from "./DateRangeSelector";

export interface FilterPanelProps {
  isVisible: boolean;
  onClose: () => void;
  onDateRangeChange: (startDate: Date | null, endDate: Date | null) => void;
}

export const FilterPanel: React.FC<FilterPanelProps> = ({
  isVisible,
  onClose,
  onDateRangeChange,
}) => {
  return (
    <div
      className={`fixed top-4 right-4 w-96 frosted-glass transform transition-all duration-300 ease-in-out z-40 overflow-hidden ${
        isVisible ? "translate-y-0 opacity-100" : "-translate-y-full opacity-0"
      }`}
      style={{ bottom: "352px" }} // Leave gap above alerts panel (320px height + 16px margin + 16px gap)
    >
      <div className="h-full flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-4 pb-3">
          <div className="flex items-center gap-2">
            <svg
              className="w-4 h-4 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.707A1 1 0 013 7V4z"
              />
            </svg>
            <h3 className="text-base font-medium text-white">
              Filters & Search
            </h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 hover:bg-bangladesh-green rounded-full transition-colors"
          >
            <svg
              className="w-4 h-4 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>

        {/* Vertical line separator */}
        <div className="w-full h-px bg-stone mx-4"></div>

        {/* Scrollable Content */}
        <div className="flex-1 overflow-y-auto dark-scrollbar p-4 space-y-4">
          {/* Date Range Section */}
          <div>
            <div className="flex items-center gap-2 mb-3">
              <svg
                className="w-4 h-4 text-gray-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                />
              </svg>
              <span className="text-sm text-gray-400 font-medium">
                Date Range
              </span>
            </div>
            <DateRangeSelector
              onDateRangeChange={onDateRangeChange}
              className="!p-0 !shadow-none !bg-transparent"
            />
          </div>

          {/* Severity Filters */}
          <div>
            <div className="flex items-center gap-2 mb-3">
              <svg
                className="w-4 h-4 text-gray-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.5 0L4.268 13.5c-.77.833.192 2.5 1.732 2.5z"
                />
              </svg>
              <span className="text-sm text-gray-400 font-medium">
                Severity Levels
              </span>
            </div>
            <div className="grid grid-cols-2 gap-2">
              {[
                { name: "Extreme", level: 5, color: "text-red-400" },
                { name: "Severe", level: 4, color: "text-orange-400" },
                { name: "Moderate", level: 3, color: "text-yellow-400" },
                { name: "Minor", level: 2, color: "text-green-400" },
              ].map((severity) => (
                <label
                  key={severity.name}
                  className="flex items-center gap-2 p-2 rounded-lg hover:bg-rich-black hover:bg-opacity-30 cursor-pointer"
                >
                  <input
                    type="checkbox"
                    className="filter-checkbox"
                    defaultChecked
                  />
                  <span className={`text-sm font-bold ${severity.color}`}>
                    {severity.level}
                  </span>
                  <span className="text-xs text-gray-300">{severity.name}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Category Filters */}
          <div>
            <div className="flex items-center gap-2 mb-3">
              <svg
                className="w-4 h-4 text-gray-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"
                />
              </svg>
              <span className="text-sm text-gray-400 font-medium">
                Categories
              </span>
            </div>
            <div className="space-y-1">
              {[
                "Weather",
                "Geological",
                "Security",
                "Health",
                "Environmental",
                "Infrastructure",
              ].map((category) => (
                <label
                  key={category}
                  className="flex items-center gap-2 p-2 rounded-lg hover:bg-rich-black hover:bg-opacity-30 cursor-pointer"
                >
                  <input
                    type="checkbox"
                    className="filter-checkbox"
                    defaultChecked
                  />
                  <span className="text-xs text-gray-300">{category}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Quick Actions */}
          <div>
            <div className="flex items-center gap-2 mb-3">
              <svg
                className="w-4 h-4 text-gray-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M13 10V3L4 14h7v7l9-11h-7z"
                />
              </svg>
              <span className="text-sm text-gray-400 font-medium">
                Quick Actions
              </span>
            </div>
            <div className="flex gap-2">
              <button className="flex-1 px-3 py-1.5 text-xs bg-bangladesh-green hover:bg-mountain-meadow text-white hover:text-dark-green rounded-md transition-colors font-medium">
                Apply Filters
              </button>
              <button className="flex-1 px-3 py-1.5 text-xs border border-stone text-stone hover:bg-stone hover:text-dark-green rounded-md transition-colors font-medium">
                Reset All
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
