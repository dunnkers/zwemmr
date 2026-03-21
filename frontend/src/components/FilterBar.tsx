import type { Filters, PoolType, View } from "../types";

const POOL_TYPES: { value: PoolType | ""; label: string }[] = [
  { value: "", label: "Alle types" },
  { value: "binnenbad", label: "Binnenbad" },
  { value: "combibad", label: "Combibad" },
  { value: "buitenbad", label: "Buitenbad" },
  { value: "leszwembad", label: "Leszwembad" },
  { value: "wellness", label: "Wellness" },
];

interface FilterBarProps {
  filters: Filters;
  onChange: (filters: Filters) => void;
  onReset: () => void;
  districts: string[];
  view: View;
  onViewChange: (view: View) => void;
}

export function FilterBar({
  filters,
  onChange,
  onReset,
  districts,
  view,
  onViewChange,
}: FilterBarProps) {
  const update = (patch: Partial<Filters>) =>
    onChange({ ...filters, ...patch });

  const hasActiveFilters =
    filters.search !== "" ||
    filters.type !== "" ||
    filters.district !== "" ||
    filters.has25m ||
    filters.has50m ||
    filters.crawlLane;

  return (
    <div className="sticky top-0 z-20 border-b border-gray-200 bg-white/80 shadow-sm backdrop-blur-sm">
      <div className="mx-auto max-w-7xl px-4 py-3 sm:px-6 lg:px-8">
        <div className="flex flex-wrap items-center gap-3">
          {/* Search */}
          <div className="relative min-w-48 grow sm:grow-0">
            <svg
              className="pointer-events-none absolute top-1/2 left-3 h-4 w-4 -translate-y-1/2 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
            <input
              type="text"
              placeholder="Zoek zwembad..."
              value={filters.search}
              onChange={(e) => update({ search: e.target.value })}
              className="w-full rounded-lg border border-gray-300 py-2 pr-3 pl-9 text-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none"
            />
          </div>

          {/* Type dropdown */}
          <select
            value={filters.type}
            onChange={(e) => update({ type: e.target.value as PoolType | "" })}
            className="rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none"
          >
            {POOL_TYPES.map((t) => (
              <option key={t.value} value={t.value}>
                {t.label}
              </option>
            ))}
          </select>

          {/* District dropdown */}
          <select
            value={filters.district}
            onChange={(e) => update({ district: e.target.value })}
            className="rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none"
          >
            <option value="">Alle stadsdelen</option>
            {districts.map((d) => (
              <option key={d} value={d}>
                {d}
              </option>
            ))}
          </select>

          {/* Checkboxes */}
          <label className="flex items-center gap-1.5 text-sm text-gray-700">
            <input
              type="checkbox"
              checked={filters.has25m}
              onChange={(e) => update({ has25m: e.target.checked })}
              className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            25m
          </label>
          <label className="flex items-center gap-1.5 text-sm text-gray-700">
            <input
              type="checkbox"
              checked={filters.has50m}
              onChange={(e) => update({ has50m: e.target.checked })}
              className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            50m
          </label>
          <label className="flex items-center gap-1.5 text-sm text-gray-700">
            <input
              type="checkbox"
              checked={filters.crawlLane}
              onChange={(e) => update({ crawlLane: e.target.checked })}
              className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            Crawlbaan
          </label>

          {/* Reset */}
          {hasActiveFilters && (
            <button
              onClick={onReset}
              className="rounded-lg px-3 py-2 text-sm text-gray-500 hover:bg-gray-100 hover:text-gray-700"
            >
              Reset
            </button>
          )}

          {/* Spacer */}
          <div className="grow" />

          {/* View toggle */}
          <div className="flex rounded-lg border border-gray-300 bg-gray-50">
            <button
              onClick={() => onViewChange("cards")}
              className={`rounded-l-lg px-3 py-2 text-sm font-medium ${
                view === "cards"
                  ? "bg-blue-600 text-white"
                  : "text-gray-600 hover:bg-gray-100"
              }`}
            >
              Kaarten
            </button>
            <button
              onClick={() => onViewChange("map")}
              className={`rounded-r-lg px-3 py-2 text-sm font-medium ${
                view === "map"
                  ? "bg-blue-600 text-white"
                  : "text-gray-600 hover:bg-gray-100"
              }`}
            >
              Kaart
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
