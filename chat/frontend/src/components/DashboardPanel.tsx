export function DashboardPanel() {
  return (
    <div className="flex-1 h-full border-r border-gray-200">
      <iframe
        src="/dashboard/index.html"
        className="w-full h-full border-0"
        title="BP Dashboard"
      />
    </div>
  );
}
