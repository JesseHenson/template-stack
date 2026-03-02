/** Example TanStack Query hooks — replace with your product's hooks. */

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import api from "@/api/client";
import type { Item, ItemCreate, ItemUpdate } from "@/types";

export function useItems() {
  return useQuery({
    queryKey: ["items"],
    queryFn: async () => {
      const { data } = await api.get<Item[]>("/items");
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
    },
  });
}
