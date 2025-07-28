// app/error.tsx
'use client';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div className="text-center mt-10">
      <h2 className="text-2xl font-bold">Something went wrong!</h2>
      <button
        onClick={
          // Attempt to recover by re-rendering the segment
          () => reset()
        }
        className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
      >
        Try again
      </button>
    </div>
  );
}