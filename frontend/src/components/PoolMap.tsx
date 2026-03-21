import { useEffect, useRef } from "react";
import { MapContainer, Marker, Popup, TileLayer, useMap } from "react-leaflet";
import L from "leaflet";
import type { Pool } from "../types";

// Fix default marker icons (Leaflet + bundlers issue)
import markerIcon2x from "leaflet/dist/images/marker-icon-2x.png";
import markerIcon from "leaflet/dist/images/marker-icon.png";
import markerShadow from "leaflet/dist/images/marker-shadow.png";

L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
});

const AMSTERDAM_CENTER: [number, number] = [52.36, 4.9];

interface PoolMapProps {
  pools: Pool[];
  highlightedPoolId: string | null;
  onHighlightClear: () => void;
}

function FitBounds({ pools }: { pools: Pool[] }) {
  const map = useMap();

  useEffect(() => {
    if (pools.length === 0) {
      map.setView(AMSTERDAM_CENTER, 12);
      return;
    }
    const bounds = L.latLngBounds(pools.map((p) => [p.lat, p.lng]));
    map.fitBounds(bounds, { padding: [40, 40], maxZoom: 14 });
  }, [map, pools]);

  return null;
}

function HighlightPool({
  pools,
  highlightedPoolId,
  onHighlightClear,
  markerRefs,
}: {
  pools: Pool[];
  highlightedPoolId: string | null;
  onHighlightClear: () => void;
  markerRefs: React.RefObject<Map<string, L.Marker>>;
}) {
  const map = useMap();

  useEffect(() => {
    if (!highlightedPoolId) return;
    const pool = pools.find((p) => p.id === highlightedPoolId);
    if (!pool) return;

    map.setView([pool.lat, pool.lng], 15, { animate: true });

    // Open the marker popup
    const marker = markerRefs.current?.get(highlightedPoolId);
    if (marker) {
      setTimeout(() => marker.openPopup(), 300);
    }

    onHighlightClear();
  }, [highlightedPoolId, pools, map, onHighlightClear, markerRefs]);

  return null;
}

export function PoolMap({
  pools,
  highlightedPoolId,
  onHighlightClear,
}: PoolMapProps) {
  const markerRefs = useRef(new Map<string, L.Marker>());

  return (
    <div className="overflow-hidden rounded-xl shadow-lg">
      <MapContainer
        center={AMSTERDAM_CENTER}
        zoom={12}
        className="h-[70vh] w-full"
        scrollWheelZoom={true}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <FitBounds pools={pools} />
        <HighlightPool
          pools={pools}
          highlightedPoolId={highlightedPoolId}
          onHighlightClear={onHighlightClear}
          markerRefs={markerRefs}
        />
        {pools.map((pool) => (
          <Marker
            key={pool.id}
            position={[pool.lat, pool.lng]}
            ref={(ref) => {
              if (ref) {
                markerRefs.current.set(pool.id, ref);
              }
            }}
          >
            <Popup>
              <div className="min-w-48">
                <h3 className="text-sm font-bold">{pool.name}</h3>
                <p className="text-xs text-gray-500">
                  {pool.type.charAt(0).toUpperCase() + pool.type.slice(1)} —{" "}
                  {pool.district}
                </p>
                <p className="mt-1 text-xs">{pool.address}</p>
                {pool.price != null && (
                  <p className="mt-1 text-xs font-medium">
                    &euro;{pool.price.toFixed(2)}
                    {pool.stadspasPrice != null &&
                      ` (Stadspas \u20ac${pool.stadspasPrice.toFixed(2)})`}
                  </p>
                )}
                <div className="mt-2 flex gap-2">
                  <a
                    href={`https://www.google.com/maps/search/?api=1&query=${pool.lat},${pool.lng}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-xs font-medium text-green-600 hover:text-green-800"
                  >
                    Google Maps
                  </a>
                  {pool.website && (
                    <a
                      href={pool.website}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-xs font-medium text-blue-600 hover:text-blue-800"
                    >
                      Website
                    </a>
                  )}
                  {pool.scheduleUrl && (
                    <a
                      href={pool.scheduleUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-xs font-medium text-indigo-600 hover:text-indigo-800"
                    >
                      Rooster
                    </a>
                  )}
                </div>
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}
