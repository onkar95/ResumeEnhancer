interface Props {
  message?: string;
}

export default function LoadingScreen({ message = "Loading..." }: Props) {
  return (
    <div className="flex min-h-[240px] items-center justify-center bg-gray-50 p-8">
      <div className="flex items-center gap-3 rounded-xl border border-gray-200 bg-white px-4 py-3 shadow-sm">
        <span className="h-4 w-4 animate-spin rounded-full border-2 border-gray-200 border-t-brand-600" />
        <span className="text-sm font-medium text-gray-600">{message}</span>
      </div>
    </div>
  );
}
