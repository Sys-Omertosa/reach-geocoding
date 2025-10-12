import { useEffect, useRef, forwardRef, useImperativeHandle } from "react";
import mapboxgl from "mapbox-gl";

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
}

export const MapComponent = forwardRef<MapRef, MapProps>(
  (
    {
      accessToken,
      center = [85.324, 27.7172], // Default to Kathmandu, Nepal
      zoom = 10,
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
      if (!mapContainer.current) return;

      // Set the access token
      mapboxgl.accessToken = accessToken;

      // Create the map
      map.current = new mapboxgl.Map({
        container: mapContainer.current,
        style: "mapbox://styles/mapbox/streets-v12",
        center: center,
        zoom: zoom,
      });

      // Add navigation controls
      map.current.addControl(new mapboxgl.NavigationControl(), "top-right");

      // Add full screen control
      map.current.addControl(new mapboxgl.FullscreenControl());

      // Add scale control
      map.current.addControl(
        new mapboxgl.ScaleControl({
          maxWidth: 100,
          unit: "metric",
        })
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
        }
      };
    }, [accessToken, center, zoom, onMapClick]);

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
          marker.getElement().addEventListener("click", onClick);
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

    // Expose map methods via ref
    useImperativeHandle(ref, () => ({
      flyTo,
      getMap: () => map.current,
    }));

    return <div ref={mapContainer} className={className} />;
  }
);
