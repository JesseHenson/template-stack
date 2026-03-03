/** Example TanStack Query hooks — replace with your product's hooks. */

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import api from "@/api/client";
import type { Item, ItemCreate, ItemUpdate, PaginatedResponse } from "@/types";

export function useItems({ limit = 50, offset = 0 } = {}) {
  return useQuery({
    queryKey: ["items", { limit, offset }],
    queryFn: async () => {
      const { data } = await api.get<PaginatedResponse<Item>>("/items", {
        params: { limit, offset },
      });
      return data;
    },
  });
}

export function useItem(id: string) {
  return useQuery({
    queryKey: ["items", id],
    queryFn: async () => {
      const { data } = await api.get<Item>(`/items/${id}`);
      return data;
    },
    enabled: !!id,
  });
}

export function useCreateItem() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (item: ItemCreate) => {
      const { data } = await api.post<Item>("/items", item);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["items"] });
      toast.success("Item created");
    },
    onError: () => {
      toast.error("Failed to create item");
    },
  });
}

export function useUpdateItem() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ id, ...update }: ItemUpdate & { id: string }) => {
      const { data } = await api.patch<Item>(`/items/${id}`, update);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["items"] });
      toast.success("Item updated");
    },
    onError: () => {
      toast.error("Failed to update item");
    },
  });
}

export function useDeleteItem() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (id: string) => {
      await api.delete(`/items/${id}`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["items"] });
      toast.success("Item deleted");
    },
    onError: () => {
      toast.error("Failed to delete item");
    },
  });
}
