import React, { useEffect, useState } from 'react';
import { testCorsConnection } from '../utils/testCors';

export default function CorsTest() {
  const [testResult, setTestResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const runTest = async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await testCorsConnection();
      setTestResult(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">CORS Test</h2>
      <button
        onClick={runTest}
        disabled={loading}
        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
      >
        {loading ? 'Testing...' : 'Test CORS'}
      </button>
      
      {testResult && (
        <div className="mt-4">
          <h3 className="font-bold">Result:</h3>
          <pre className="bg-gray-100 p-2 rounded mt-2">
            {JSON.stringify(testResult, null, 2)}
          </pre>
        </div>
      )}
      
      {error && (
        <div className="mt-4 text-red-600">
          <h3 className="font-bold">Error:</h3>
          <pre className="bg-red-100 p-2 rounded mt-2">{error}</pre>
        </div>
      )}
    </div>
  );
}
