import { AppShell } from "@/components/layout/AppShell";
import { useItems } from "@/hooks/useItems";

export default function DashboardPage() {
  const { data, isLoading } = useItems();
  const items = data?.items;

  return (
    <AppShell>
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-500">Welcome</p>
        </div>

        <div className="rounded-lg border border-gray-200 bg-white p-6">
          <h2 className="mb-4 text-lg font-semibold">Items</h2>
          {isLoading ? (
            <p className="text-gray-500">Loading...</p>
          ) : items?.length ? (
            <ul className="divide-y divide-gray-100">
              {items.map((item) => (
                <li key={item.id} className="py-3">
                  <p className="font-medium">{item.name}</p>
                  <p className="text-sm text-gray-500">{item.description}</p>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-gray-500">No items yet.</p>
          )}
        </div>
      </div>
    </AppShell>
  );
}
