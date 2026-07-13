interface Props {
  validation: any;
}

export default function ValidationPanel({ validation }: Props) {
  if (!validation) return null;

  const coverage = validation.keyword_coverage || 0;

  return (
    <div className="bg-white rounded-xl p-6 shadow">
      {" "}
      <h2 className="text-xl font-bold mb-4">Validation Results </h2>
      <div className="mb-3">Keyword Coverage</div>
      <div className="w-full bg-gray-200 rounded-full h-4">
        <div
          className="bg-green-500 h-4 rounded-full"
          style={{
            width: `${coverage}%`,
          }}
        />
      </div>
      <div className="mt-2">{coverage}%</div>
    </div>
  );
}
