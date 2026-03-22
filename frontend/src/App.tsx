import { useCallback, useEffect, useMemo, useState } from "react";
import type { Filters, Pool, View } from "./types";
import { Header } from "./components/Header";
import { FilterBar } from "./components/FilterBar";
import { PoolGrid } from "./components/PoolGrid";
import { PoolMap } from "./components/PoolMap";
import { Footer } from "./components/Footer";

const defaultFilters: Filters = {
  search: "",
  type: "",
  district: "",
  has25m: false,
  has50m: false,
};

function filterPools(pools: Pool[], filters: Filters): Pool[] {
  return pools.filter((pool) => {
    if (filters.search) {
      const q = filters.search.toLowerCase();
      const searchable = [
        pool.name,
        pool.address,
        pool.district,
        pool.operator,
        pool.features,
      ]
        .filter(Boolean)
        .join(" ")
        .toLowerCase();
      if (!searchable.includes(q)) return false;
    }
    if (filters.type && pool.type !== filters.type) return false;
    if (filters.district && pool.district !== filters.district) return false;
    if (filters.has25m && !pool.has25m) return false;
    if (filters.has50m && !pool.has50m) return false;
    return true;
  });
}

export default function App() {
  const [pools, setPools] = useState<Pool[]>([]);
  const [filters, setFilters] = useState<Filters>(defaultFilters);
  const [view, setView] = useState<View>("cards");
  const [highlightedPoolId, setHighlightedPoolId] = useState<string | null>(
    null,
  );
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(import.meta.env.BASE_URL + "pools.json")
      .then((res) => res.json())
      .then((data: Pool[]) => {
        setPools(data);
        setLoading(false);
      });
  }, []);

  const filtered = useMemo(() => filterPools(pools, filters), [pools, filters]);

  const districts = useMemo(
    () => [...new Set(pools.map((p) => p.district))].sort(),
    [pools],
  );

  const resetFilters = useCallback(() => setFilters(defaultFilters), []);

  const showOnMap = useCallback(
    (id: string) => {
      setView("map");
      setHighlightedPoolId(id);
    },
    [],
  );

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-blue-50">
        <div className="text-xl text-blue-600">Laden...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <FilterBar
        filters={filters}
        onChange={setFilters}
        onReset={resetFilters}
        districts={districts}
        view={view}
        onViewChange={setView}
      />
      <main className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
        <p className="mb-4 text-sm text-gray-500">
          {filtered.length} zwembad{filtered.length !== 1 ? "en" : ""} gevonden
        </p>
        {view === "cards" ? (
          <PoolGrid pools={filtered} onShowOnMap={showOnMap} />
        ) : (
          <PoolMap
            pools={filtered}
            highlightedPoolId={highlightedPoolId}
            onHighlightClear={() => setHighlightedPoolId(null)}
          />
        )}
      </main>
      <Footer />
    </div>
  );
}
