"use client";

import { useEffect, useState } from "react";
import dynamic from "next/dynamic";
import { useRouter } from "next/navigation";

// react-svg-worldmap must load only on client
const WorldMap = dynamic(() => import("react-svg-worldmap"), { ssr: false });

export default function HeatmapPage() {
  const [riskData, setRiskData] = useState([]);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  const countries = [
    "India", "United States", "China", "Germany", "United Kingdom",
    "France", "Japan", "Brazil", "Australia", "Russia",
    "Canada", "South Africa", "Italy", "Spain", "Mexico"
  ];

  useEffect(() => {
    const fetchRisk = async () => {
      setLoading(true);
      const results = [];

      for (const country of countries) {
        try {
          const res = await fetch(
            `http://127.0.0.1:8000/api/risk_score/${country}`
          );
          const data = await res.json();

          results.push({
            country: convertToISO(country),
            value: data.risk_score,
            name: country,
          });
        } catch (err) {
          console.log("Error fetching risk for", country);
        }
      }

      setRiskData(results);
      setLoading(false);
    };

    fetchRisk();
  }, []);

  const convertToISO = (country) => {
    const map = {
      India: "IN",
      "United States": "US",
      China: "CN",
      Germany: "DE",
      "United Kingdom": "GB",
      France: "FR",
      Japan: "JP",
      Brazil: "BR",
      Australia: "AU",
      Russia: "RU",
      Canada: "CA",
      "South Africa": "ZA",
      Italy: "IT",
      Spain: "ES",
      Mexico: "MX",
    };
    return map[country] || "IN";
  };

  // 🔥 CLICK HANDLER
  const handleCountryClick = (event) => {
    const countryName = event.countryName;
    if (!countryName) return;

    router.push(`/?country=${encodeURIComponent(countryName)}`);
  };

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <h1 className="text-3xl font-semibold text-center mb-6">
        🌎 Global Supply Chain Risk Heatmap
      </h1>

      {loading ? (
        <p className="text-center text-gray-500">Loading heatmap...</p>
      ) : (
        <WorldMap
          color="red"
          title="Risk Score by Country"
          valueSuffix=" risk"
          size="responsive"
          data={riskData}
          onClickFunction={handleCountryClick}   // 🔥 ADDED
        />
      )}
    </div>
  );
}
