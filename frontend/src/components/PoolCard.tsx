import { useState } from "react";
import type { Pool } from "../types";

const TYPE_COLORS: Record<Pool["type"], string> = {
  binnenbad: "bg-blue-100 text-blue-800",
  combibad: "bg-green-100 text-green-800",
  buitenbad: "bg-orange-100 text-orange-800",
  leszwembad: "bg-gray-100 text-gray-800",
  wellness: "bg-purple-100 text-purple-800",
};

const TYPE_LABELS: Record<Pool["type"], string> = {
  binnenbad: "Binnenbad",
  combibad: "Combibad",
  buitenbad: "Buitenbad",
  leszwembad: "Leszwembad",
  wellness: "Wellness",
};

interface PoolCardProps {
  pool: Pool;
  onShowOnMap: (id: string) => void;
}

export function PoolCard({ pool, onShowOnMap }: PoolCardProps) {
  const [expanded, setExpanded] = useState(false);

  const googleMapsUrl = `https://www.google.com/maps/search/?api=1&query=${pool.lat},${pool.lng}`;

  return (
    <div
      id={`pool-${pool.id}`}
      className="flex flex-col rounded-xl bg-white shadow-md transition-shadow hover:shadow-lg"
    >
      {/* Header */}
      <div className="p-5 pb-3">
        <div className="mb-2 flex items-start justify-between gap-2">
          <div>
            <h3 className="text-lg font-bold text-gray-900">{pool.name}</h3>
            <p className="text-sm text-gray-500">{pool.district}</p>
          </div>
          <span
            className={`shrink-0 rounded-full px-2.5 py-0.5 text-xs font-medium ${TYPE_COLORS[pool.type]}`}
          >
            {TYPE_LABELS[pool.type]}
          </span>
        </div>

        {/* Feature pills */}
        <div className="mb-3 flex flex-wrap gap-1.5">
          {pool.has25m && (
            <span className="rounded-full bg-blue-50 px-2 py-0.5 text-xs font-medium text-blue-700">
              25m
            </span>
          )}
          {pool.has50m && (
            <span className="rounded-full bg-blue-50 px-2 py-0.5 text-xs font-medium text-blue-700">
              50m
            </span>
          )}
          {pool.crawlLane && (
            <span className="rounded-full bg-cyan-50 px-2 py-0.5 text-xs font-medium text-cyan-700">
              Crawlbaan
            </span>
          )}
          {pool.reservationRequired && (
            <span className="rounded-full bg-amber-50 px-2 py-0.5 text-xs font-medium text-amber-700">
              Reservering verplicht
            </span>
          )}
        </div>
      </div>

      {/* Info rows */}
      <div className="grow space-y-1.5 border-t border-gray-100 px-5 py-3 text-sm text-gray-600">
        <InfoRow label="Adres" value={pool.address} />
        {pool.phone && <InfoRow label="Tel" value={pool.phone} />}
        {pool.price != null && (
          <InfoRow
            label="Prijs"
            value={`\u20ac${pool.price.toFixed(2)}${pool.stadspasPrice != null ? ` (Stadspas \u20ac${pool.stadspasPrice.toFixed(2)})` : ""}`}
          />
        )}
        {pool.priceNote && !pool.price && (
          <InfoRow label="Prijs" value={pool.priceNote} />
        )}
        {pool.waterTemp != null && (
          <InfoRow label="Temp" value={`${pool.waterTemp}\u00b0C`} />
        )}
        {pool.dimensions && (
          <InfoRow label="Afmetingen" value={pool.dimensions} />
        )}
      </div>

      {/* Features */}
      {pool.features && (
        <div className="border-t border-gray-100 px-5 py-3">
          <p
            className={`text-sm text-gray-500 ${!expanded ? "line-clamp-2" : ""}`}
          >
            {pool.features}
          </p>
          {pool.features.length > 100 && (
            <button
              onClick={() => setExpanded(!expanded)}
              className="mt-1 text-xs font-medium text-blue-600 hover:text-blue-800"
            >
              {expanded ? "Minder" : "Meer lezen"}
            </button>
          )}
        </div>
      )}

      {/* Actions */}
      <div className="flex flex-wrap gap-2 border-t border-gray-100 p-4">
        <a
          href={googleMapsUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-1.5 rounded-lg bg-green-600 px-3 py-1.5 text-xs font-medium text-white shadow-sm hover:bg-green-700"
        >
          <svg className="h-3.5 w-3.5" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z" />
          </svg>
          Google Maps
        </a>
        {pool.website && (
          <a
            href={pool.website}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 rounded-lg bg-blue-600 px-3 py-1.5 text-xs font-medium text-white shadow-sm hover:bg-blue-700"
          >
            Website
          </a>
        )}
        {pool.scheduleUrl && (
          <a
            href={pool.scheduleUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 rounded-lg bg-indigo-600 px-3 py-1.5 text-xs font-medium text-white shadow-sm hover:bg-indigo-700"
          >
            Rooster
          </a>
        )}
        <button
          onClick={() => onShowOnMap(pool.id)}
          className="inline-flex items-center gap-1.5 rounded-lg border border-gray-300 px-3 py-1.5 text-xs font-medium text-gray-700 hover:bg-gray-50"
        >
          <svg className="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"
            />
          </svg>
          Toon op kaart
        </button>
      </div>
    </div>
  );
}

function InfoRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex gap-2">
      <span className="w-20 shrink-0 font-medium text-gray-500">{label}</span>
      <span className="text-gray-700">{value}</span>
    </div>
  );
}
