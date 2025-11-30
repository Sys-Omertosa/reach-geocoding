import { useEffect, useRef, forwardRef, useImperativeHandle } from "react";
import mapboxgl from "mapbox-gl";
import customStyle from "./style.json";

export interface MapProps {
  accessToken: string;
  center?: [number, number];
  zoom?: number;
  onMapClick?: (
    coordinates: [number, number],
    event: mapboxgl.MapMouseEvent
  ) => void;
  markers?: Array<{
    coordinates: [number, number];
    popupContent?: string;
    onClick?: () => void;
  }>;
  className?: string;
}

export interface MapRef {
  flyTo: (coordinates: [number, number], zoomLevel?: number) => void;
  getMap: () => mapboxgl.Map | null;
  highlightPolygon: (geometry: any) => void;
  clearHighlight: () => void;
}

export const MapComponent = forwardRef<MapRef, MapProps>(
  (
    {
      accessToken,
      center = [69.3451, 30.3753], // Default to Pakistan center
      zoom = 3,
      onMapClick,
      markers = [],
      className = "w-full h-full",
    },
    ref
  ) => {
    const mapContainer = useRef<HTMLDivElement>(null);
    const map = useRef<mapboxgl.Map | null>(null);
    const markersRef = useRef<mapboxgl.Marker[]>([]);

    // Initialize map
    useEffect(() => {
      if (!mapContainer.current || map.current) return; // Don't reinitialize if map already exists

      // Set the access token
      mapboxgl.accessToken = accessToken;

      // Create the map
      map.current = new mapboxgl.Map({
        container: mapContainer.current,
        // style: "mapbox://styles/mapbox/dark-v11",
        style: customStyle as any,
        center: center,
        zoom: zoom,
        preserveDrawingBuffer: true, // Help prevent context loss
        antialias: false, // Reduce GPU load
      });

      // Handle WebGL context loss
      map.current.on("webglcontextlost", (e) => {
        console.warn("WebGL context lost");
        if (e.originalEvent) {
          e.originalEvent.preventDefault();
        }
      });

      // Handle WebGL context restore
      map.current.on("webglcontextrestored", () => {
        console.log("WebGL context restored");
        // Re-add any highlights or custom layers here if needed
      });

      // Add navigation controls
      map.current.addControl(new mapboxgl.NavigationControl(), "top-left");

      // Add full screen control
      map.current.addControl(new mapboxgl.FullscreenControl(), "top-left");

      // Add scale control
      map.current.addControl(
        new mapboxgl.ScaleControl({
          maxWidth: 100,
          unit: "metric",
        }),
        "bottom-left"
      );

      // Handle map clicks if callback provided
      if (onMapClick) {
        map.current.on("click", (e) => {
          const coordinates: [number, number] = [e.lngLat.lng, e.lngLat.lat];
          onMapClick(coordinates, e);
        });
      }

      // Cleanup function
      return () => {
        if (map.current) {
          map.current.remove();
          map.current = null;
        }
      };
    }, [accessToken]); // Only depend on accessToken to minimize re-initialization

    // Update markers when markers prop changes
    useEffect(() => {
      if (!map.current) return;

      // Clear existing markers
      markersRef.current.forEach((marker) => marker.remove());
      markersRef.current = [];

      // Add new markers
      markers.forEach(({ coordinates, popupContent, onClick }) => {
        const marker = new mapboxgl.Marker()
          .setLngLat(coordinates)
          .addTo(map.current!);

        if (popupContent) {
          const popup = new mapboxgl.Popup({ offset: 25 }).setHTML(
            popupContent
          );
          marker.setPopup(popup);
        }

        if (onClick) {
          marker.getElement().addEventListener("click", (e) => {
            e.stopPropagation(); // Prevent map click event
            onClick();
          });
        }

        markersRef.current.push(marker);
      });
    }, [markers]);

    // Fly to location
    const flyTo = (coordinates: [number, number], zoomLevel?: number) => {
      if (!map.current) return;

      map.current.flyTo({
        center: coordinates,
        zoom: zoomLevel || map.current.getZoom(),
        essential: true,
      });
    };

    // Function to convert PostGIS geometry to GeoJSON
    const convertToGeoJSON = (geometry: any): any => {
      if (!geometry) return null;

      try {
        if (typeof geometry === "string") {
          // Parse WKT format
          const polygonMatch = geometry.match(
            /POLYGON\s*\(\s*\(\s*([\d.-\s,]+)\s*\)\s*\)/i
          );
          if (polygonMatch) {
            const coordString = polygonMatch[1];
            const coordinates: number[][] = [];

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

            return {
              type: "Feature",
              geometry: {
                type: "Polygon",
                coordinates: [coordinates],
              },
            };
          }
        } else if (geometry && typeof geometry === "object") {
          if (geometry.type === "Polygon") {
            return {
              type: "Feature",
              geometry: geometry,
            };
          }
        }
      } catch (error) {
        console.warn("Failed to convert geometry to GeoJSON:", error);
      }

      return null;
    };

    const highlightPolygon = (geometry: any) => {
      if (!map.current) {
        console.warn("Map not available for highlighting");
        return;
      }

      // Wait for map to be fully loaded
      if (!map.current.isStyleLoaded()) {
        console.log("Map style not loaded yet, waiting...");
        map.current.once("styledata", () => {
          highlightPolygon(geometry);
        });
        return;
      }

      console.log("Highlighting polygon with geometry:", geometry);

      const geoJSON = convertToGeoJSON(geometry);
      console.log("Converted to GeoJSON:", geoJSON);

      if (!geoJSON) {
        console.warn("Failed to convert geometry to GeoJSON");
        return;
      }

      try {
        // Remove existing highlight if any
        clearHighlight();

        // Check if map is still valid before adding layers
        if (!map.current.getStyle()) {
          console.warn("Map style not available, skipping polygon highlight");
          return;
        }

        // Add the polygon as a source
        map.current.addSource("highlighted-polygon", {
          type: "geojson",
          data: geoJSON,
        });

        // Add fill layer
        map.current.addLayer({
          id: "highlighted-polygon-fill",
          type: "fill",
          source: "highlighted-polygon",
          paint: {
            "fill-color": "#006240", // Bangladesh green - more muted
            "fill-opacity": 0.25,
          },
        });

        // Add outline layer
        map.current.addLayer({
          id: "highlighted-polygon-outline",
          type: "line",
          source: "highlighted-polygon",
          paint: {
            "line-color": "#2fa96c", // Mint green - softer outline
            "line-width": 2,
          },
        });

        console.log("Polygon highlight added successfully");
      } catch (error) {
        console.warn(
          "Failed to add polygon highlight (context may be lost):",
          error
        );
        // Try to recover by waiting and retrying once
        setTimeout(() => {
          try {
            if (map.current && map.current.getStyle()) {
              highlightPolygon(geometry);
            }
          } catch (retryError) {
            console.warn("Retry failed, polygon highlighting unavailable");
          }
        }, 100);
      }
    };

    const clearHighlight = () => {
      if (!map.current) return;

      try {
        // Remove layers if they exist
        if (map.current.getLayer("highlighted-polygon-fill")) {
          map.current.removeLayer("highlighted-polygon-fill");
        }
        if (map.current.getLayer("highlighted-polygon-outline")) {
          map.current.removeLayer("highlighted-polygon-outline");
        }
        // Remove source if it exists
        if (map.current.getSource("highlighted-polygon")) {
          map.current.removeSource("highlighted-polygon");
        }
      } catch (error) {
        console.warn(
          "Failed to clear polygon highlight (this is normal after context loss):",
          error
        );
      }
    };

    // Expose map methods via ref
    useImperativeHandle(ref, () => ({
      flyTo,
      getMap: () => map.current,
      highlightPolygon,
      clearHighlight,
    }));

    return (
      <div ref={mapContainer} className={className} key="mapbox-container" />
    );
  }
);
