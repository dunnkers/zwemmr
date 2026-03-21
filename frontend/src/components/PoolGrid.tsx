import type { Pool } from "../types";
import { PoolCard } from "./PoolCard";

interface PoolGridProps {
  pools: Pool[];
  onShowOnMap: (id: string) => void;
}

export function PoolGrid({ pools, onShowOnMap }: PoolGridProps) {
  if (pools.length === 0) {
    return (
      <div className="py-16 text-center">
        <p className="text-lg text-gray-500">
          Geen zwembaden gevonden met deze filters.
        </p>
        <p className="mt-1 text-sm text-gray-400">
          Probeer andere zoektermen of filters.
        </p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
      {pools.map((pool) => (
        <PoolCard key={pool.id} pool={pool} onShowOnMap={onShowOnMap} />
      ))}
    </div>
  );
}
