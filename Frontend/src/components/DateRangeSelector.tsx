import React, { useState } from "react";
import { format, isValid, parseISO } from "date-fns";

export interface DateRangeSelectorProps {
  onDateRangeChange?: (startDate: Date | null, endDate: Date | null) => void;
  initialStartDate?: Date;
  initialEndDate?: Date;
  className?: string;
}

export const DateRangeSelector: React.FC<DateRangeSelectorProps> = ({
  onDateRangeChange,
  initialStartDate,
  initialEndDate,
  className = "",
}) => {
  const [startDate, setStartDate] = useState<string>(
    initialStartDate ? format(initialStartDate, "yyyy-MM-dd") : ""
  );
  const [endDate, setEndDate] = useState<string>(
    initialEndDate ? format(initialEndDate, "yyyy-MM-dd") : ""
  );

  const handleDateChange = (newStartDate: string, newEndDate: string) => {
    const parsedStartDate = newStartDate ? parseISO(newStartDate) : null;
    const parsedEndDate = newEndDate ? parseISO(newEndDate) : null;

    const validStartDate =
      parsedStartDate && isValid(parsedStartDate) ? parsedStartDate : null;
    const validEndDate =
      parsedEndDate && isValid(parsedEndDate) ? parsedEndDate : null;

    // Ensure start date is not after end date
    if (validStartDate && validEndDate && validStartDate > validEndDate) {
      setStartDate(format(validEndDate, "yyyy-MM-dd"));
      setEndDate(format(validStartDate, "yyyy-MM-dd"));
      onDateRangeChange?.(validEndDate, validStartDate);
    } else {
      onDateRangeChange?.(validStartDate, validEndDate);
    }
  };

  const handleStartDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newStartDate = e.target.value;
    setStartDate(newStartDate);
    handleDateChange(newStartDate, endDate);
  };

  const handleEndDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newEndDate = e.target.value;
    setEndDate(newEndDate);
    handleDateChange(startDate, newEndDate);
  };

  const clearDates = () => {
    setStartDate("");
    setEndDate("");
    onDateRangeChange?.(null, null);
  };

  const setLast7Days = () => {
    const end = new Date();
    const start = new Date();
    start.setDate(end.getDate() - 7);

    const startStr = format(start, "yyyy-MM-dd");
    const endStr = format(end, "yyyy-MM-dd");

    setStartDate(startStr);
    setEndDate(endStr);
    onDateRangeChange?.(start, end);
  };

  const setLast30Days = () => {
    const end = new Date();
    const start = new Date();
    start.setDate(end.getDate() - 30);

    const startStr = format(start, "yyyy-MM-dd");
    const endStr = format(end, "yyyy-MM-dd");

    setStartDate(startStr);
    setEndDate(endStr);
    onDateRangeChange?.(start, end);
  };

  return (
    <div className={`bg-white p-4 rounded-lg shadow-md border ${className}`}>
      <h3 className="text-lg font-semibold mb-3 text-gray-800">Date Range</h3>

      <div className="space-y-3">
        <div>
          <label
            htmlFor="start-date"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            Start Date
          </label>
          <input
            type="date"
            id="start-date"
            value={startDate}
            onChange={handleStartDateChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        <div>
          <label
            htmlFor="end-date"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            End Date
          </label>
          <input
            type="date"
            id="end-date"
            value={endDate}
            onChange={handleEndDateChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        <div className="flex gap-2">
          <button
            onClick={clearDates}
            className="px-3 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition-colors text-sm"
          >
            Clear
          </button>
          <button
            onClick={setLast7Days}
            className="px-3 py-2 bg-blue-100 text-blue-700 rounded-md hover:bg-blue-200 transition-colors text-sm"
          >
            Last 7 Days
          </button>
          <button
            onClick={setLast30Days}
            className="px-3 py-2 bg-blue-100 text-blue-700 rounded-md hover:bg-blue-200 transition-colors text-sm"
          >
            Last 30 Days
          </button>
        </div>
      </div>
    </div>
  );
};
