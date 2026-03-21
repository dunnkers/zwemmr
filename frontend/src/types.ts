export interface Pool {
  id: string;
  name: string;
  type: "binnenbad" | "combibad" | "buitenbad" | "leszwembad" | "wellness";
  district: string;
  operator: string;
  address: string;
  lat: number;
  lng: number;
  phone: string | null;
  has25m: boolean;
  has50m: boolean;
  dimensions: string | null;
  waterTemp: number | null;
  waterTempNote: string | null;
  price: number | null;
  priceNote: string | null;
  stadspasPrice: number | null;
  crawlLane: boolean;
  crawlLaneNote: string | null;
  reservationRequired: boolean;
  features: string | null;
  website: string | null;
  scheduleUrl: string | null;
}

export type PoolType = Pool["type"];

export interface Filters {
  search: string;
  type: PoolType | "";
  district: string;
  has25m: boolean;
  has50m: boolean;
  crawlLane: boolean;
}

export type View = "cards" | "map";
