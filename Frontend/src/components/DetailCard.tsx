import React from "react";

export interface DetailData {
  id?: string;
  title: string;
  description: string;
  location?: string;
  date?: Date;
  category?: string;
  severity?: string;
  urgency?: string;
  instruction?: string;
  source?: string;
  additionalInfo?: Record<string, any>;
}

export interface DetailCardProps {
  isVisible: boolean;
  data: DetailData | null;
  onClose: () => void;
  onActionClick?: (action: string, data: DetailData) => void;
}

export const DetailCard: React.FC<DetailCardProps> = ({
  isVisible,
  data,
  onClose,
  onActionClick,
}) => {
  const formatDate = (date: Date) => {
    return date.toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  const getSeverityColor = (severity?: string) => {
    switch (severity?.toLowerCase()) {
      case "extreme":
        return "bg-red-100 text-red-800";
      case "severe":
        return "bg-orange-100 text-orange-800";
      case "moderate":
        return "bg-yellow-100 text-yellow-800";
      case "minor":
        return "bg-green-100 text-green-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  const getUrgencyColor = (urgency?: string) => {
    switch (urgency?.toLowerCase()) {
      case "immediate":
        return "bg-red-100 text-red-800";
      case "expected":
        return "bg-orange-100 text-orange-800";
      case "future":
        return "bg-blue-100 text-blue-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  const handleViewMore = () => {
    if (data && onActionClick) {
      onActionClick("view-more", data);
    }
  };

  const handleShare = () => {
    if (data && onActionClick) {
      onActionClick("share", data);
    }
  };

  const renderContent = () => {
    if (!data) {
      return (
        <div className="text-center text-gray-500 py-8">
          <svg
            className="w-12 h-12 mx-auto mb-4 text-gray-300"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          <p>Click on the map to view details</p>
        </div>
      );
    }

    return (
      <div className="space-y-4">
        {/* Title and description */}
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            {data.title}
          </h3>
          <p className="text-gray-600 text-sm leading-relaxed">
            {data.description}
          </p>
        </div>

        {/* Badges */}
        <div className="flex flex-wrap gap-2">
          {data.category && (
            <span className="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-full">
              {data.category}
            </span>
          )}
          {data.severity && (
            <span
              className={`px-2 py-1 text-xs font-medium ${getSeverityColor(
                data.severity
              )} rounded-full`}
            >
              {data.severity}
            </span>
          )}
          {data.urgency && (
            <span
              className={`px-2 py-1 text-xs font-medium ${getUrgencyColor(
                data.urgency
              )} rounded-full`}
            >
              {data.urgency}
            </span>
          )}
        </div>

        {/* Details */}
        <div className="space-y-3">
          {data.location && (
            <div className="flex items-start gap-2">
              <svg
                className="w-4 h-4 text-gray-400 mt-0.5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
                />
              </svg>
              <div>
                <span className="text-sm font-medium text-gray-700">
                  Location:
                </span>
                <span className="text-sm text-gray-600 ml-1">
                  {data.location}
                </span>
              </div>
            </div>
          )}

          {data.date && (
            <div className="flex items-start gap-2">
              <svg
                className="w-4 h-4 text-gray-400 mt-0.5"
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
              <div>
                <span className="text-sm font-medium text-gray-700">Date:</span>
                <span className="text-sm text-gray-600 ml-1">
                  {formatDate(data.date)}
                </span>
              </div>
            </div>
          )}

          {data.source && (
            <div className="flex items-start gap-2">
              <svg
                className="w-4 h-4 text-gray-400 mt-0.5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
              <div>
                <span className="text-sm font-medium text-gray-700">
                  Source:
                </span>
                <span className="text-sm text-gray-600 ml-1">
                  {data.source}
                </span>
              </div>
            </div>
          )}
        </div>

        {/* Instructions */}
        {data.instruction && (
          <div className="bg-blue-50 p-3 rounded-lg">
            <h4 className="text-sm font-medium text-blue-900 mb-1">
              Instructions
            </h4>
            <p className="text-sm text-blue-800">{data.instruction}</p>
          </div>
        )}

        {/* Actions */}
        <div className="flex gap-2 pt-2">
          <button
            onClick={handleViewMore}
            className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors text-sm font-medium"
          >
            View More Details
          </button>
          <button
            onClick={handleShare}
            className="px-4 py-2 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 transition-colors text-sm font-medium"
          >
            Share
          </button>
        </div>
      </div>
    );
  };

  return (
    <>
      {/* Detail card */}
      <div
        className={`fixed top-0 right-0 h-full w-96 bg-white shadow-xl transform transition-transform duration-300 ease-in-out z-50 overflow-y-auto ${
          isVisible ? "translate-x-0" : "translate-x-full"
        }`}
      >
        <div className="p-6">
          {/* Header */}
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold text-gray-900">Details</h2>
            <button
              onClick={onClose}
              className="p-2 hover:bg-gray-100 rounded-full transition-colors"
            >
              <svg
                className="w-5 h-5 text-gray-500"
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

          {/* Content */}
          <div>{renderContent()}</div>
        </div>
      </div>

      {/* Overlay */}
      <div
        className={`fixed inset-0 bg-black bg-opacity-50 transition-opacity duration-300 z-40 ${
          isVisible ? "opacity-100" : "opacity-0 invisible"
        }`}
        onClick={onClose}
      />
    </>
  );
};
