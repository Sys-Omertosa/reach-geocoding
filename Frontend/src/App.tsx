import React, { useState, useRef, useMemo, useCallback } from "react";
import { MapComponent, type MapRef } from "./components/MapComponent";
import { DateRangeSelector } from "./components/DateRangeSelector";
import { DetailCard, type DetailData } from "./components/DetailCard";
import { useAlerts } from "./hooks/useAlerts";
import type { AlertWithLocation } from "./types/database";

// Function to calculate centroid of a polygon
function calculatePolygonCentroid(coordinates: number[][]): [number, number] {
  let totalLng = 0;
  let totalLat = 0;
  let pointCount = coordinates.length;

  coordinates.forEach(([lng, lat]) => {
    totalLng += lng;
    totalLat += lat;
  });

  return [totalLng / pointCount, totalLat / pointCount];
}

// Function to extract centroid coordinates from PostGIS geometry data
function extractCoordinatesFromGeometry(polygon: any): [number, number] | null {
  if (!polygon) return null;

  try {
    // Handle different PostGIS geometry formats
    if (typeof polygon === "string") {
      // Parse WKT string like "POLYGON((lng lat, lng lat, ...))"
      const polygonMatch = polygon.match(
        /POLYGON\s*\(\s*\(\s*([\d.-\s,]+)\s*\)\s*\)/i
      );
      if (polygonMatch) {
        const coordString = polygonMatch[1];
        const coordinates: number[][] = [];

        // Extract all coordinate pairs
        const coordPairs = coordString.split(",");
        coordPairs.forEach((pair) => {
          const coords = pair.trim().split(/\s+/);
          if (coords.length >= 2) {
            const lng = parseFloat(coords[0]);
            const lat = parseFloat(coords[1]);
            if (!isNaN(lng) && !isNaN(lat)) {
              coordinates.push([lng, lat]);
            }
          }
        });

        if (coordinates.length > 0) {
          return calculatePolygonCentroid(coordinates);
        }
      }
    } else if (polygon && typeof polygon === "object") {
      // If it's a GeoJSON-like object
      if (polygon.type === "Polygon" && polygon.coordinates?.[0]) {
        const ringCoordinates = polygon.coordinates[0]; // Outer ring
        if (Array.isArray(ringCoordinates) && ringCoordinates.length > 0) {
          return calculatePolygonCentroid(ringCoordinates);
        }
      }
      // If it's a Point, return it directly
      if (polygon.type === "Point" && polygon.coordinates) {
        const [lng, lat] = polygon.coordinates;
        return [lng, lat];
      }
      // If coordinates are directly available as array
      if (polygon.coordinates && Array.isArray(polygon.coordinates)) {
        if (Array.isArray(polygon.coordinates[0])) {
          // It's an array of coordinates, calculate centroid
          return calculatePolygonCentroid(polygon.coordinates);
        } else {
          // It's a single coordinate pair
          const [lng, lat] = polygon.coordinates;
          return [lng, lat];
        }
      }
    }
  } catch (error) {
    console.warn("Failed to parse geometry:", error);
  }

  return null;
}

// Transform Supabase alert data to match our DetailData interface
function transformAlertToDetailData(alert: AlertWithLocation): DetailData {
  const firstLocation = alert.alert_areas?.[0]?.place;

  // Extract coordinates from PostGIS geometry data
  let coordinates: [number, number];

  if (firstLocation?.polygon) {
    const extractedCoords = extractCoordinatesFromGeometry(
      firstLocation.polygon
    );
    if (extractedCoords) {
      coordinates = extractedCoords;
    } else {
      // Fallback to Pakistan center if geometry parsing fails
      coordinates = [69.3451, 30.3753]; // Pakistan center
    }
  } else {
    // Default to Pakistan center if no geometry data
    coordinates = [69.3451, 30.3753];
  }

  return {
    id: alert.id,
    title: alert.event,
    description: alert.description,
    location: firstLocation?.name || "Unknown Location",
    date: new Date(alert.effective_from),
    category: alert.category,
    severity: alert.severity,
    urgency: alert.urgency,
    instruction: alert.instruction,
    source: alert.document?.source || "Unknown",
    additionalInfo: {
      coordinates,
      effectiveUntil: new Date(alert.effective_until),
      places:
        alert.alert_areas?.map((area) => area.place?.name).filter(Boolean) ||
        [],
      polygon: firstLocation?.polygon, // Include polygon data for highlighting
    },
  };
}

const MAPBOX_TOKEN = import.meta.env.VITE_MAPBOX_TOKEN || "";

export const App: React.FC = () => {
  const [selectedAlert, setSelectedAlert] = useState<DetailData | null>(null);
  const [isDetailCardVisible, setIsDetailCardVisible] = useState(false);
  const [dateFilters, setDateFilters] = useState<{
    startDate?: Date;
    endDate?: Date;
  }>({});
  const mapRef = useRef<MapRef>(null);

  // Use the Supabase alerts hook with filters
  const alertsFilters = useMemo(
    () => ({
      startDate: dateFilters.startDate,
      endDate: dateFilters.endDate,
    }),
    [dateFilters.startDate, dateFilters.endDate]
  );

  const {
    alerts: supabaseAlerts,
    loading,
    error,
    refetch,
  } = useAlerts({
    filters: alertsFilters,
    autoFetch: true,
  });

  // Transform Supabase alerts to DetailData format
  const currentAlerts = useMemo(
    () => supabaseAlerts.map(transformAlertToDetailData),
    [supabaseAlerts]
  );

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
    // Don't create a new alert if one is already selected
    // This allows users to interact with the map while viewing alert details
    if (isDetailCardVisible) {
      return;
    }

    // Only create a sample alert if no alert is currently selected
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

  const handleDateRangeChange = useCallback(
    (startDate: Date | null, endDate: Date | null) => {
      console.log("Date range changed:", startDate, endDate);
      setDateFilters({
        startDate: startDate || undefined,
        endDate: endDate || undefined,
      });
    },
    []
  );

  const handleAlertClick = (alert: DetailData) => {
    setSelectedAlert(alert);
    setIsDetailCardVisible(true);

    // Fly to location and highlight polygon on map
    if (alert.additionalInfo?.coordinates && mapRef.current) {
      const [lng, lat] = alert.additionalInfo.coordinates;
      mapRef.current.flyTo([lng, lat], 10);

      // Highlight the polygon if geometry data is available
      if (alert.additionalInfo?.polygon) {
        console.log("Highlighting polygon for:", alert.location);
        mapRef.current.highlightPolygon(alert.additionalInfo.polygon);
      } else {
        console.warn("No polygon data available for this alert");
      }
    }
  };

  const handleDetailCardClose = () => {
    setIsDetailCardVisible(false);
    setSelectedAlert(null);

    // Clear polygon highlight when closing detail card
    if (mapRef.current) {
      mapRef.current.clearHighlight();
    }
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

  const refreshAlerts = useCallback(() => {
    console.log("Refreshing alerts...");
    refetch();
  }, [refetch]);

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
    <div className="relative h-screen w-screen overflow-hidden">
      {/* Fixed Background Map */}
      <div className="fixed inset-0 z-0">
        <MapComponent
          ref={mapRef}
          accessToken={MAPBOX_TOKEN}
          center={[69.3451, 30.3753]}
          zoom={6}
          onMapClick={handleMapClick}
          markers={mapMarkers}
          className="w-full h-full"
        />
      </div>

      {/* Sidebar Overlay */}
      <div className="absolute top-0 left-0 w-80 h-full bg-white shadow-lg overflow-y-auto z-20">
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
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-semibold text-gray-800">
                Recent Alerts
              </h2>
              {loading && (
                <div className="animate-spin h-4 w-4 border-2 border-blue-500 border-t-transparent rounded-full"></div>
              )}
            </div>

            {error && (
              <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-sm text-red-700">
                  Error loading alerts: {error}
                </p>
                <button
                  onClick={refreshAlerts}
                  className="mt-2 px-3 py-1 bg-red-600 text-white text-xs rounded hover:bg-red-700"
                >
                  Retry
                </button>
              </div>
            )}

            <div className="space-y-2 max-h-96 overflow-y-auto">
              {currentAlerts.length === 0 && !loading && !error ? (
                <div className="p-4 text-center text-gray-500">
                  <p className="text-sm">No alerts found</p>
                  <p className="text-xs mt-1">Try adjusting your date range</p>
                </div>
              ) : (
                currentAlerts.map((alert) => (
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
                ))
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Map Controls Overlay */}
      <div className="absolute top-4 z-20" style={{ left: "336px" }}>
        <div className="bg-white rounded-lg shadow-md p-2">
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
