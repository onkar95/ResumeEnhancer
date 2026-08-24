export default function DiffLegend() {
  return (
    <div className="flex items-center gap-4 text-xs text-gray-500 mb-3">
      <span className="flex items-center gap-1">
        <span className="inline-block w-3 h-3 rounded" style={{ background: "lime" }} />
        Added / changed
      </span>
      <span className="flex items-center gap-1">
        <span className="inline-block w-3 h-3 rounded" style={{ background: "red" }} />
        Removed
      </span>
    </div>
  );
}