/** Example types — replace with your product's types. */

export interface Item {
  id: string;
  user_id: string;
  name: string;
  description: string;
  metadata: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

export interface ItemCreate {
  name: string;
  description?: string;
  metadata?: Record<string, unknown>;
}

export interface ItemUpdate {
  name?: string;
  description?: string;
  metadata?: Record<string, unknown>;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  limit: number;
  offset: number;
}
