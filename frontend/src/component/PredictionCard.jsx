export default function PredictionCard({ prediction }) {
  return (
    <div className="p-4 rounded-2xl shadow bg-white w-full">
      <p className="font-semibold">Model Status:</p>
      <p>{prediction.status}</p>

      <p className="font-semibold mt-2">Risk Score:</p>
      <p className="text-lg font-bold text-red-600">
        {(prediction.risk_score * 100).toFixed(1)}%
      </p>

      <p className="font-semibold mt-2">Label:</p>
      <p>{prediction.risk_label}</p>
    </div>
  );
}
