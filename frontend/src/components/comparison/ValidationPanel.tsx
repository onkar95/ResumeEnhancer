interface Props {
  validation: any;
}

export default function ValidationPanel({ validation }: Props) {
  if (!validation) return null;

  const coverage = validation.keyword_coverage || 0;

  return (
    <div className="card p-6 min-w-0">
      <h2 className="text-xl font-bold mb-4 text-gray-900">Validation Results</h2>
      <div className="mb-3 text-sm text-gray-600">Keyword Coverage</div>
      <div className="w-full bg-gray-100 rounded-full h-3">
        <div
          className="bg-brand-500 h-3 rounded-full transition-all"
          style={{ width: `${coverage}%` }}
        />
      </div>
      <div className="mt-2 text-sm font-medium text-gray-700">{coverage}%</div>
    </div>
  );
}