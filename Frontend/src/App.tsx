import React, { useState, useRef } from "react";
import { MapComponent, type MapRef } from "./components/MapComponent";
import { DateRangeSelector } from "./components/DateRangeSelector";
import { DetailCard, type DetailData } from "./components/DetailCard";

// Sample data matching your schema structure
const sampleAlerts: DetailData[] = [
  {
    id: "1",
    title: "Flood Warning - Kathmandu Valley",
    description:
      "Heavy rainfall expected in Kathmandu Valley. Risk of flash flooding in low-lying areas. Residents advised to stay indoors and avoid unnecessary travel.",
    location: "Kathmandu Valley",
    date: new Date(2024, 9, 10, 14, 30), // October 10, 2024
    category: "Met",
    severity: "Severe",
    urgency: "Expected",
    instruction:
      "Avoid travel through flooded roads. Move to higher ground if necessary. Keep emergency supplies ready.",
    source: "NDMA",
    additionalInfo: {
      coordinates: [85.324, 27.7172],
    },
  },
  {
    id: "2",
    title: "Landslide Risk - Pokhara Region",
    description:
      "Increased landslide risk due to continuous rainfall. Several roads may become impassable.",
    location: "Pokhara Region",
    date: new Date(2024, 9, 11, 8, 15),
    category: "Geo",
    severity: "Moderate",
    urgency: "Expected",
    instruction: "Use alternative routes. Check road conditions before travel.",
    source: "NEOC",
    additionalInfo: {
      coordinates: [83.9856, 28.2096],
    },
  },
  {
    id: "3",
    title: "Air Quality Alert - Biratnagar",
    description:
      "Poor air quality due to industrial emissions and weather conditions. Health advisory issued.",
    location: "Biratnagar",
    date: new Date(2024, 9, 12, 10, 0),
    category: "Health",
    severity: "Minor",
    urgency: "Immediate",
    instruction:
      "Limit outdoor activities. Use air purifiers indoors. Wear masks when outside.",
    source: "NDMA",
    additionalInfo: {
      coordinates: [87.2718, 26.4525],
    },
  },
];

const MAPBOX_TOKEN = import.meta.env.VITE_MAPBOX_TOKEN || "";

export const App: React.FC = () => {
  const [currentAlerts, setCurrentAlerts] =
    useState<DetailData[]>(sampleAlerts);
  const [selectedAlert, setSelectedAlert] = useState<DetailData | null>(null);
  const [isDetailCardVisible, setIsDetailCardVisible] = useState(false);
  const mapRef = useRef<MapRef>(null);

  const getSeverityColor = (severity?: string): string => {
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

  const handleMapClick = (coordinates: [number, number], _event: any) => {
    const sampleAlert: DetailData = {
      id: "clicked-location",
      title: "Selected Location",
      description: `You clicked at coordinates: ${coordinates[1].toFixed(
        4
      )}, ${coordinates[0].toFixed(4)}`,
      location: `Lat: ${coordinates[1].toFixed(
        4
      )}, Lng: ${coordinates[0].toFixed(4)}`,
      date: new Date(),
      category: "Info",
      severity: "Unknown",
      urgency: "Unknown",
      instruction: "This is a sample alert for the clicked location.",
      source: "User Input",
    };

    setSelectedAlert(sampleAlert);
    setIsDetailCardVisible(true);
  };

  const handleDateRangeChange = (
    startDate: Date | null,
    endDate: Date | null
  ) => {
    console.log("Date range changed:", startDate, endDate);

    if (startDate && endDate) {
      const filtered = sampleAlerts.filter((alert) => {
        if (!alert.date) return false;
        return alert.date >= startDate && alert.date <= endDate;
      });
      setCurrentAlerts(filtered);
    } else {
      setCurrentAlerts(sampleAlerts);
    }
  };

  const handleAlertClick = (alert: DetailData) => {
    setSelectedAlert(alert);
    setIsDetailCardVisible(true);

    // Fly to location on map if coordinates available
    if (alert.additionalInfo?.coordinates && mapRef.current) {
      const [lng, lat] = alert.additionalInfo.coordinates;
      mapRef.current.flyTo([lng, lat], 12);
    }
  };

  const handleDetailCardClose = () => {
    setIsDetailCardVisible(false);
    setSelectedAlert(null);
  };

  const handleDetailCardAction = (action: string, data: DetailData) => {
    console.log("Detail card action:", action, data);

    switch (action) {
      case "view-more":
        alert(`View more details for: ${data.title}`);
        break;
      case "share":
        if (navigator.share) {
          navigator.share({
            title: data.title,
            text: data.description,
            url: window.location.href,
          });
        } else {
          navigator.clipboard.writeText(`${data.title}: ${data.description}`);
          alert("Alert details copied to clipboard!");
        }
        break;
    }
  };

  const refreshAlerts = () => {
    console.log("Refreshing alerts...");
    setCurrentAlerts(sampleAlerts);
  };

  // Prepare markers for map
  const mapMarkers = currentAlerts
    .filter((alert) => alert.additionalInfo?.coordinates)
    .map((alert) => ({
      coordinates: alert.additionalInfo!.coordinates as [number, number],
      popupContent: `
        <div class="p-2">
          <h3 class="font-semibold text-sm">${alert.title}</h3>
          <p class="text-xs text-gray-600 mt-1">${alert.description.substring(
            0,
            100
          )}...</p>
          <div class="mt-2">
            <span class="px-2 py-1 text-xs rounded-full ${getSeverityColor(
              alert.severity
            )}">${alert.severity}</span>
          </div>
        </div>
      `,
      onClick: () => handleAlertClick(alert),
    }));

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <div className="w-80 bg-white shadow-lg overflow-y-auto">
        <div className="p-6">
          <h1 className="text-2xl font-bold text-gray-900 mb-6">
            REACH Dashboard
          </h1>

          {/* Date Range Selector */}
          <DateRangeSelector
            onDateRangeChange={handleDateRangeChange}
            className="mb-6"
          />

          {/* Alerts List */}
          <div className="space-y-4">
            <h2 className="text-lg font-semibold text-gray-800">
              Recent Alerts
            </h2>
            <div className="space-y-2 max-h-96 overflow-y-auto">
              {currentAlerts.map((alert) => (
                <div
                  key={alert.id}
                  onClick={() => handleAlertClick(alert)}
                  className="p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors cursor-pointer"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <h3 className="font-medium text-sm text-gray-900">
                        {alert.title}
                      </h3>
                      <p className="text-xs text-gray-600 mt-1">
                        {alert.description.substring(0, 80)}...
                      </p>
                      <div className="flex gap-2 mt-2">
                        <span
                          className={`px-2 py-1 text-xs rounded-full ${getSeverityColor(
                            alert.severity
                          )}`}
                        >
                          {alert.severity}
                        </span>
                        {alert.category && (
                          <span className="px-2 py-1 text-xs rounded-full bg-blue-100 text-blue-800">
                            {alert.category}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 relative">
        <MapComponent
          ref={mapRef}
          accessToken={MAPBOX_TOKEN}
          center={[85.324, 27.7172]}
          zoom={7}
          onMapClick={handleMapClick}
          markers={mapMarkers}
          className="w-full h-full"
        />

        {/* Map Controls */}
        <div className="absolute top-4 left-4 bg-white rounded-lg shadow-md p-2">
          <button
            onClick={refreshAlerts}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors text-sm"
          >
            Refresh Alerts
          </button>
        </div>
      </div>

      {/* Detail Card */}
      <DetailCard
        isVisible={isDetailCardVisible}
        data={selectedAlert}
        onClose={handleDetailCardClose}
        onActionClick={handleDetailCardAction}
      />
    </div>
  );
};
