export type BudgetBand = "low" | "medium" | "high";

export interface UserPreferences {
  location?: string;
  budget?: BudgetBand;
  cuisine?: string;
  min_rating?: number;
  notes?: string;
}

export interface PresentationResult {
  name: string;
  cuisines: string;
  rating?: number;
  cost?: string;
  explanation: string;
}

export interface PresentationResponse {
  results: PresentationResult[];
  summary_blurb?: string;
}
